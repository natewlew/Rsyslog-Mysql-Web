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

from django.conf.urls import patterns, include, url
from django.conf import settings
import os

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'logviewer.views.index', name = 'logs'),
    #url(r'^logs/$', 'logviewer.views.logs', name = 'logs'),
    #url(r'^logs/ajax/$', 'logviewer.views.logsajax', name = 'logs_ajax'),
    #url(r'^logs/dojo/$', 'logviewer.views.logsdojo', name = 'logs_dojo'), # Examples:
    # url(r'^$', 'rsyslog_mysql_web.views.home', name='home'),
    # url(r'^rsyslog_mysql_web/', include('rsyslog_mysql_web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

#static files in debug mode(e.g css)
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'site_media').replace('\\','/')}),    )
