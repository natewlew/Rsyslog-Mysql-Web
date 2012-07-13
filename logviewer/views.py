"""
This file is part of Rsyslog Mysql Web, Copyright 2012 Nathan Lewis <natewlew@gmail.com>

    Rsyslog Mysql Web is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Rsyslog Mysql Web is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Rsyslog Mysql Web.  If not, see <http://www.gnu.org/licenses/>.
"""

from django.shortcuts import render_to_response
from logviewer.models import Systemevents, Facilities, Priorites
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.db.models import Q
import operator
from logviewer.utils import queryHelper, paramHelper

template="logviewer"

def index(request):

    return render_to_response(template + '/index.html', {'SITE_URL': settings.SITE_URL, 'MEDIA_URL': settings.MEDIA_URL})    
    
    
def rsyslogjson(request):

    import gviz_api
    from django.http import HttpResponse
    
    #import pdb; pdb.set_trace()
    
    columns = set(request.GET.get('tq', '').split(','))
    split_colums = "";
    params = {}
    
    # Default Params
    orderby = ""
    direction = ""
    
    # Create params from tq split
    for column in columns:
        split_columns = column.split('::')
        
        try:
            params[split_columns[0].strip()] = split_columns[1].strip()
        except:
            pass
    
    # Set order by and direction params
    try:
        orderby = params['orderby']
        direction = params['direction']
    except:
        pass
        
    if len(orderby) == 0:
        orderby = "-id" # Set default orderby if orderby param is not set
    else: # If orderby is set
        if len(direction) > 0: # if direction is set
            if direction == "desc": # if direction is desc add the minus sign else leave is alone
                orderby = "-%s" % orderby
    
	# Set form Values
        
    param_helper = paramHelper()
    
    devicereportedtime_start = param_helper.getStringParam(params, 'devicereportedtime_start', '')   
    devicereportedtime_end = param_helper.getStringParam(params, 'devicereportedtime_end', '')     
    fromhost = param_helper.getStringParam(params, 'fromhost', '')   
    priority = param_helper.getStringParam(params, 'priority', '') 
    syslogtag = param_helper.getStringParam(params, 'syslogtag', '')  
    facility = param_helper.getStringParam(params, 'facility', '') 
    message = param_helper.getStringParam(params, 'message', '')
    
    operator = param_helper.getStringParam(params, 'operator', '')
    
    rows = param_helper.getIntParam(params, 'rows', 20) # if rows is not an int, set it to 20  
    page = param_helper.getIntParam(params, 'page', 1) # if page is not an int, set it to 1
    
    export_format = param_helper.getStringParam(params, 'export_format', '')
    
    # Make sure correct export value is set
    if export_format != 'csv' and export_format != 'tsv': 
        export_format = '';
    
    query_helper = queryHelper()
    
    query_helper.setQueryDateRange('devicereportedtime', devicereportedtime_start, devicereportedtime_end)
    
    query_helper.setQueryList(fromhost, 'fromhost')
    query_helper.setQueryList(priority, 'priority__severity')
    query_helper.setQueryList(syslogtag, 'syslogtag')
    query_helper.setQueryList(facility, 'facility__facility')
    query_helper.setQueryList(message, 'message')
    
    query_helper.setOperator(operator) # set the and,or operator before get_list
    
    list_in_txt = query_helper.get_list_in()
    list_ex_txt = query_helper.get_list_ex()
      
    # Get the query set
    queryset = Systemevents.objects.filter( list_in_txt ).exclude( list_ex_txt ).order_by(orderby).all().select_related("id","devicereportedtime","facility","priority","fromhost","syslogtag","message")
    
    # Export is not set. Do standard Page
    if len(export_format) == 0:
    
        # Set the paginator
        paginator = Paginator(queryset, rows)
        
        try:
            limited_query = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            limited_query = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            limited_query = paginator.page(paginator.num_pages)
     
    # Export is Set. Do not Page but limit query       
    else:
       limited_query = queryset[:2000]
     
    #return HttpResponse(queryset.query)

    # Set the fields for the table header
    description = {}
    description['id'] = ('number', 'ID')
    description['devicereportedtime'] = ('datetime', 'Reported Time')
    description['facility'] = ('string', 'Facility')
    description['priority'] = ('string', 'Priority')
    description['fromhost'] = ('string', 'Host')
    description['syslogtag'] = ('string', 'Tag')
    description['message'] = ('string', 'Message')
    description['messagefull'] = ('string', 'Message Full')

    myvalues = {}
    
    # Set the google datatable
    data_table = gviz_api.DataTable(description)
    
    # Populate the data in the table
    for query in limited_query:     
        
        if(len(query.message) > 120):
            mymessage = "%s ...." % query.message[:120] # trim the message if it is greater than 120 chars
        else:
            mymessage = query.message # leave it alone
        
        myvalues = {'id': query.id,
                    'devicereportedtime': query.devicereportedtime,
                    'facility': query.facility,
                    'priority': query.priority,
                    'fromhost': query.fromhost,
                    'syslogtag': query.syslogtag,
                    'message': mymessage,
                    'messagefull': query.message
                    }
        
        data_table.AppendData([myvalues])

    #import pdb; pdb.set_trace()
    
    # Export to CSV
    if export_format == 'csv':
    
        my_data = data_table.ToCsv(columns_order=("id","devicereportedtime","facility","priority","fromhost","syslogtag","messagefull"))
        
        response = HttpResponse(my_data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=syslog_export.csv'
    
        return response
        
    # Export to TSV
    if export_format == 'tsv':
    
        my_data = data_table.ToTsvExcel(columns_order=("id","devicereportedtime","facility","priority","fromhost","syslogtag","messagefull"))
        
        response = HttpResponse(my_data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=syslog_export_excel.csv'
    
        return response
        
    # Default: Export to Table
    else: 
        return HttpResponse(data_table.ToResponse(columns_order=("id","devicereportedtime","facility","priority","fromhost","syslogtag","message","messagefull"), 
                                                  tqx=request.GET.get('tqx', '')))
    
    
    
    
    
    
    
    
    
    
    
    
    
