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

Basic Usage
-----------

    '<name:type>'

becomes

    '(?P<name>%s)' % types['type']

The `types` dictionary is populated from a set of pre-defined regex patterns
(refer to the `defaults` dict at the top of `types.py`) and any patterns you
define yourself.  To add custom patterns, create a dictionary named `REGEX_TYPES`
in `settings.py`.

For example, with `REGEX_TYPES` defined like:

    REGEX_TYPES = {
        'ymd': r'\d{4}\-\d{2}\-\d{2}',
    }

...one could write...

    earle.patterns(
        ('posts/<date:ymd>/'),
    )

...instead of...

    patterns(
        ('^posts/(?P<date>\d{4}\-\d{2}\-\d{2})/$'),
    )

Note that the leading `^` and trailing `$` do not need to be explicitly written
as they are automatically added where appropriate.

Type Processors
---------------

You can also preprocess the captured group values before they reach your views.
For example, consider the `defaults` dict of pre-defined patterns- the `int`
entry is defined as `'int': ('\d+', lambda x: int(x))`.  You can optionally
specify a function that is called on the captured value.

Returning to our example above, it may be useful then to define a type processor
like so:

    import datetime
    
    def to_date(ymd):
        year, month, day = ymd.split('-')
        return datetime.date(int(year), int(month), int(day))
    
    REGEX_TYPES = {
        'ymd': (r'\d{4}\-\d{2}\-\d{2}', to_date),
    }

Your view will then receive a `datetime.date` object instead of a string.