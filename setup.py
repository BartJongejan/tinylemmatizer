# setup.py - builds the C extension. Project metadata is in pyproject.toml.
#
import sysconfig
from setuptools import setup
from Cython.Build import cythonize
from setuptools.extension import Extension

# Build one wheel per platform that works for every CPython version >= 3.9 (abi3).
# Free-threaded CPython (e.g. 3.14t) does not support abi3, so there we do a normal build.
limited_api = not sysconfig.get_config_var("Py_GIL_DISABLED")

sourcefiles = ['cstlempy.pyx', 'tinylemmatizer.c']
macros = [("_CRT_SECURE_NO_WARNINGS", None), ("PYTHONINTERFACE", None)]
if limited_api:
    macros.append(("Py_LIMITED_API", "0x03090000"))

extensions = [Extension("cstlempy", sourcefiles,
                        include_dirs=["."],
                        depends=["tinylemmatizer.h"],
                        define_macros=macros,
                        py_limited_api=limited_api)]

setup(
    ext_modules = cythonize(extensions, emit_linenums=True,
                            compiler_directives={'language_level': 3, 'embedsignature': True,
                                                 'freethreading_compatible': True}),
    options = {"bdist_wheel": {"py_limited_api": "cp39"}} if limited_api else {},
)
