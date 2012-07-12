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
    page = ""
    rows = ""
    orderby = ""
    direction = ""
    
    # Create params from tq split
    for column in columns:
        split_columns = column.split(':')
        
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

    # set page and row params
    try:
        page = params['page']
        rows = params['rows']
    except:
        pass
    
    # if rows is not an integer, set it to 20
    try:
	    rows=int(rows) 
    except:
	    rows = 20
        
    # Get the query set
    queryset = Systemevents.objects.all().order_by(orderby).select_related("id","devicereportedtime","facility","priority","fromhost","syslogtag","message")
    
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

    return HttpResponse(data_table.ToResponse(columns_order=("id","devicereportedtime","facility","priority","fromhost","syslogtag","message","messagefull"), 
                                              tqx=request.GET.get('tqx', '')))
    
    
    
    
    
    
    
    
    
    
    
    
    
