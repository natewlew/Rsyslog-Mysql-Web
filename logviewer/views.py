"""
This file is part of Rsyslog Mysql Web, Copyright 2012 Nathan Lewis <natewlew@gmail.com>

    Rsyslog Mysql Web is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
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
from django.utils import simplejson
import csv
from datetime import datetime
from django.db.models import Count

template="logviewer"
                                                 
def index(request):

        return render_to_response(template + '/flexgrid.html', {'SITE_URL': settings.SITE_URL, 'MEDIA_URL': settings.MEDIA_URL}) 
        
def flexigridajax(request):

    #import pdb; pdb.set_trace()
    
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
    
    if sortname == 'age': # Age is a calculated column. The database doesn't know about it.
        sortname = 'id';
        
    if sortorder == "desc": # if direction is desc add the minus sign else leave is alone
        sortname = "-%s" % sortname
          
    # Get the query set
    queryset = Systemevents.objects.filter( list_in_txt ).exclude( list_ex_txt ).order_by(sortname)     
    
    #return HttpResponse(queryset.query)
        
    mydate = ""
    
    DATE_FORMAT = "%Y-%m-%d" 
    # 24 Hour(%H:%M:%S), 12 Hour (%I:%M:%S %p)
    TIME_FORMAT = "%I:%M:%S %p"

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
        rows = queryset[0:1999]
        
        # Populate the data in the table
        for query in rows:     
            
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

    # Build Data for Chart
    elif export_format == "chart":
    
        my_list = []
        
        chartcolumn = request.GET.get('chartcolumn', 'priority__severity')
        
        # It chart column selected, there needs to be special processing
        if chartcolumn == "devicereportedtime":
        
            # Using Checksum in values. This is only was I could get DATE(DeviceReportedTime) 
            # in the group by to work. Checksum is always zero so it does not affect the query.
            # Otherwise a valid column is in the group by and destroys the query.
            rows = queryset.values('checksum').extra(select={chartcolumn: """DATE(DeviceReportedTime)"""}).annotate(my_count=Count('id')).values(chartcolumn, 'my_count').order_by(chartcolumn)
            
            # Populate the data in the table
            for query in rows:
            
                my_list.append([query[chartcolumn].strftime("%s" % (DATE_FORMAT)), query['my_count']])
            
        # Normal Chart Column Field
        else:
        
            rows = queryset.values(chartcolumn).annotate(my_count=Count(chartcolumn)).values(chartcolumn, 'my_count')
        
            # Populate the data in the table
            for query in rows:
            
                my_list.append([query[chartcolumn], query['my_count']])
            
        # Return Json
        return HttpResponse(simplejson.dumps([my_list]), mimetype='application/json')
        
    # Default: Build data for Flexigrid
    else:
    
        my_list = []
        count = 1;
    
        # Paginate Results
        p = Paginator(queryset, rp)
        
        # Try to Fetch the Query
        try:
        
            rows = p.page(page)
    
            # Populate the data in the table
            for query in rows:     
            
                # Trim Message if it is greater than 120 characters
                if(len(query.message) > 120):
                    mymessage = "%s ...." % query.message[:120] # trim the message if it is greater than 120 chars
                else:
                    mymessage = query.message # leave it alone
                
                mydate = query.devicereportedtime.strftime("%s %s" % (DATE_FORMAT, TIME_FORMAT))
                
                mynow = datetime.now()
                
                tdelta = mynow - query.devicereportedtime # Get age 
                
                # Create Dictionary for Row
                myvalues = { 'id': count,
                             'cell':
                                {'id': query.id,
                                'devicereportedtime': mydate,
                                'age': "%s, %s, %s" % (tdelta.days, tdelta.seconds//3600, (tdelta.seconds//60)%60), # Get age in Days,Hours,Minutes
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
                
            # Set the Row Count
            my_count = p.count
        
        # If there is an Error
        # set the count to zero
        # and return empty result.
        except:
        
            # Set the Row Count
            my_count = 0
        
        # Create Final Json Dictionary
        json_dict = {
            'page': page,
            'total': my_count,
            'rows': my_list
            }
        
        # Return Json
        return HttpResponse(simplejson.dumps(json_dict), mimetype='application/json')

    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
