from django.core.urlresolvers import RegexURLPattern, RegexURLResolver

defaults = {
    'alpha': '[a-zA-Z]+',
    'alphanumeric': '[a-zA-Z0-9]+',
    'any': '[^/]+',
    'float': ('\d*\.?\d+', lambda x: float(x)),
    'int': ('\d+', lambda x: int(x)),
}

class TypeProcessor(object):

    def process(self, callback, args, kwargs):
        '''Run any type processors on kwargs.'''
        for name, value in kwargs.iteritems():
            if name in self.type_processors:
                kwargs[name] = self.type_processors[name](value)
        return callback, args, kwargs

class RegexEarlePattern(RegexURLPattern, TypeProcessor):
    
    def __init__(self, regex, type_processors, callback, default_args = None, name = None):
        super(RegexEarlePattern, self).__init__(regex, callback, default_args = default_args, name = name)
        self.type_processors = type_processors
    
    def resolve(self, path):
        values = super(RegexEarlePattern, self).resolve(path)
        if values:
            return self.process(*values)

        
class RegexEarleResolver(RegexURLResolver, TypeProcessor):
    
    def __init__(self, regex, type_processors, module, kwargs, app_name, namespace):
        super(RegexEarleResolver, self).__init__(regex, module, kwargs, app_name, namespace)
        self.type_processors = type_processors
    
    def resolve(self, path):
        values = super(RegexEarleResolver, self).resolve(path)
        if values:
            return self.process(*values)