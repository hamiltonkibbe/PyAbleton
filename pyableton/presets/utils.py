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

"""Utilities functions for handling ableton presets
"""
import __builtin__
import gzip
import os
from bs4 import BeautifulSoup

class AbletonParameter(object):
    """ A simple parameter wrapping class storing the XML element name, min/max values, and
    semantic data for enum parameters
    """
    def __init__(self, name=None, type=None, min=None, max=None, dict=None, converter=None):
        self.name = name
        self.type = type
        self.min = min
        self.max = max
        self.dict = dict
        self.converter = converter
        
        # Automatically calculate min and max for enum parameters
        if self.dict is not None:
            self.min = self.min if self.min is not None else __builtin__.min(self.dict.itervalues())
            self.max = self.max if self.max is not None else __builtin__.max(self.dict.itervalues())

    # Allow dict-style semantics
    def __getitem__(self, key):
        return self.__dict__[key]
        
    def __setitem__(self, key, value):
        self.__dict__[key] = value
        
def preset2xml(filename, create_file=False):
    """ Convert an Ableton Preset to xml format. if `create_file` is True,
    write the xml data to filename.xml
    """
    with gzip.open(filename, 'rb') as f:
        xml = f.read()
        if create_file:
            with open(os.path.splitext(filename)[0] + '.xml','w') as out:
                out.write(xml)
    return xml

def xml2preset(filename):
    """ Convert an Ableton Preset in xml format to an Ableton Preset file.
    """
    with open(filename) as f:
        with gzip.open(os.path.splitext(filename)[0] + '.adv', 'wb') as out:
            out.writelines(f)

    

def get_value(parameter, parent):
    """ Get the value of the passed parameter with the given parent
    """
    val = getattr(parent, parameter.name).ArrangerAutomation.Events.contents[1]['Value']
    eventname = getattr(parent, parameter.name).ArrangerAutomation.Events.contents[1].name
    if 'BoolEvent' in eventname:
        return (string2bool(val))
    elif 'EnumEvent' in eventname:
        # Try to get the human-readable description from the dict, but fall
        # back to returning just the int value
        if parent is not None and parameter.type == 'enum':
            for key, value in parameter.dict.iteritems():
                if value == int(val):
                    return key
        else:
            return int(val)  
    elif 'FloatEvent' in eventname:
        return float(val)


def set_value(parameter, value, parent):
    """ Set the value of the parameter with the given parent to "value"
    do bounds checking and clamp values to usable range.
    """
    if parameter.type is 'bool':
        to_write = u'true' if value else u'false'
    elif parameter.type is 'int':
        to_write = u'%d' % clamp(value)
    elif parameter.type is 'float':
        to_write = u'%f' % clamp(value)
    elif parameter.type is 'enum':
        for key, val in parameter.dict.iteritems():
            if key == value.upper():
                value = val
                break
        to_write = u'%d' % value
    getattr(parent,parameter.name).ArrangerAutomation.Events.contents[1]['Value'] = to_write
    
    
def clamp(value, parameter):
        """ Clamp value to parameter's min and max values
        """
        value = parameter.min if value < parameter.min else value
        value = parameter.max if value > parameter.max else value
        return value
    

def string2bool(string):
    return 'true' in string