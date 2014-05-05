#!/usr/bin/env python
#
#   Copyright (c) 2014 Hamilton Kibbe <ham@hamiltonkib.be>
#
#   Permission is hereby granted, free of charge, to any person obtaining a 
#   copy of this software and associated documentation files (the "Software"), 
#   to deal in the Software without restriction, including without limitation 
#   the rights to use, copy, modify, merge, publish, distribute, sublicense, 
#   and/or sell copies of the Software, and to permit persons to whom the 
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included 
#   in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
#   OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
#   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.


'''The setup and build script for the PyAbleton library.'''

__author__ = 'Hamilton Kibbe <ham@hamiltonkib.be>'
__version__ = '1.0'




METADATA = {
    'name': 'pyableton',
    'version': __version__,
    'url': 'https://github.com/hamiltonkibbe/PyAbleton',
    'packages': ['pyableton'],
    'package_data': {'presets': ['presets/res/*']},
    'author': 'Hamilton Kibbe',
    'author_email': 'ham@hamiltonkib.be',
    'description': 'A library for creating/editing Ableton Live presets',
    'license': 'MIT License'
    }

SETUPTOOLS_METADATA = {
    'install_requires':['setuptools','bs4'],
    'include_package_data': True
    }

def install():
    ''' Install using setuptools, fallback to distutils
    '''
    try:
        from setuptools import setup
        METADATA.update(SETUPTOOLS_METADATA)
        setup(**METADATA)
    except ImportError:
        from sys import stderr
        stderr.write("Could not import setuptools, using distutils")
        stderr.write("NOTE: You will need to install dependencies manualy")
        from distutils.core import setup
        setup(**METADATA)

if __name__ == '__main__':
    install()

