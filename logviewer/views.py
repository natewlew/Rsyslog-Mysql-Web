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
from django.template import RequestContext

from datetime import datetime
from django.shortcuts import redirect

from django.utils.translation import ugettext as _
from datable.web.columns import HrefColumn
from datable.web.columns import ImageColumn

from datable.core.serializers import HrefSerializer
from datable.core.serializers import URLSerializer

from django.db.models import Q

from datable.web.table import Table
from datable.web.storage import Storage

from datable.core.converters import IntegerConverter
from datable.web.widgets import Maximum, Minimum
from datable.web.widgets import Constraints
from datable.web.widgets import Widget
from datable.web.widgets import StringWidget
from datable.web.widgets import BooleanWidget
from datable.web.widgets import DateWidget
from datable.web.widgets import DateTimeWidget

from datable.core.serializers import UnicodeSerializer
from datable.core.serializers import FormatStringSerializer
from datable.core.filters import IntegerFilter

from datable.web.extra.widgets import AutocompleteStringWidget
from datable.web.extra.widgets import DateTimeLessOrEqual
from datable.web.extra.widgets import ForeignKeyComboBox
from datable.web.extra.widgets import DateTimeGreaterOrEqual
from datable.web.extra.widgets import PeriodicRefreshWidget
from datable.core.converters import DojoComboValueConverter
from datable.core.filters import StringFilter

from datable.web.columns import Column
from datable.web.columns import StringColumn
from datable.web.columns import DateColumn
from datable.web.columns import BooleanColumn
from datable.web.columns import DateTimeColumn
from datable.core.serializers import ForeignKeySerializer
from datable.core.serializers import StringSerializer

template="logviewer"

def index(request):

    first_table = Table(
        name='first_table',

        storage=Storage(
            querySet=Systemevents.objects.all().order_by('-id'),
            columns=[
                StringColumn('id', width=100),
                DateTimeColumn('devicereportedtime', width=150),
                StringColumn('facility', width=150),
                StringColumn('priority', width=100),
                StringColumn('fromhost', width=150),
                StringColumn('syslogtag', width=200),
                StringColumn('message', width=700),
                ],
            widgets=[
                StringWidget('fromhost', placeholder=_("From Host")),
                StringWidget('syslogtag', placeholder=_("Tag")),
                StringWidget('message', placeholder=_("Message")),
                DateTimeLessOrEqual('devicereportedtime', paired=True, placeholder=_("Reported Time - Max")),
                DateTimeGreaterOrEqual('devicereportedtime', paired=True, placeholder=_("Reported Time - Min")),
                ForeignKeyComboBox(
                    'facility', otherSet=Facilities.objects.all(), otherField='id',
                    otherFormat='Facility: %(facility)s',
                    placeholder=_("Facility")),
                ForeignKeyComboBox(
                    'priority', otherSet=Priorites.objects.all(), otherField='num',
                    otherFormat='Priority: %(severity)s',
                    placeholder=_("Priority")),
                    
                PeriodicRefreshWidget('periodic', filterField='published_on')


            ]
            ),
        filename=_("My important export data %Y-%m-%d")
        )

    if first_table.willHandle(request):
        return first_table.handleRequest(request)

    return render_to_response(
        template + '/index.html', {'first_table': first_table})
