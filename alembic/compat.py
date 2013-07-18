import sys
import os

if sys.version_info < (2, 6):
    raise NotImplementedError("Python 2.6 or greater is required.")

py3k = sys.version_info >= (3, 0)
py33 = sys.version_info >= (3, 3)

if py3k:
    import builtins as compat_builtins
    string_types = str,
    binary_type = bytes
    text_type = str
    def callable(fn):
        return hasattr(fn, '__call__')
else:
    import __builtin__ as compat_builtins
    string_types = basestring,
    binary_type = str
    text_type = unicode
    callable = callable

if py3k:
    from configparser import ConfigParser as SafeConfigParser
    import configparser
else:
    from ConfigParser import SafeConfigParser
    import ConfigParser as configparser

if py33:
    from importlib import machinery
    def load_module(module_id, path):
        return machinery.SourceFileLoader(module_id, path).load_module()
else:
    import imp
    def load_module(module_id, path):
        #if both pyc and py files exist, load the py file
        #otherwise load the appropriate file

        #does our file exist?
        if os.path.exists(path):
            #do both .py and .pyc exist? pick up .py then
            if path.endswith('.pyc') and os.path.exists(path[:-1]):
                    path = path[:-1]
        else:
            #file doesn't exist, but does .pyc exist?
            if os.path.exists(path+'c'):
                path = path + 'c'
        fp = open(path, 'rb')
        try:
            #pyc and py use different load methods
            if path.endswith('.pyc'):
                module = imp.load_compiled(module_id, path, open(path, 'rb'))
            else:
                module = imp.load_source(module_id, path, open(path, 'rb'))

            return module
        finally:
            fp.close()


try:
    exec_ = getattr(compat_builtins, 'exec')
except AttributeError:
    # Python 2
    def exec_(func_text, globals_, lcl):
        exec('exec func_text in globals_, lcl')

################################################
# cross-compatible metaclass implementation
# Copyright (c) 2010-2012 Benjamin Peterson
def with_metaclass(meta, base=object):
    """Create a base class with a metaclass."""
    return meta("%sBase" % meta.__name__, (base,), {})
################################################
