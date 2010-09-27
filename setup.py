from setuptools import setup, find_packages

version = '0.1'

setup(
    name = 'earle',
    version = version,
    description = 'A URL pattern parser for Django',
    author = 'Scott Nelson',
    author_email = 'scottbnel@gmail.com',
    url = 'http://www.github.com/scottbnel/earle/',
    py_modules = ['earle'],
    requires = ['django'],
    zip_safe = True,
)
