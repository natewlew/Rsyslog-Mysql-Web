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
import csv

template="logviewer"
                                                 
def index(request):

        return render_to_response(template + '/flexgrid.html', {'SITE_URL': settings.SITE_URL, 'MEDIA_URL': settings.MEDIA_URL}) 
        
def flexigridajax(request):

    # Get Form Values
    devicereportedtime_start = request.GET.get('devicereportedtime_start', '')  
    devicereportedtime_end = request.GET.get('devicereportedtime_end', '')       
    fromhost = request.GET.get('fromhost', '')   
    priority = request.GET.get('priority', '')   
    syslogtag = request.GET.get('syslogtag', '')   
    facility = request.GET.get('facility', '')   
    message = request.GET.get('message', '')   
    
    operator = request.GET.get('operator', '')
    
    export_format = request.GET.get('export_format', '')
    
    # Build the Query
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
    
    # Get the Flexigrid Params
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
    
    #return HttpResponse(queryset.query)
        
    mydate = ""
    
    DATE_FORMAT = "%Y-%m-%d" 
    TIME_FORMAT = "%H:%M:%S"

    # Build Data for Export to CSV
    if export_format == "csv":
    
        # Build CSV Response Headers
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=export.csv'
        
        writer = csv.writer(response)
        
        # Write CSV header Row
        writer.writerow(['id', 
                         'devicereportedtime', 
                         'facility', 
                         'priority', 
                         'fromhost', 
                         'syslogtag', 
                         'message'])
        
        # Don't Paginate Export but limit to 2000 rows
        rows = queryset[0:2000]
        
        # Populate the data in the table
        for query in queryset:     
            
            mydate = query.devicereportedtime.strftime("%s %s" % (DATE_FORMAT, TIME_FORMAT))
            
            # Write data rows to csv file
            writer.writerow([query.id, 
                             mydate, 
                             query.facility.facility, 
                             query.priority.severity, 
                             query.fromhost, 
                             query.syslogtag,
                             query.message])

        return response

    # Default: Build data for Flexigrid
    else:
    
        my_list = []
        count = 1;
    
        # Paginate Results
        p = Paginator(queryset, rp)
        
        rows = p.page(page)
    
        # Populate the data in the table
        for query in rows:     
        
            # Trim Message if it is greater than 120 characters
            if(len(query.message) > 120):
                mymessage = "%s ...." % query.message[:120] # trim the message if it is greater than 120 chars
            else:
                mymessage = query.message # leave it alone
            
            mydate = query.devicereportedtime.strftime("%s %s" % (DATE_FORMAT, TIME_FORMAT))
            
            # Create Dictionary for Row
            myvalues = { 'id': count,
                         'cell':
                            {'id': query.id,
                            'devicereportedtime': mydate,
                            'facility': query.facility.facility,
                            'priority': query.priority.severity,
                            'fromhost': query.fromhost,
                            'syslogtag': query.syslogtag,
                            'message': mymessage,
                            'messagefull': query.message
                            }
                        }
            
            # Append Dictionary to List
            my_list.append(myvalues)
            
            count += 1  
        
        # Create Final Json Dictionary
        json_dict = {
            'page': page,
            'total': p.count,
            'rows': my_list
            }
        
        # Return Json
        return HttpResponse(simplejson.dumps(json_dict), mimetype='application/json')

    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
