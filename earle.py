import re
from django.conf import settings
from django.core.urlresolvers import RegexURLPattern
from types import defaults, RegexEarlePattern, RegexEarleResolver

re_template = r'<(?P<name>[a-zA-Z_][a-zA-Z_0-9]*):(?P<type>[a-z]+)>'
re_pattern = re.compile(re_template)

class Earle(object):

    def __init__(self):
        self.types = dict([(k, v) for k, v in defaults.iteritems()])
        custom_types = getattr(settings, 'REGEX_TYPES', False)
        if custom_types:
            self.types.update(custom_types)
        
    def patterns(self, prefix, *args):
        '''Replacement for django.conf.urls.defaults.patterns.'''
        pattern_list = []
        for t in args:
            if isinstance(t, (list, tuple)):
                t = self.url(prefix = prefix, *t)
            elif isinstance(t, (RegexEarlePattern, RegexURLPattern)):
                t.add_prefix(prefix)
            pattern_list.append(t)
        return pattern_list
        
    def url(self, regex, view, kwargs = None, name = None, prefix = ''):
        '''Replacement for django.conf.urls.defaults.url.'''
        regex, type_processors = self.replace_all(regex)
        regex = self.prepend_caret(regex)
        if isinstance(view, (list, tuple)):
            module, app_name, namespace = view
            return RegexEarleResolver(regex, type_processors, module, kwargs, app_name, namespace)
        else:
            regex = self.append_dollar(regex)
            if isinstance(view, basestring):
                if not view:
                    raise ImproperlyConfigured('Empty URL pattern view name not permitted (for pattern %r)' % regex)
                if prefix:
                    view = prefix + '.' + view
            return RegexEarlePattern(regex, type_processors, view, kwargs, name)
            
    def replace_all(self, regex):
        '''Replace all Earle groups with normal regex groups and extract any type processors.'''
        matches = re_pattern.finditer(regex)
        type_processors = {}
        for match in matches:
            group_name, group_type, group_type_processors = self.group(match)
            type_processors.update(group_type_processors)
            regex = self.replace_group(regex, group_name, group_type, match.span())
        return regex, type_processors
        
    def group(self, match):
        '''Extract group name, type, and type processors from a match.'''
        groups = match.groupdict()
        group_name = groups['name']
        group_type = self.types[groups['type']]
        type_processors = {}
        if isinstance(group_type, (list, tuple)):
            group_type, type_processor = group_type
            type_processors[group_name] = type_processor
        return group_name, group_type, type_processors
        
    def replace_group(self, regex, group_name, group_type, bounds):
        '''Replace Earle group with normal regex group.'''
        replacement = r'(?P<%s>%s)' % (group_name, group_type)
        start, end = bounds
        return regex[:start] + replacement + regex[end:]
            
    def append_dollar(self, regex):
        '''Append the regex with $ if not present.'''
        if not regex.endswith('$'):
            regex = regex + '$'
        return regex
            
    def prepend_caret(self, regex):
        '''Prepend the regex with ^ if not present.'''
        if not regex.startswith('^'):
            regex = '^' + regex
        return regex

earle = Earle()
patterns = earle.patterns
url = earle.url