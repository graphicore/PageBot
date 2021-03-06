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
#     composer.py
#
from pagebot.elements import newTextBox
from pagebot.elements import CodeBlock

class Composer:
    u"""A Composer takes a artDirection and tries to make pagination from given context,
    a “nice” layout (on existing or new document pages), by taking the elements from
    the galley pasteboard and finding the best place in pages, e.g. in page-flows that
    are copied from their templates.
    If necessary elements can be split, new elements can be made on the page and element can be
    reshaped byt width and height, if that results in better placements.

    >>> from pagebot import getResourcesPath
    >>> from pagebot.constants import A4
    >>> from pagebot.toolbox.units import em, pt
    >>> from pagebot.toolbox.color import color, blackColor
    >>> from pagebot.elements import TextBox
    >>> from pagebot.typesetter import Typesetter
    >>> from pagebot.document import Document
    >>> numPages = 4
    >>> path = getResourcesPath() + '/texts/TEST.md' # Get the path to the text markdown.
    >>> h1Style = dict(font='Verdana', fontSize=pt(36), textFill=color(1, 0, 0))
    >>> h2Style = dict(font='Georgia', fontSize=pt(18), textFill=color(1, 0, 0.5))
    >>> pStyle = dict(font='Verdana', fontSize=pt(10), leading=em(1.4), textFill=blackColor)
    >>> styles = dict(h1=h1Style, h2=h2Style, p=pStyle)
    >>> doc = Document(size=A4, styles=styles, autoPages=numPages, originTop=True)
    >>> t = Typesetter(doc.context, styles=styles)
    >>> # Create a "main" textbox in each page.
    >>> a = [TextBox(parent=doc[n], name='main', x=100, y=100, w=400, h=500) for n in range(1, numPages+1)] 
    >>> galley = t.typesetFile(path)
    >>> c = Composer(doc)
    >>> targets = c.compose(galley)
    >>> targets['errors']
    []
    >>> page = doc[1]
    >>> box = page.select('main') # Get the box of this page.
    >>> box
    TextBox:main ([100pt, 100pt], [400pt, 500pt]) S(1157)
    >>> doc.export('_export/ComposerTest.pdf')

    """
    def __init__(self, doc):
        self.doc = doc

    def compose(self, galley, targets=None, page=None):
        u"""Compose the galley element, based on code blocks in the gally.
        Later we'll add more art-direction instructions here.
        Targets contains the resources for the composition, such as the doc, current page, current box and other 
        info that the MarkDown assumes to be available. If targets is omitted, then it is created by the Composer
        and answered at the end.
        """
        if targets is None:
            if page is None:
                page = self.doc[1]
            targets = dict(composer=self, doc=self.doc, page=page, style=self.doc.styles, box=page.select('main'), newTextBox=newTextBox)  
        elif page is not None:
            targets['page'] = page

        if 'errors' not in targets:
            targets['errors'] = []
        errors = targets['errors']

        for e in galley.elements:
            if isinstance(e, CodeBlock): # Code can select a new page/box and execute other Python statements.
                e.run(targets)
            elif targets.get('box') is None: # In case no box was selected, mark as error and move on to next element.
                errors.append('%s.compose: No box selected. Cannot place element %s' % (self.__class__.__name__, e))
            elif e.isTextBox and targets['box'] is not None and targets['box'].isTextBox:
                targets['box'].bs += e.bs
            else:
                errors.append('%s.compose: No box defined or box is not a TextBox in "%s - %s"' % (self.__class__.__name__, globals['page'], e))
        return targets


if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
