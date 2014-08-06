"""
This module should contain python files with Jinja filters and methods
that can be used when rendering Dockerfiles with dj.

All methods will be auto registered by the core application.

All filters should have their method name start with _filter_ to auto load by ed

All global functions should have their method name start with _func_ to auto load by ed
"""
from . import basic
from . import file
