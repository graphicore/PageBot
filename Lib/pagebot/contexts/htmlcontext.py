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
#     htmlcontext.py
#
from pagebot.contexts.basecontext import BaseContext
from pagebot.contexts.builders.htmlbuilder import HtmlBuilder
from pagebot.contexts.strings.htmlstring import HtmlString
from pagebot.toolbox.color import noColor

class HtmlContext(BaseContext):
    """A HtmlContext instance builds all necessary for a website, taking the element.
    Most of the building is done by the HtmlBuilder instance, stored as self.b.
    Still we need this HtmlContext layer, as not all drawing can be done in html, so 
    this context can decide to include SVG or pixel images for the HTML-representation
    of certain types of elements.
    
    TODO: Add all methods compatible with DrawBotContext, even if empty functionality
    for HTML/CSS.
    """
    useTags = True # Indication to Typesetter that by default tags should be included in output.
    
    # Used by the generic BaseContext.newString( )
    STRING_CLASS = HtmlString
    EXPORT_TYPES = ('html', 'css', 'js')

    def __init__(self):
        self.b = HtmlBuilder()
        self._fill = self._stroke = noColor
        self._strokeWidth = 0

    #   T E X T

    def newBulletString(self, bullet, e=None, style=None):
        """Ignore by answering None, as HTML does bullets automatic."""
        return None 

    #   D R A W I N G

    def rect(self, x, y, w, h):
        # TODO: Implement as SVG.
        pass
    
    def oval(self, x, y, w, h):
        # TODO: Implement as SVG.
        pass
    
    def circle(self, x, y, r):
        # TODO: Implement as SVG.
        pass
    
    def line(self, p1, p2):
        # TODO: Implement as SVG.
        pass

    #   I M A G E

    def imagePixelColor(self, path, p):
        return 0
        #return cls.b.imagePixelColor(path, p)

    def imageSize(self, path):
        """Answer the (w, h) image size of the image file at path."""
        return (0, 0)
        #return cls.b.imageSize(path)

    #   C O L O R

    def fill(self, c):
        self._fill = c

    setFillColor = fill # DrawBot compatible API
      
    def stroke(self, c, w=None):
        self._stroke = c
        if w is not None:
            self.strokeWidth(w)

    setStrokeColor = stroke # DrawBot compatible API
       
    def strokeWidth(self, w):
        self._strokeWidth = w

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
