"""Tools to assist importing optional external modules."""

import sys
import types

# Override these in the module to change the default warning behavior.
# For example, you might set both to False before running the tests so that
# warnings are not printed to the console, or set both to True for debugging.

WARN_NOT_INSTALLED = None # Default is False
WARN_OLD_VERSION = None # Default is True

def __sympy_debug():
    # helper function from sympy/__init__.py
    # We don't just import SYMPY_DEBUG from that file because we don't want to
    # import all of sympy just to use this module.
    import os
    return eval(os.getenv('SYMPY_DEBUG', 'False'))

if __sympy_debug():
    WARN_OLD_VERSION = True
    WARN_NOT_INSTALLED = True

def import_module(module, min_module_version=None, min_python_version=None,
        warn_not_installed=None, warn_old_version=None,
        module_version_attr='__version__', module_version_attr_call_args=None,
        __import__kwargs={}, catch=(), lazy=True):
    """
    Import and return a module if it is installed.

    If the module is not installed, the boolean value of the returned object
    will be False.

    A minimum version for the module can be given as the keyword argument
    min_module_version.  This should be comparable against the module version.
    By default, module.__version__ is used to get the module version.  To
    override this, set the module_version_attr keyword argument.  If the
    attribute of the module to get the version should be called (e.g.,
    module.version()), then set module_version_attr_call_args to the args such
    that module.module_version_attr(*module_version_attr_call_args) returns the
    module's version.

    If the module version is less than min_module_version using the Python <
    comparison, None will be returned, even if the module is installed. You can
    use this to keep from importing an incompatible older version of a module.

    You can also specify a minimum Python version by using the
    min_python_version keyword argument.  This should be comparable against
    sys.version_info.

    If the keyword argument warn_not_installed is set to True, the function will
    emit a UserWarning when the module is not installed.

    If the keyword argument warn_old_version is set to True, the function will
    emit a UserWarning when the library is installed, but cannot be imported
    because of the min_module_version or min_python_version options.

    Note that because of the way warnings are handled, a warning will be
    emitted for each module only once.  You can change the default warning
    behavior by overriding the values of WARN_NOT_INSTALLED and WARN_OLD_VERSION
    in sympy.external.importtools.  By default, WARN_NOT_INSTALLED is False and
    WARN_OLD_VERSION is True.

    This function uses __import__() to import the module.  To pass additional
    options to __import__(), use the __import__kwargs keyword argument.  For
    example, to import a submodule A.B, you must pass a nonempty fromlist option
    to __import__.  See the docstring of __import__().

    This catches ImportError to determine if the module is not installed.  To
    catch additional errors, pass them as a tuple to the catch keyword
    argument.

    Note, by default, import_module does not actually return the module to be
    imported, but a lazy object that acts just like the module, except that it
    doesn't actually import the module until it is used.  This can be used to
    defer the import of module so that it is not imported when sympy is
    imported, which can slow down the time of "import sympy" if the external
    module is installed.  Be aware though that the module will be imported as
    soon as the object returned by import_module is used in any way.  You can
    check if a module has been imported by seeing if it is in sys.modules.
    This behavior can be disabled by setting lazy=False.

    Examples
    ========

    >>> from sympy.external import import_module

    >>> numpy = import_module('numpy')

    >>> numpy = import_module('numpy', min_python_version=(2, 6),
    ... warn_old_version=False)

    >>> numpy = import_module('numpy', min_module_version='1.5',
    ... warn_old_version=False) # numpy.__version__ is a string

    >>> # gmpy does not have __version__, but it does have gmpy.version()

    >>> gmpy = import_module('gmpy', min_module_version='1.14',
    ... module_version_attr='version', module_version_attr_call_args=(),
    ... warn_old_version=False)

    >>> # To import a submodule, you must pass a nonempty fromlist to
    >>> # __import__().  The values do not matter.
    >>> p3 = import_module('mpl_toolkits.mplot3d',
    ... __import__kwargs={'fromlist':['something']})

    >>> # matplotlib.pyplot can raise RuntimeError when the display cannot be opened
    >>> matplotlib = import_module('matplotlib',
    ... __import__kwargs={'fromlist':['pyplot']}, catch=(RuntimeError,))

    >>> dne = import_module("doesnotexist")
    >>> dne
    DeferredImport('doesnotexist')
    >>> bool(dne)
    False

    """
    if lazy:
        return DeferredImport(module, min_module_version=min_python_version,
            min_python_version=min_python_version,
            warn_not_installed=warn_not_installed,
            warn_old_version=warn_old_version,
            module_version_attr=module_version_attr,
            module_version_attr_call_args=module_version_attr_call_args,
            __import__kwargs=__import__kwargs, catch=catch)

    # keyword argument overrides default, and global variable overrides
    # keyword argument.
    warn_old_version = (WARN_OLD_VERSION if WARN_OLD_VERSION is not None
        else warn_old_version or True)
    warn_not_installed = (WARN_NOT_INSTALLED if WARN_NOT_INSTALLED is not None
        else warn_not_installed or False)

    import warnings

    # Check Python first so we don't waste time importing a module we can't use
    if min_python_version:
        if sys.version_info < min_python_version:
            if warn_old_version:
                warnings.warn("Python version is too old to use %s "
                    "(%s or newer required)" % (module, '.'.join(map(str, min_python_version))),
                    UserWarning)
            return

    # PyPy 1.6 has rudimentary NumPy support and importing it produces errors, so skip it
    if module == 'numpy' and '__pypy__' in sys.builtin_module_names:
        return

    try:
        mod = __import__(module, **__import__kwargs)
    except ImportError:
        if warn_not_installed:
            warnings.warn("%s module is not installed" % module, UserWarning)
        return
    # TODO: After 2.5 is dropped, use new 'as' keyword
    #except catch as e:
    except catch, e:
        if warn_not_installed:
            warnings.warn("%s module could not be used (%s)" % (module, repr(e)))
        return

    if min_module_version:
        modversion = getattr(mod, module_version_attr)
        if module_version_attr_call_args is not None:
            modversion = modversion(*module_version_attr_call_args)
        if modversion < min_module_version:
            if warn_old_version:
                # Attempt to create a pretty string version of the version
                if isinstance(min_module_version, basestring):
                    verstr = min_module_version
                elif isinstance(min_module_version, (tuple, list)):
                    verstr = '.'.join(map(str, min_module_version))
                else:
                    # Either don't know what this is.  Hopefully
                    # it's something that has a nice str version, like an int.
                    verstr = str(min_module_version)
                warnings.warn("%s version is too old to use "
                    "(%s or newer required)" % (module, verstr),
                    UserWarning)
            return

    return mod

class DeferredImport(types.ModuleType):
    """
    An object that pretends it is an imported module, but doesn't actually
    import the module until it is used.

    See also the docstring of import_module.

    At least two cases where this will work different from an actual import:

    - The code checks if the module is in sys.modules

    - The code compares the object against the real module using "is"
      comparison (__eq__ is implemented).

    """
    def __init__(self, name, *args, **kwargs):
        # Note, all names begin with double underscores so that Python will
        # use name mangling, preventing any possible name conflicts
        self.__name = name
        self.__args = args
        self.__kwargs = kwargs
        self.__kwargs['lazy'] = False

    @property
    def __module(self):
        return import_module(self.__name, *self.__args, **self.__kwargs)

    def __getattr__(self, attr):
        return getattr(self.__module, attr)

    def __nonzero__(self):
        return bool(self.__module)

    # XXX: Do we need this one?
    def __getitem__(self, key):
        return self.__module[key]

    def __repr__(self):
        return "DeferredImport(%s)" % repr(self.__name)

    @property
    def __dict__(self):
        return self.__module.__dict__

    def __eq__(self, other):
        return self is other or self.__module is other

    def __hash__(self):
        return hash(self.__module)
