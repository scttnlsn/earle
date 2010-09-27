earle
======

Earle is a URL pattern parser for Django.  It is a drop-in replacement for
Django's existsing patterns() function, but also allows URL patterns to be
specified more concisely.

Example
-------

    patterns(
        ('^hello/(?P<firstname>[a-zA-Z]+)/(?P<lastname>[a-zA-Z]+)/$', 'views.hello'),
        ('^example/', include('example.urls')),
    )
    
can be written

    earle.patterns(
        ('hello/<firstname:alpha>/<lastname:alpha>/', 'views.hello'),
        ('example/', include('example.urls')),
    )

Usage
-----

    '<name:type>'

becomes

    '(?P<name>%s)' % types['type']

The `types` dictionary is populated from a set of pre-defined regex patterns
(refer to the top of `earle.py`) and any patterns you define yourself.  To
add custom patterns, create a dictionary named REGEX_TYPES in `settings.py`.

For example, with `REGEX_TYPES` defined like

    REGEX_TYPES = {
        'ymd': r'\d{4}\-\d{2}\-\d{2}',
    }

one could write

    earle.patterns(
        ('posts/<date:ymd>/'),
    )

instead of

    patterns(
        ('^posts/(?P<date>\d{4}\-\d{2}\-\d{2})/$'),
    )

Note that the leading `^` and trailing `$` do not need to be explicitly written
as they are automatically added where appropriate.