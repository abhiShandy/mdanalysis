# $Id$
"""Distutils based setup script for MDAnalysis.

This uses Distutils (http://python.org/sigs/distutils-sig/) the standard
python mechanism for installing packages. For the easiest installation
just type the command:

  python setup.py install

For more in-depth instructions, see the installation section at the
MDAnalysis Wiki:

  http://code.google.com/p/mdanalysis/wiki/Install

Or for more details about the options available from distutils, look at
the 'Installing Python Modules' distutils documentation, available from:

  http://python.org/sigs/distutils-sig/doc/

Or, if all else fails, feel free to ask on the MDAnalysis mailing list
for help:

  http://groups.google.com/group/mdnalysis-discussion

(Note that the group really is called `mdnalysis-discussion' because
Google groups forbids any name that contains the string `anal'.)
"""
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

import sys, os
import glob

# Make sure I have the right Python version.
if sys.version_info[:2] < (2, 3):
    print "MDAnalysis requires Python 2.3 or better.  Python %d.%d detected" % \
        sys.version_info[:2]
    sys.exit(-1)

from distutils import sysconfig
from numpy import get_numpy_include
from distutils.core import setup, Extension
from Pyrex.Distutils import build_ext

include_dirs = [get_numpy_include()]

if sys.platform == "darwin": # Mac OS X
    fast_numeric_include = ['/System/Library/Frameworks/vecLib.framework/Versions/A/Headers']
    fast_numeric_link = ["-framework","vecLib"]
elif sys.platform[:5] == "linux":
    fast_numeric_include = ['/opt/intel/cmkl/10.0.5.025/include']
    fast_numeric_link = ["-L/opt/intel/cmkl/10.0.5.025/lib/em64t", "-lmkl_lapack","-lmkl","-lguide"]
else:
    fast_numeric_include = []
    fast_numeric_link = []

if __name__ == '__main__':
    # for main trunk:
    ## RELEASE = "0.6.0"
    # for UNSTABLE:
    RELEASE = "0.6.0-rc2"
    ##RELEASE = "svn149_UNSTABLE"   # submitted svn revision:  echo $(($(svnversion | tr --delete '[a-zA-Z]') + 1))

    ## currently not installing doc files because data_files appears to be broken
    ## (does not create the full directory; in any case this implemetation is not very
    ## customizable and it's also not clear to me where python docs should go)
    # DOC_FILES = ['README', 'LICENSE', 'CHANGELOG', 'TODO'] + glob.glob('doc/*')
    # doc_install_dir = os.path.join('share','doc','MDAnalysis') # assumes that docs are in <install_data>/share/doc/MDAnalysis
    
    LONG_DESCRIPTION = \
"""MDAnalysis is a tool for analyzing molecular dynamics trajectories.
"""
    CLASSIFIERS = ['Development Status :: 1 - Alpha',
                   'Environment :: Workstation',
                   'Intended Audience :: Scientists',
                   'License :: OSI Approved :: GPL License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Scientific Software :: Biology',
                   'Topic :: Scientific Software :: Chemistry',]

    if 'DEBUG_CFLAGS' in os.environ:
        extra_compile_args = '\
            -std=c99 -pedantic -Wall -Wcast-align -Wcast-qual -Wpointer-arith \
            -Wchar-subscripts -Winline -Wnested-externs -Wbad-function-cast \
            -Wunreachable-code -Werror'
        define_macros = [('DEBUG', '1')]
    else:
        extra_compile_args = ''
        define_macros = []

    extensions = [Extension('coordinates._dcdmodule', ['src/dcd/dcd.c'],
                            include_dirs = include_dirs+['src/dcd/include'],
                            define_macros=define_macros,
                            extra_compile_args=extra_compile_args),
                  Extension('coordinates._dcdtest', ['src/dcd/_dcdtest.pyx'],
                            include_dirs = include_dirs+['src/dcd/include'],
                            define_macros=define_macros,
                            extra_compile_args=extra_compile_args),
                  Extension('core.distances', ['src/numtools/distances.pyx'],
                            include_dirs = include_dirs+['src/numtools'],
                            libraries = ['m'],
                            define_macros=define_macros,
                            extra_compile_args=extra_compile_args),
                  Extension('core.rms_fitting', ['src/numtools/rms_fitting.pyx'],
                            libraries = ['m'],
                            define_macros=define_macros,
                            include_dirs = include_dirs+fast_numeric_include,
                            extra_link_args=fast_numeric_link,
                            extra_compile_args=extra_compile_args),
                  #Extension('util.delaunay', ['src/delaunay/delaunay.pyx', 'src/delaunay/blas.c', 'src/delaunay/tess.c'],
                  #          libraries = ['m'],
                  #          define_macros=define_macros,
                  #          include_dirs = include_dirs+fast_numeric_include+['src/delaunay'],
                  #          extra_link_args=fast_numeric_link,
                  #          extra_compile_args=extra_compile_args),
                  Extension('KDTree._CKDTree', 
                            ["src/KDTree/KDTree.cpp",
                             "src/KDTree/KDTree.swig.cpp"],
                            include_dirs = include_dirs,
                            libraries=["stdc++"],
                            language="c++"),
                  ]

    setup(name              = 'MDAnalysis',
          version           = RELEASE,
          description       = 'Python tools to support analysis of trajectories',
          author            = 'Naveen Michaud-Agrawal',
          author_email      = 'naveen.michaudagrawal@gmail.com',
          url               = 'http://mdanalysis.googlecode.com/',
          license           = 'GPL 2',
          packages          = [ 'MDAnalysis',
                                'MDAnalysis.core', 'MDAnalysis.topology',
                                'MDAnalysis.coordinates', 'MDAnalysis.util',
                                'MDAnalysis.KDTree'],
          package_dir       = {'MDAnalysis': 'MDAnalysis'},
          ext_package       = 'MDAnalysis',
          ext_modules       = extensions,
        # data_files        = [ (doc_install_dir, DOC_FILES) ],  ## see comments for DOC_FILES
          classifiers       = CLASSIFIERS,
          long_description  = LONG_DESCRIPTION,
          cmdclass = {'build_ext': build_ext}
          )
