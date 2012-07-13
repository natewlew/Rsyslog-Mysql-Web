from django.db.models import Q
import operator

class queryHelper():

    list_ex = None
    list_in = None
    
    split_char = '||'
    exclude_char = '--'
    
    def __init__(self):
        self.list_ex = []
        self.list_in = []
        
    def setQueryList(self, param, column):
    
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
        
    def getReduceQuery(self, my_list):
    
        return_val = Q()

        if len(my_list) > 0:
            return_val = reduce(operator.or_, my_list)
        
        return return_val
        
    def get_list_ex(self):
     
        return self.getReduceQuery(self.list_ex)
        
    def get_list_in(self):
     
        return self.getReduceQuery(self.list_in)
        
class paramHelper():

    #def __init__(self):
        # Set defaults
        
    def getStringParam(self, params, param_name, default):
        
        try:
            default = params[param_name]
        except:
            pass
            
        return default
        
    def getIntParam(self, params, param_name, default):
	    
        try:
            default = int(params[param_name])
        except:
            pass
            
        return default
            
        
        
    
