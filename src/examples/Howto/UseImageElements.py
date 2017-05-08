# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     ColorSquares.py
#
#     This script generates a page with random color squares, indicating where their position is.
#     This script is using the style parameters "originTop", making the coordinate system run downwards.
#
from __future__ import division # Make integer division result in float.
import pagebot # Import to know the path of non-Python resources.

from pagebot import x2cx, y2cy
# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, A4, CENTER, NO_COLOR,TOP, BOTTOM, MM
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot import getFormattedString

from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document
    
RedSize = 100
YellowSize = 30
PagePadding = 64
PageSize = 500

GUTTER = 8 # Distance between the squares.
SQUARE = 10 * GUTTER # Size of the squares

# The standard PageBot function getRootStyle() answers a standard Python dictionary, 
# where all PageBot style entries are filled by their default values. The root style is kept in RS
# as reference for the ininitialization of all elements. 
# Each element uses the root style as copy and then modifies the values it needs. 
# Note that the use of style dictionaries is fully recursive in PageBot, implementing a cascading structure
# that is very similar to what happens in CSS.


RS = getRootStyle(w=PageSize, h=PageSize)
# Setting value for demo purpose, it is style default, using the elements origin as top-left. 
# Change to False will show origin of elements in their bottom-left corner.
if 0: # TOP
    RS['originTop'] = True
    RS['yAlign'] = TOP 
else:
    RS['originTop'] = False 
    RS['yAlign'] = BOTTOM 
  
# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/UseImages.pdf' 


Variable([
    #dict(name='ElementOrigin', ui='CheckBox', args=dict(value=False)),
    dict(name='RedSize', ui='Slider', args=dict(minValue=100, value=100, maxValue=500)),
    dict(name='YellowSize', ui='Slider', args=dict(minValue=10, value=30, maxValue=500)),
    dict(name='PagePadding', ui='Slider', args=dict(minValue=10, value=30, maxValue=100)),
    dict(name='PageSize', ui='Slider', args=dict(minValue=100, value=400, maxValue=800)),
], globals())

def makeDocument(rs):
    u"""Make a new document, using the rs as root style."""

    #W = H = 120 # Get the standard a4 width and height in points.
    W = PageSize
    H = PageSize

    # Hard coded SQUARE and GUTTE, just for simple demo, instead of filling padding an columns in the root style.
    # Page size decides on the amount squares that is visible.
    # Page padding is centered then.
    sqx = int(W/(SQUARE + GUTTER)) # Whole amount of squares that fit on the page.
    sqy = int(H/(SQUARE + GUTTER))
    # Calculate centered paddings for the amount of fitting squares.
    # Set values in the rootStyle, so we can compare with column calculated square position and sizes.
    rs['colH'] = rs['colW'] = SQUARE  # Make default colW and colH square.

    #padX = (W - sqx*(SQUARE + GUTTER) + GUTTER)/2
    my = (H - sqy*(SQUARE + GUTTER) + GUTTER)/2

    doc = Document(rootStyle=rs, title='Color Squares', autoPages=1)
    
    view = doc.getView()
    view.showElementOrigin = True
    view.padding = 0 # Aboid showing of crop marks, etc.
    
    # Get list of pages with equal y, then equal x.    
    #page = doc[0][0] # Get the single page from te document.
    page = doc.getPage(0) # Get page on pageNumber, first in row (this is only one now).
    page.name = 'This is a demo page for floating child elements'
    page.padding = PagePadding
    
    page.w = W
    page.h = H
 
    page.gutter3D = GUTTER # Set all 3 gutters to same value
    """
    im = newImage('images/cookbot10.jpg', (50, 50, 10), padding=0, parent=page, w=200, conditions=(Top2Top(), Fit2Width()), elasticH=True, yAlign=BOTTOM,
        frameFill=(0, 1, 0, 0.3), 
        frameStroke=(1, 0, 0)
    )
    if im.image:
        print im.image.size
    # Give parent on creation, to have the css chain working.
    """
    rr = newRect(fill=(1, 0, 0), w=RedSize, h=RedSize, conditions=(Left2Left(), Bottom2Bottom()), 
        parent=page) 
    rr.pb = 10
    
    yr1 = newRect(fill=(1, 1, 0), w=YellowSize, h=YellowSize, parent=rr, xAlign=CENTER, yAlign=TOP,
        conditions=(Center2Center(), Bottom2Bottom())) 
    yr2 = newRect(fill=(0, 1, 1), z=10, w=50, h=50, parent=rr, xAlign=CENTER, 
        conditions=(Top2TopSide(), Center2Center(),)) 
   
    # Caption falls through the yr2 (with differnt z) and lands on yr1 by Float2BottomSide()    
    cap = newTextBox('Float down to yr1. '*6, w=rr.w, name='Caption', parent=rr,
        font='Verdana', conditions=[ Fit2Width(), Float2BottomSide()], elasticH=True,
        fontSize=8, textFill=0, frameStrokeWidth=0.5, frameFill=(0, 0, 1, 0.3), frameStroke=(0, 0, 1),
    )
    cap.padding = 10
    print cap.isLeftOnLeft(0)
    print cap.isRightOnRight(0)
    print Fit2Width().test(cap)
    print cap.mw, cap.mh, cap.md
    print cap.pw, cap.ph, cap.pd
    
    score = page.solve()
    if score.fails:
        print score.fails
    return doc # Answer the doc for further doing.
        
d = makeDocument(RS)
d.export(EXPORT_PATH) 
