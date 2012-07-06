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

import os
import sys

# Python Paths
sys.path.append('/opt/python/rsyslog_mysql_web')
#sys.path.append('/opt/python/rsyslog_mysql_web/logviewer')
#sys.path.append('/opt/python/rsyslog_mysql_web/rsyslog_mysql_web')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rsyslog_mysql_web.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
