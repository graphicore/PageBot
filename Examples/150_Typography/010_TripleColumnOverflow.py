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
#     010_TripleColumnOverflow.py
#
#     Draw a two columns with a single text, showing overflow from one column
#     into the other. Use some view.showGrid options to show the grid.
#     Use view.showBaselines = True to show the baselines of the text.

#from pagebot.contexts.flatcontext import FlatContext
from pagebot.contexts.platform import getContext

from pagebot.fonttoolbox.objects.font import findFont
from pagebot.document import Document
from pagebot.elements import * # Import all types of page-child elements for convenience
from pagebot.toolbox.color import color
from pagebot.toolbox.units import em, p, pt
from pagebot.conditions import * # Import all conditions for convenience.
from pagebot.constants import GRID_COL_BG, GRID_ROW_BG, GRID_SQR_BG, LANGUAGE_EN

#context = FlatContext()
context = getContext() # Get the context that we are running in (e.g. DrawBotContext = DrawBot)

W, H = pt(1500, 1000) # Document size
PADDING = pt(100) # Page padding on all sides
G = p(2) # 2 Pica gutter
PW = W - 2*PADDING # Usable padded page width
PH = H - 2*PADDING # Usable padded page height
CW = (PW - G)/3 # Column width
CH = PH
# Hard coded grid for 3 columns, will be automatic in later examples.
GRIDX = ((CW, G), (CW, G), (CW, G))
GRIDY = ((CH, 0),) # No division in vertical grid.
BASELINE = G

text = """Considering the fact that the application allows individuals to call a phone number and leave a voice mail, which is automatically translated into a tweet with a hashtag from the country of origin. """

# Get the font object, from te Roboto file that is included in PageBot resources for testing.
font = findFont('Roboto-Regular')

# Make the style dictionary for the body text.
style = dict(font=font, fontSize=24, leading=em(1.4), textFill=0.3, hyphenation=LANGUAGE_EN)
# Make long formatted BabelString (type depends on the context) text to force box overflow
t = context.newString(text * 16, style=style)
# Create a new document with 1 page. Set overall size and padding.
doc = Document(w=W, h=H, padding=PADDING, gridX=GRIDX, gridY=GRIDY, context=context, originTop=True, baselineGrid=BASELINE)
# Get the default page view of the document and set viewing parameters
view = doc.view
view.showTextOverflowMarker = True # Shows as [+] marker on bottom-right of page.
view.showOrigin = True # Show position of elements as cross-hair
view.showGrid = [GRID_COL_BG, GRID_ROW_BG, GRID_SQR_BG] # Set types of grid lines to show for background
view.showBaselines = True # Show default baseline grid of the column lines.

# Get the page, with size/padding inheriting from the document setting.
page = doc[1]
# Make text box as child element of the page and set its layout conditions
# to fit the padding of the page and the condition Overflow2Next() that 
# checks on text overflow.
c1 = newTextBox(t, w=CW, name='c1', parent=page, nextElementName='c2',
    conditions=[Left2Left(), Top2Top(), Fit2Height(), Overflow2Next()])
# Text without initial content, will be filled by overflow of c1.
# Not showing the [+] marker, as the overflow text fits in the flows into
# the third column.
c2 = newTextBox(w=CW, name='c2', parent=page, nextElementName='c3',
    conditions=[Left2Col(1), Top2Top(), Fit2Height(), Overflow2Next()])
# Text without initial content, will be filled by overflow of c2.
# Showing the [+] marker, as the overflow text does not fit in the third column.
c3 = newTextBox(w=CW, name='c3', parent=page,
    conditions=[Left2Col(2), Top2Top(), Fit2Height()])
# Solve the page/element conditions. It will test the conditions (in page
# order, element order and order of the conditions list), adjusting the
# position and size of the text boxes and checking of the there is text 
# overflow that needs to be linked to boxes marked by nextElementName.
doc.solve()

# Export the document to this PDF file.
doc.export('_export/TripleColumnOverflow.pdf')
# And to a png as example.
doc.export('_export/TripleColumnOverflow.png')

