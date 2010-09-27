import re

from django.conf import settings
from django.conf.urls.defaults import url
from django.core.urlresolvers import RegexURLPattern

re_template = r'<(?P<name>[a-zA-Z_][a-zA-Z_0-9]*):(?P<type>[a-z]+)>'
re_pattern = re.compile(re_template)

default_types = {
    'alpha': '[a-zA-Z]+',
    'alphanumeric': '[a-zA-Z0-9]+',
    'any': '[^/]+',
    'float': '\d*\.?\d+',
    'int': '\d+',
}

class Earle(object):
    
    def __init__(self):
        self.types = dict([(k, v) for k, v in default_types.iteritems()])
        custom_types = getattr(settings, 'REGEX_TYPES', False)
        if custom_types:
            self.types.update(custom_types)
        
    def patterns(self, prefix, *args):
        '''Replacement for django.conf.urls.defaults.patterns.'''
        pattern_list = []
        for t in args:
            if isinstance(t, (list, tuple)):
                t = self.url(prefix = prefix, *t)
            elif isinstance(t, RegexURLPattern):
                t.add_prefix(prefix)
            pattern_list.append(t)
        return pattern_list
    
    def url(self, regex, view, kwargs = None, name = None, prefix = ''):
        '''Replacement for django.conf.urls.defaults.url.'''
        regex = self.replace(regex)
        regex = self.prepend(regex)
        if not isinstance(view, (tuple, list)):
            regex = self.append(regex)
        return url(regex, view, kwargs, name, prefix)
            
    def replace(self, regex):
        '''Replace Earle groups with normal regex groups.'''
        matches = re_pattern.finditer(regex)
        for match in matches:
            groups = match.groupdict()
            replacement = r'(?P<%s>%s)' % (groups['name'], self.types[groups['type']])
            start, end = match.span()
            regex = regex[:start] + replacement + regex[end:]
        return regex
            
    def append(self, regex):
        '''Append the regex with $ if not present.'''
        if not regex.endswith('$'):
            regex = regex + '$'
        return regex
            
    def prepend(self, regex):
        '''Prepend the regex with ^ if not present.'''
        if not regex.startswith('^'):
            regex = '^' + regex
        return regex

patterns = Earle().patterns