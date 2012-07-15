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
from logviewer.utils import queryHelper
from django.http import HttpResponse
import simplejson

template="logviewer"
                                                 
def index(request):

        return render_to_response(template + '/flexgrid.html', {'SITE_URL': settings.SITE_URL, 'MEDIA_URL': settings.MEDIA_URL}) 
        
def flexigridajax(request):

    devicereportedtime_start = request.GET.get('devicereportedtime_start', '')  
    devicereportedtime_end = request.GET.get('devicereportedtime_end', '')       
    fromhost = request.GET.get('fromhost', '')   
    priority = request.GET.get('priority', '')   
    syslogtag = request.GET.get('syslogtag', '')   
    facility = request.GET.get('facility', '')   
    message = request.GET.get('message', '')   
    
    operator = request.GET.get('operator', '')
    
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
    
    sortname = request.GET.get('sortname', 'id') # Sort Field
    page = request.GET.get('page', 1) # Page (EX: 2 of 20)
    sortorder = request.GET.get('sortorder', 'desc') # Ascending/descending
    rp = int(request.GET.get('rp', 20)) # Requests per page
    #qtype = request.GET.get('qtype', None) # Query type
    #query = request.GET.get('query', None) # Query string
        
    if sortorder == "desc": # if direction is desc add the minus sign else leave is alone
        sortname = "-%s" % sortname
          
    # Get the query set
    queryset = Systemevents.objects.filter( list_in_txt ).exclude( list_ex_txt ).order_by(sortname)     
    #queryset = Systemevents.objects.order_by(sortname)
    
    #return HttpResponse(queryset.query)
    
    p = Paginator(queryset, rp)
        
    rows = p.page(page)
        
    my_list = []
    count = 1;
    
    DATE_FORMAT = "%Y-%m-%d" 
    TIME_FORMAT = "%H:%M:%S"

    # Populate the data in the table
    for query in rows:     
    
        if(len(query.message) > 120):
            mymessage = "%s ...." % query.message[:120] # trim the message if it is greater than 120 chars
        else:
            mymessage = query.message # leave it alone
        
        myvalues = { 'id': count,
                     'cell':
                    {'id': query.id,
                    'devicereportedtime': query.devicereportedtime.strftime("%s %s" % (DATE_FORMAT, TIME_FORMAT)),
                    'facility': query.facility.facility,
                    'priority': query.priority.severity,
                    'fromhost': query.fromhost,
                    'syslogtag': query.syslogtag,
                    'message': mymessage,
                    'messagefull': query.message
                    }
                    }
        
        my_list.append(myvalues)
        
        count += 1  
    
    json_dict = {
        'page': page,
        'total': p.count,
        'rows': my_list
        }
    
    return HttpResponse(simplejson.dumps(json_dict), mimetype='application/json')

    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
