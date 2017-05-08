# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     AlignElements.py
#
#     This script generates a page with aligned square, showing how conditional placement works.
#
import pagebot # Import to know the path of non-Python resources.
from pagebot.contributions.filibuster.blurb import blurb

from pagebot import getFormattedString
# Creation of the RootStyle (dictionary) with all available default style parameters filled.
from pagebot.style import getRootStyle, A4, CENTER, NO_COLOR,TOP, BOTTOM, MIDDLE
# Document is the main instance holding all information about the document togethers (pages, styles, etc.)
from pagebot.document import Document
from pagebot.elements import *
# Import all layout condition classes
from pagebot.conditions import *

from pagebot.toolbox.transformer import path2ScriptId
scriptGlobals = pagebot.getGlobals(path2ScriptId(__file__))
 
PageSize = 500

G = 8 # Distance between the squares.
SQ = 2 * G # Size of the squares

# The standard PageBot function getRootStyle() answers a standard Python dictionary, 
# where all PageBot style entries are filled by their default values. The root style is kept in RS
# as reference for the ininitialization of all elements. 
# Each element uses the root style as copy and then modifies the values it needs. 
# Note that the use of style dictionaries is fully recursive in PageBot, implementing a cascading structure
# that is very similar to what happens in CSS.

MaxPage = 1200

RedWidth = 200
RedHeight = 100
YellowWidth = 200
YellowHeight = 200
BlueWidth = 200
BlueHeight = 200

ShowOrigin = False
ShowElementInfo = False
PageSize = MaxPage

Variable([
    #dict(name='ElementOrigin', ui='CheckBox', args=dict(value=False)),
    dict(name='RedWidth', ui='Slider', args=dict(minValue=30, value=100, maxValue=MaxPage)),
    dict(name='RedHeight', ui='Slider', args=dict(minValue=30, value=100, maxValue=MaxPage)),
    dict(name='YellowWidth', ui='Slider', args=dict(minValue=60, value=100, maxValue=MaxPage)),
    dict(name='YellowHeight', ui='Slider', args=dict(minValue=30, value=100, maxValue=MaxPage)),
    dict(name='BlueWidth', ui='Slider', args=dict(minValue=30, value=100, maxValue=MaxPage)),
    dict(name='BlueHeight', ui='Slider', args=dict(minValue=30, value=100, maxValue=MaxPage)),
    dict(name='ShowOrigin', ui='CheckBox', args=dict(value=True)),
    dict(name='ShowElementInfo', ui='CheckBox', args=dict(value=False)),
    dict(name='PageSize', ui='Slider', args=dict(minValue=200, value=400, maxValue=MaxPage)),
], globals())

EXPORT_PATH = '_export/AlignElements.pdf' # Export in _export folder that does not commit in Git. Force to export PDF.

def makeDocument():
    u"""Make a new document."""

    doc = Document(w=PageSize, h=PageSize, originTop=False, pages=1)

    view = doc.getView()
    view.padding = 10 # Don't show cropmarks and such.
    view.showPageCropMarks = True
    view.showElementOrigin = ShowOrigin
    view.showElementDimensions = ShowOrigin
    view.showElementInfo = ShowElementInfo
       
    page = doc[0] # Get the single page from te document.
    
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = SQ
    
    pageArea = PageSize-2*SQ
    print PageSize, pageArea, SQ
    
    # Make new container for adding elements inside with alignment.
    newRect(z=10, w=pageArea, h=pageArea, fill=(0.8, 0.8, 0.8, 0.4), 
        parent=page, margin=0, padding=0, yAlign=MIDDLE, maxW=pageArea, maxH=pageArea, 
        xAlign=CENTER, stroke=None, conditions=(Center2Center(), Middle2Middle()))
    
    fontSize = RedHeight/3
    fs = getFormattedString('Headline in red box.', style=dict(textFill=1, fontSize=fontSize, 
        maxW=pageArea, maxH=pageArea, leading=fontSize, font='LucidaGrande'))    
    newTextBox(fs, z=0, w=RedWidth, h=RedHeight, name='RedRect', parent=page, fill=(1, 0, 0), 
        yAlign=TOP, maxW=pageArea, maxH=pageArea,
        padding=4, conditions=(Center2Center(), Top2Top()))

    if not hasattr(scriptGlobals, 'blurbText'):
        scriptGlobals.blurbText = blurb.getBlurb('article_summary', noTags=True)
    fs = getFormattedString(scriptGlobals.blurbText,
        style=dict(font='LucidaGrande', fontSize=10, leading=12, textFill=0))   
    newTextBox(fs, z=0, w=YellowWidth, h=YellowHeight, parent=page, 
        padding=4, fill=(1, 1, 0), 
        maxW=pageArea, maxH=pageArea, conditions=(Left2Left(), Float2Top()))
    
    newImage('images/cookbot10.jpg', z=0, w=BlueWidth, h=BlueHeight, parent=page, fill=(0.1, 0.1, 0.7), 
        maxW=pageArea, maxH=pageArea, conditions=(Right2Right(), Float2Top()))
    
    newRect(z=0, w=BlueWidth, h=20, parent=page, fill=(0, 1, 0), 
        conditions=(Fit2Width(), Float2Top()))
    
    score = page.solve()
    if score.fails:
        print 'Condition fails', score.fails 
    
    return doc # Answer the doc for further doing.
        
d = makeDocument()
d.export(EXPORT_PATH) 
