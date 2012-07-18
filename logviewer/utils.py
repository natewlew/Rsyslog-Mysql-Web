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

from django.db.models import Q
import operator

class queryHelper():
    """
    Help Build the Query From the Params
    """

    list_ex = None
    list_in = None
    operator = None
    
    split_char = '||'
    exclude_char = '--'
    
    def __init__(self):
        """
        Init: Sets Defaults
        """
        self.list_ex = []
        self.list_in = []
        self.operator = "or"
        
    def setOperator(self, myoperator):
        self.operator = myoperator
        
    def setQueryList(self, param, column):
        """
        Set the Query List. Builds the list_ex and list_in
        """
        contains = '%s__icontains' % column
        
        split_params = param.split(self.split_char)

        for singleparam in split_params:

            if len(singleparam) > 0:
                if singleparam.startswith(self.exclude_char):
                    #not equal to
                    self.list_ex.append( Q(**{contains:singleparam[len(self.exclude_char):]} ) ) 
                else:
                    #equal to
                    self.list_in.append( Q(**{contains:singleparam} ) ) 
                    
    def setQueryDateRange(self, column, start, end):
        """
        Set the Date Range on a Column
        """        
        if len(start) > 0 and len(end) > 0:
            contains = '%s__range' % column
            self.list_in.append( Q(**{contains:[start, end]} ) )
        elif len(start) > 0 and len(end) == 0:
            contains = '%s__gte' % column
            self.list_in.append( Q(**{contains:start} ) )
        elif len(start) == 0 and len(end) > 0:
            contains = '%s__lte' % column
            self.list_in.append( Q(**{contains:end} ) )        
        
    def getReduceQuery(self, my_list):
        """
        Takes existing list query and sets the operator
        """
        return_val = Q()

        if len(my_list) > 0:
        
            if self.operator == "and": # operator is add
                return_val = reduce(operator.and_, my_list)
            else: # default, operator is or
                return_val = reduce(operator.or_, my_list)
        
        return return_val
        
    def get_list_ex(self):
     
        return self.getReduceQuery(self.list_ex)
        
    def get_list_in(self):
     
        return self.getReduceQuery(self.list_in)
            
        
        
    
