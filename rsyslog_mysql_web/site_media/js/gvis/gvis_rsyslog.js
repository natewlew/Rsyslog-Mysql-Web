google.load('visualization', '1', {'packages' : ['table']});
google.setOnLoadCallback(init);

function init() {
  query = new google.visualization.Query(dataSourceUrl);
  container = document.getElementById(elementID);
  options = {'pageSize': default_page};
  sendAndDraw();
}

function sendAndDraw() {
  query.abort();
  var tableQueryWrapper = new TableQueryWrapper(query, container, options);
  tableQueryWrapper.sendAndDraw();
}


function setOption(prop, value) {
  options[prop] = value;
  sendAndDraw();
}

var TableQueryWrapper = function(query, container, options) {

  this.table = new google.visualization.Table(container);
  this.query = query;
  this.sortQueryClause = '';
  this.pageQueryClause = '';
  this.container = container;
  this.currentDataTable = null;

  var self = this;
  var addListener = google.visualization.events.addListener;
  addListener(this.table, 'page', function(e) {self.handlePage(e)});
  addListener(this.table, 'sort', function(e) {self.handleSort(e)});

  options = options || {};
  options = TableQueryWrapper.clone(options);

  options['sort'] = 'event';
  options['page'] = 'event';
  options['showRowNumber'] = showRowNumber;
  var buttonConfig = 'pagingButtonsConfiguration';
  options[buttonConfig] = options[buttonConfig] || 'both';
  options['pageSize'] = (options['pageSize'] > 0) ? options['pageSize'] : default_page;
  options['allowHtml'] = true;
  this.pageSize = options['pageSize'];
  this.tableOptions = options;
  this.currentPageIndex = 0;
  this.setPageQueryClause(0);
};


/**
 * Sends the query and upon its return draws the Table visualization in the
 * container. If the query refresh interval is set then the visualization will
 * be redrawn upon each refresh.
 */
TableQueryWrapper.prototype.sendAndDraw = function() {
  this.query.abort();
  var queryClause = this.sortQueryClause + ' ' + this.pageQueryClause;
  this.query.setQuery(queryClause);
  this.table.setSelection([]);
  var self = this;
  this.query.send(function(response) {self.handleResponse(response)});
};


/** Handles the query response after a send returned by the data source. */
TableQueryWrapper.prototype.handleResponse = function(response) {
  this.currentDataTable = null;
  if (response.isError()) {
    google.visualization.errors.addError(this.container, response.getMessage(),
        response.getDetailedMessage(), {'showInTooltip': false});
  } else {
    this.currentDataTable = response.getDataTable();
    
    /*
    Priority Conditional Formating
    0	Emergency //brown #917171
    1	Alert // dark red #B23232
    2	Critical //red #FF4747
    3	Error //pink #FFC0C0
    4	Warning //orange #FFCD82
    5	Notice // blue #94DBFF
    6	Informational //green #85FF85
    7	Debug //yellow #FFFF4D
    */
                    
    var formatter = new google.visualization.ColorFormat();
    formatter.addRange("Emergency", "Emergency-1", 'white', '#917171');
    formatter.addRange("Alert", "Alert-1", 'white', '#B23232');
    formatter.addRange("Critical", "Critical-1", 'white', '#FF4747');
    formatter.addRange("Error", "Error-1", 'white', '#FFC0C0');
    formatter.addRange("Warning", "Warning-1", 'white', '#FFCD82');
    formatter.addRange("Notice", "Notice-1", 'white', '#94DBFF');
    formatter.addRange("Informational", "Informational-1", 'white', '#85FF85');
    formatter.addRange("Debug", "Debug-1", 'white', '#FFFF4D');
    formatter.format(this.currentDataTable, 3);
  
    this.table.draw(this.currentDataTable, this.tableOptions);
  }
};


/** Handles a sort event with the given properties. Will page to page=0. */
TableQueryWrapper.prototype.handleSort = function(properties) {
  var columnIndex = properties['column'];
  var isAscending = properties['ascending'];
  this.tableOptions['sortColumn'] = columnIndex;
  this.tableOptions['sortAscending'] = isAscending;
  // dataTable exists since the user clicked the table.
  var colID = this.currentDataTable.getColumnId(columnIndex);
  this.sortQueryClause = 'order by `' + colID + (!isAscending ? '` desc' : '`');
  // Calls sendAndDraw internally.
  this.handlePage({'page': 0});
};


/** Handles a page event with the given properties. */
TableQueryWrapper.prototype.handlePage = function(properties) {
  var localTableNewPage = properties['page']; // 1, -1 or 0
  var newPage = 0;
  if (localTableNewPage != 0) {
    newPage = this.currentPageIndex + localTableNewPage;
  }
  if (this.setPageQueryClause(newPage)) {
    this.sendAndDraw();
  }
};


/**
 * Sets the pageQueryClause and table options for a new page request.
 * In case the next page is requested - checks that another page exists
 * based on the previous request.
 * Returns true if a new page query clause was set, false otherwise.
 */
TableQueryWrapper.prototype.setPageQueryClause = function(pageIndex) {
  var pageSize = this.pageSize;

  if (pageIndex < 0) {
    return false;
  }
  var dataTable = this.currentDataTable;
  if ((pageIndex == this.currentPageIndex + 1) && dataTable) {
    if (dataTable.getNumberOfRows() < pageSize) {
      return false;
    }
  }
  this.currentPageIndex = pageIndex;
  var newStartRow = this.currentPageIndex * pageSize;
  // Get the pageSize + 1 so that we can know when the last page is reached.
  //this.pageQueryClause = 'limit ' + (pageSize) + ' offset ' + newStartRow;
  this.pageQueryClause = 'page:' + (pageIndex + 1) + ',rows:' + pageSize;
  //alert(this.pageQueryClause);
  // Note: row numbers are 1-based yet dataTable rows are 0-based.
  this.tableOptions['firstRowNumber'] = newStartRow + 1;
  return true;
};


/** Performs a shallow clone of the given object. */
TableQueryWrapper.clone = function(obj) {
  var newObj = {};
  for (var key in obj) {
    newObj[key] = obj[key];
  }
  return newObj;
};
