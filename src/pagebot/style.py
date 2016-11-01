# -*- coding: UTF-8 -*-

class Style(object):
    u"""Container for style instances."""
        
    def __init__(self, **kwargs):
        # Overwite default values from user arguments.
        for name, value in kwargs.items():
            setattr(self, name, value)
 
    def __repr__(self):
        return '[%s=%s font=%s fontSize=%s fill=%s]' % (self.__class__.__name__, 
            self.name, self.font, self.fontSize, self.fill)
           
    def __getitem__(self, name):
        if hasattr(self, name):
            return getattr(self, name)
        return None

    def __setitem__(self, name, value):
        self.name = value
        
    def get(self, name, default=None):
        if hasattr(self, name):
            return getattr(self, name)
        return default

# Basic layout measures 
U = 7
PW = 595 # Page width 210mm, international generic fit.
PH = 11 * 72 # Page height 11", international generic fit.
ML = 7*U # Margin left
MT = 7*U # Margin top
MR = MB = 0 # Calculated as result of ml/mt and cw/ch
BASELINE_GRID = 2*U
CW = 11*U # Column width. 
G = U # Generic gutter.
CH = 6*BASELINE_GRID - G # Approx. square. Fit with baseline.
LIST_INDENT = U*0.8 # Indent for bullet lists
# Display option
SHOW_GRID = True
SHOW_BASELINE_GRID = True
SHOW_FLOW_CONNECTIONS = True
GRID_FILL = (0.8, 0.9, 0.8)
GRID_STROKE = (0.8, 0.8, 0.8)
GRID_STROKEWIDTH = 1
FLOW_CONNECTION_STROKE1 = (0.2, 0.5, 0.1, 0.8)
FLOW_CONNECTION_STROKE2 = (1, 0, 0, 0.8)
FLOW_CONNECTION_STROKEWIDTH = 2 # Line width of curved flow lines
FLOW_MARKER_FILL = (0.8, 0.8, 0.8, 0.5) # Fill of flow curve marker.
FLOW_MARKER_SIZE = 8 # Size of flow marker circle.
FLOW_CURVATURE_FACTOR = 0.15 # Factor of curved flow lines.
# Text measures
LEADING = BASELINE_GRID
RLEADING = 0
FONTSIZE = 10
FONT = 'Georgia'
FALLBACK_FONT = 'LucidaGrande'
OPENTYPE_FEATURES = None
LEFT_ALIGN = 'left'
RIGHT_ALIGN = 'right'
CENTER = 'center'
JUSTIFIED = 'justified'

# Tracking presets
H1_TRACK = H2_TRACK = 0.015
H3_TRACK = 0.030 # Tracking as relative factor to font size.
P_TRACK = 0.030

# Language settings
LANGUAGE = 'en'
PAGENUMBER_MARKER = '#?#'
FIRSTPAGE = 1
NO_COLOR = -1
MISSING_IMAGE_FILL = 0.5
 
def getRootStyle():
    return Style(
        name = 'root',
        u = U,
        w = PW,
        h = PH, # Size of the document..
        ml = ML, mt = MT, mr = MR, mb = MB, # Margins 
        cw = CW, ch = CH , # Column width for column2point calculations.
        g = G, # Gutter
        # Grid
        showGrid = SHOW_GRID,
        showBaselineGrid = SHOW_BASELINE_GRID,
        gridFill = GRID_FILL,
        gridStroke = GRID_STROKE, # Stroke of grid lines in part of a template.
        gridStrokeWidth = GRID_STROKEWIDTH,
        # Draw connection arrows between the flow boxes on a page.
        showFlowConnections = SHOW_FLOW_CONNECTIONS, # Draw arrows between the flows for debugging.
        flowConnectionStroke1 = FLOW_CONNECTION_STROKE1,
        flowConnectionStroke2 = FLOW_CONNECTION_STROKE2,
        flowConnectionStrokeWidth = FLOW_CONNECTION_STROKEWIDTH,
        flowMarkerFill = FLOW_MARKER_FILL,
        flowMarkerSize = FLOW_MARKER_SIZE,
        flowCurvatureFactor = FLOW_CURVATURE_FACTOR,
        # Image stuff
        missingImageFill = MISSING_IMAGE_FILL,
        # Typographic defaults
        font = FONT, # Default is to avoid existing font and fontSize in the graphic state.
        fallbackFont = FALLBACK_FONT,
        fontSize = FONTSIZE, # Font size in points
        tracking = 0, # Absloute tracking value.
        rTracking = 0, # Tracking as factor of the fontSize.
        align = LEFT_ALIGN, # Alignment, one if ('left', 'justified', 'cemter'. 'right')
        # Set tabs,tuples of (float, alignment) Aligment can be “left”, “center”, “right” 
        # or any other character. If a character is provided the alignment will be right and 
        # centered on the specified character.
        listTabs = [(LIST_INDENT, LEFT_ALIGN)], # Default indent for bullet lists. Copy onto style.tabs for usage.
        listIndent = LIST_INDENT, # Copy on style.indent for usage.
        tabs = None, 
        firstLineIndent = None, # Indent of first paragraph in a text tag
        rFirstLineIndent = None, # First line indent as factor if font size.
        indent = None,
        rIndent = None, # indent as factor of font size.
        tailIndent = None,
        rTailIndent = None, # tailIndent as factor of font size

        # List of supported OpenType features. 
        # c2pc, c2sc, calt, case, cpsp, cswh, dlig, frac, liga, lnum, onum, ordn, pnum, rlig, sinf, 
        # smcp, ss01, ss02, ss03, ss04, ss05, ss06, ss07, ss08, ss09, ss10, ss11, ss12, ss13, ss14, 
        # ss15, ss16, ss17, ss18, ss19, ss20, subs, sups, swsh, titl, tnum
        openTypeFeatures = OPENTYPE_FEATURES, 
        # Vertical spacing
        baselineGrid = BASELINE_GRID,
        baselineGridStroke = GRID_STROKEWIDTH,
        leading = LEADING, # Relative factor to fontSize.
        rLeading = RLEADING, # Relative factor to fontSize.
        paragraphTopSpacing = None,
        rParagraphTopSpacing = None,
        paragraphBottomSpacing = None,
        rParagraphBottomSpacing = None,
        baselineGridfit = False,
        firstLineGridfit = True,
        baselineShift = None, # Absolute baseline shift in points. Positive value is upward.
        rBaselineShift = None, # Relative baseline shift, multiplyer to current self.fontSize 
        needsAbove = 0, # Check if this space is available above, to get amount of text lines above headings.
        rNeedsAbove = 0, # Check if this relative fontSize space is available above, to get amount of text lines above headings.
        needsBelow = 0, # Check if this point space is available below, to get amount of text lines below headings.
        rNeedsBelow = 0, # Check if this relative fontSize space is available below, to get amount of text lines below headings.
        # Language and hyphenation
        language = LANGUAGE,
        hyphenation = True,
        stripWhiteSpace = ' ', # Strip pre/post white space from e.text and e.tail and add single space
        pageNumberMarker = PAGENUMBER_MARKER,
        # Color
        noColor = NO_COLOR,
        fill = 0, # Default is black
        stroke = None, # Default is to have no stroke.
        cmykFill = NO_COLOR, # Flag to ignore, None is valid value for color.
        cmykStroke = NO_COLOR, # Flag to ignore, None is valid value for color.
        strokeWidth = None, # Stroke thickness
    )
  
