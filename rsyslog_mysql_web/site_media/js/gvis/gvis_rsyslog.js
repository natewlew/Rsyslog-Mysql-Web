google.load('visualization', '1', {'packages' : ['table']});
google.setOnLoadCallback(init);

function init() {

  setDetailText("", "", "", "", ""); // Clear the detail text
  
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
  this.view = null;

  var self = this;
  var addListener = google.visualization.events.addListener;
  addListener(this.table, 'page', function(e) {self.handlePage(e)});
  addListener(this.table, 'sort', function(e) {self.handleSort(e)});
  addListener(this.table, 'select', function(e) {self.handleSelect(e)});
      
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
  var queryClause = getFormQuery() + this.sortQueryClause + this.pageQueryClause;
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
    
    this.view = new google.visualization.DataView(this.currentDataTable);
    this.view.setColumns([0,1,2,3,4,5,6]);
    
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
    formatter.addRange("Error", "Error-1", 'black', '#FFC0C0');
    formatter.addRange("Warning", "Warning-1", 'black', '#FFCD82');
    formatter.addRange("Notice", "Notice-1", 'white', '#94DBFF');
    formatter.addRange("Informational", "Informational-1", 'white', '#85FF85');
    formatter.addRange("Debug", "Debug-1", 'white', '#FFFF4D');
    formatter.format(this.currentDataTable, 3);
  
    this.table.draw(this.view, this.tableOptions);
  
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
  this.sortQueryClause = 'orderby::' + colID + (!isAscending ? ',direction::desc,' : ',direction::asc,');
  // Calls sendAndDraw internally.
  this.handlePage({'page': 0});
};


/** Handles a page event with the given properties. */
TableQueryWrapper.prototype.handlePage = function(properties) {

  setDetailText("", "", "", "", ""); // Clear the detail text
  
  var localTableNewPage = properties['page']; // 1, -1 or 0
  var newPage = 0;
  if (localTableNewPage != 0) {
    newPage = this.currentPageIndex + localTableNewPage;
  }
  if (this.setPageQueryClause(newPage)) {
    this.sendAndDraw();
  }
};
     
/** Handles Select on Row **/
TableQueryWrapper.prototype.handleSelect = function(properties) {
    var myrow = this.table.getSelection()[0].row;
    //alert('You selected ' + this.currentDataTable.getValue(myrow, 7));
    
    var message_detail_text = this.currentDataTable.getValue(myrow, 7);  
    var host_detail_text = this.currentDataTable.getValue(myrow, 4); 
    var date_detail_text = this.currentDataTable.getValue(myrow, 1);  
    var priority_detail_text = this.currentDataTable.getValue(myrow, 3);
    var tag_detail_text = this.currentDataTable.getValue(myrow, 5);
    
    setDetailText(message_detail_text, host_detail_text, date_detail_text, priority_detail_text,tag_detail_text);

};

/** Set the Detail Text. This is located below the data table **/
function setDetailText(mymessage, host, mydate, priority, tag) {

    var host_query_helper = ""
    var priority_query_helper = ""
    var tag_query_helper = ""
    
    if(mymessage.length > 0) {
    
        host_query_helper = '<input type="button" value="Search" onClick="append_host_query(\'' + host + '\')"> <input type="button" value="Exclude" onClick="append_host_query(\'-' + host + '\')"> '
        
        priority_query_helper = '<input type="button" value="Search" onClick="append_priority_query(\'' + priority + '\')"> <input type="button" value="Exclude" onClick="append_priority_query(\'-' + priority + '\')"> '
        
        tag_query_helper = '<input type="button" value="Search" onClick="append_tag_query(\'' + tag + '\')"> <input type="button" value="Exclude" onClick="append_tag_query(\'-' + tag + '\')"> '
    }
    
    
    
    var message_detail = document.getElementById('message_detail');
    message_detail.innerHTML = mymessage;
    
    var host_detail = document.getElementById('host_detail');  
    host_detail.innerHTML = host_query_helper + host;
    
    var date_detail = document.getElementById('date_detail');  
    date_detail.innerHTML = mydate;
    
    var priority_detail = document.getElementById('priority_detail'); 
      
    priority_detail.innerHTML = priority_query_helper + priority;
    
    var tag_detail = document.getElementById('tag_detail');  
    tag_detail.innerHTML = tag_query_helper + tag;
}

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
  this.pageQueryClause = 'page::' + (pageIndex + 1) + ',rows::' + pageSize;
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

function reset_page() {
    
    clear_form()
    
    init();
}

function formsubmit() {
    
    init();
    
    return false;
}

function clear_form() {

    clear_input('fromhost');
    clear_input('priority');
    clear_input('syslogtag');
}

function getFormQuery() {
    
    var fromhost = document.getElementById('fromhost');
    
    var fromhostQuery = 'fromhost::' + fromhost.value + ','
    
    return fromhostQuery;
}

function clear_input(input) {

    var element = document.getElementById(input);
    element.value = "";
    
}

function append_host_query(host) {

    var element = document.getElementById('fromhost');
    
    if(element.value.length > 0) {
        element.value = element.value + '||' + host;
    } else {
        element.value = host;
    }

}

function append_priority_query(priority) {

    var element = document.getElementById('priority');
    
    if(element.value.length > 0) {
        element.value = element.value + '||' + priority;
    } else {
        element.value = priority;
    }

}

function append_tag_query(tag) {

    var element = document.getElementById('syslogtag');
    
    if(element.value.length > 0) {
        element.value = element.value + '||' + tag;
    } else {
        element.value = tag;
    }

}
