#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     pagebot/__init__.py
#
import re

VERSION = '0.6'
STATUS = 'alpha'
__doc__ = """PageBot module"""
__version__ = '%s-%s' % (VERSION, STATUS)
ROOT_PATH = '/'.join(__file__.split('/')[:-1])
RESOURCES_PATH = ROOT_PATH + '/resources'

def getRootPath():
    """Answer the root path on the platform for the PageBot module."""
    return ROOT_PATH

def getResourcesPath():
    """Answer the root path on the platform for the PageBot module."""
    return RESOURCES_PATH

def getContext(contextType='DrawBot'):
    """
    >>> context = getContext()
    >>> print(context)
    <DrawBotContext>
    >>> context = getContext('DrawBot')
    >>> print(context)
    <DrawBotContext>
    >>> context = getContext('Flat')
    >>> print(context)
    <FlatContext>
    >>> context = getContext('HTML')
    >>> print(context)
    <HtmlContext>
    """
    from pagebot.contexts.platform import getContext as getPlatformContext
    return getPlatformContext(contextType=contextType)

# In order to let PageBot scripts and/applications exchange information
# without the need to save data in files, the pbglobals module supports the
# storage of non-persistent information. This way, applications with Vanilla
# windows can be used as UI for scripts that perform as batch process.

# Note that it is the responsibilty of individual scripts to create unique ids
# for attributes. Also they need to know of each other, in case information is
# exchanged.
#
# Key is script/application id, e.g. their __file__ value.
#
# Access as:
#
#   from pagebot.toolbox.transformer import path2ScriptId
#   scriptGlobals = pagebot.getGlobals(path2ScriptId(__file__))
#
# or direct as:
#
# ...

pbGlobals = {}

class Globals:
    # Allow adding by attribute and key.
    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

def getGlobals(scriptId):
    """In order to let PageBot scripts and/applications exchange information,
    without the need to save as files, the pbglobals module supports the
    storage of non-persistent information. This way, applications with Vanilla
    windows can be used as UI for scripts that perform as batch process.  Note
    that it is up to the responsibilty of individual scripts to create uniqued
    ids for attributes. Also they need to know from each other, in case
    information is exchanged."""
    if not scriptId in pbGlobals:
        pbGlobals[scriptId] = Globals()
    return pbGlobals[scriptId]

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
