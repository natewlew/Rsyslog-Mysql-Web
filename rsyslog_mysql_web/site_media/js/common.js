/**
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
**/

/**
    Reset Page to start
**/
function reset_page() {
    
    clear_form()
    
    setDetailText("", "", "", "", "", ""); // Clear the detail text
    
    setTimer(null);
    
    clear_input_dropdown('pagesize', default_page);
    clear_input_dropdown('refresh', "");
    clear_input_dropdown('export', "");
    
    //init();
    // need to implement reset
}

/**
    Clear Form
**/
function clear_form() {

    clear_input('fromhost');
    clear_input('priority');
    clear_input('syslogtag');
    clear_input('message');
    clear_input('facility');  
    clear_input('devicereportedtime_start');
    clear_input('devicereportedtime_end');
    clear_input_dropdown('operator', 'or');
    clear_input_dropdown('operator', 'or');
}

/**
    Clear an elements value
    
    @param string input - Element ID
**/
function clear_input(elem) {

    var element = document.getElementById(elem);
    element.value = "";
}

function clear_input_dropdown(elem, value) {
    
    var element = document.getElementById(elem);
    element.value = value;
    
}

/** 

    Set the Detail Text. This is located below the data table 
    
    @param string mymessage - Message String
    @param string host - From Host
    @param string mydate - Date
    @param string priority - Priority
    @param string tag - Syslog Tag
    @param string facility - Facility String
    
**/
function setDetailText(mymessage, host, mydate, priority, tag, facility) {

    var host_query_helper = ""
    var facility_query_helper = ""
    var priority_query_helper = ""
    var tag_query_helper = ""
    
    // Set Query Helpers
    if(mymessage.length > 0) {
    
        host_query_helper = '<input type="button" value="Search" onClick="append_query(\'' + host + '\', \'fromhost\')">'
        host_query_helper += '<input type="button" value="Exclude" onClick="append_query(\'--' + host + '\', \'fromhost\')"> '
        
        facility_query_helper = '<input type="button" value="Search" onClick="append_query(\'' + facility + '\', \'facility\')">'
        facility_query_helper += '<input type="button" value="Exclude" onClick="append_query(\'--' + facility + '\', \'facility\')"> '
        
        priority_query_helper = '<input type="button" value="Search" onClick="append_query(\'' + priority + '\', \'priority\')">'
        priority_query_helper += '<input type="button" value="Exclude" onClick="append_query(\'--' + priority + '\', \'priority\')"> '
        
        tag_query_helper = '<input type="button" value="Search" onClick="append_query(\'' + tag + '\', \'syslogtag\')">'
        tag_query_helper += '<input type="button" value="Exclude" onClick="append_query(\'--' + tag + '\', \'syslogtag\')"> '
        
    }
    
    
    var message_detail = document.getElementById('message_detail');
    message_detail.innerHTML = mymessage;
    
    var host_detail = document.getElementById('host_detail');  
    host_detail.innerHTML = host_query_helper + host;
    
    var facility_detail = document.getElementById('facility_detail');  
    facility_detail.innerHTML = facility_query_helper + facility;
    
    var date_detail = document.getElementById('date_detail');  
    date_detail.innerHTML = mydate;
    
    var priority_detail = document.getElementById('priority_detail');   
    priority_detail.innerHTML = priority_query_helper + priority;
    
    var tag_detail = document.getElementById('tag_detail');  
    tag_detail.innerHTML = tag_query_helper + tag;
}

/**
    Timer Variables
**/
var time_interval = null
var myTimerVal = null

/**
    Turn Timer on and off
**/
function initTimer() {

    clearInterval(myTimerVal);
    
    if(isNaN(time_interval) && 
       parseInt(time_interval)!=time_interval){
         time_interval = null;
    } else if(time_interval < 5000) {
        time_interval = null;
    }
    
    if(time_interval) {
        myTimerVal=setInterval(function(){myTimer()},time_interval);
    } 
}

/**
    Timer Function. Refreshes page
**/
function myTimer() {
    
    reload(); //refresh page
    
    // Update Refesh Time
    setTimeOnElem('refresh_time');
}

/**
    Set the Timer
    
    @param int interval - Interval for timer in milliseconds
**/
function setTimer(interval) {

    time_interval = interval;
    
    initTimer();  
}
  
/**
    Show Refresh time for timer
**/
function setTimeOnElem(elem) {

    var myelem = document.getElementById(elem);
    
    var now=new Date();
    var hour        = now.getHours();
    var minute      = now.getMinutes();
    var second      = now.getSeconds();
    //var monthnumber = now.getMonth();
    //var monthday    = now.getDate();
    //var year        = now.getYear();
    
    // Conver to AM,PM
    var ap = "AM";
    
    if (hour > 11) { 
        ap = "PM";   
    }
    
    if (hour > 12) { 
        hour = hour - 12; 
    }
    
    if (hour == 0) { 
        hour = 12;        
    }
    
    if (minute < 10) {
        minute = '0' + minute;
    }
    
    if (second < 10) {
        second = '0' + second;
    }

    myelem.innerHTML = hour + ':' + minute + ':' + second + ' ' + ap;
}

/**
    Appends the query to a search box.
    
    If a value is empty it adds the value, if it is not it appends the query using "||"
    
    @param string query - Query String
    @param string elem - Element ID
**/
function append_query(query, elem) {

    var element = document.getElementById(elem);
    
    if(element.value.length > 0) {
        element.value = element.value + '||' + query;
    } else {
        element.value = query;
    }

}

/**
    Export to Spreadsheet
    
    @param string mytype - cvs,tvs
**/
function export_to_spreadsheet(mytype) {
    
    if(mytype) {
        values = $('#fmFilter').serializeArray();
        values = jQuery.param(values);
        window.location = sitelink + "ajax?" + values + '&export_format=' + mytype
    }
    
    clear_input_dropdown('export', "");
}

/**
    Export to Spreadsheet
    
    @param string mytype - cvs,tvs
**/
function getChartUrl(chartcolumn) {
    
    if(chartcolumn) {
        values = $('#fmFilter').serializeArray();
        values = jQuery.param(values);
        
        return sitelink + "ajax?" + values + '&export_format=chart&chartcolumn=' + chartcolumn
               
    }
    
}

/**
    Not Implemented
**/


/**
    Submit Form
    
    Can't find way to submit form
**/
function formsubmit() {
    
    reload();
    
    return false;
}
