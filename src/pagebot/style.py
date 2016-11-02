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
BASELINE_GRID = 2*U

# Display option
SHOW_GRID = True
SHOW_BASELINE_GRID = True
SHOW_FLOW_CONNECTIONS = True

NO_COLOR = -1

LEFT_ALIGN = 'left'
RIGHT_ALIGN = 'right'
CENTER = 'center'
JUSTIFIED = 'justified'

def getRootStyle(u=U, showGrid=SHOW_GRID, showBaselineGrid=SHOW_BASELINE_GRID,
        showFlowConnection=SHOW_FLOW_CONNECTIONS):
    u"""Answer the main root style tha contains all default style attributes of Pagebot.
    To be overwritten when needed by calling applications.
    CaAPITALIZED attribute names are for reference only. Not used directly from styles.
    They can be copied on other style attributes.
    Note that if the overall unit style.u is changed by the calling applcation, also the
    U-based values must be recalcualted for proper measures.
    """
    # Some calculations to show dependecies.
    baselineGrid = 2*u
    leftIndent = 0.8*u
    noColor = NO_COLOR

    return Style( # Answer the default root style.

        # Basic page/template measures
        name = 'root', # Name of the style, key in document.getRootstyle( )
        u = u, # Base unir of Dutch/Swiss typography :)
        w = 595, # Page width, basis size of the document. 210mm, international generic fit.
        h = 11 * 72, # Page height, basis size of the document. 11", international generic fit.
        # Margins left, top, right bottom (
        # as rounding of column width and gutter.
        ml = 7*u, # Marign top
        mt = 7*u, # Margin left
        mr = 6*u, # Margin right is used as minimum. Actual value is calculated from cw and gutter,
        mb = 6*u, # Margin bottom is used as minimum. Actual value is calculated from baseline grid.
        # Column width for column2point and column2rect calculations.
        cw = 11*u, # Column width, based on multiple of U or gutter.
        ch = u*baselineGrid - u, # Aopprocimately square with cw + gutter.
        g = u, # Main gutter of pages. Based on U.

        # Grid stuff
        showGrid = showGrid, # Flag to show the grid in output.
        gridFill = (0.8, 0.9, 0.8), # Fill color for (cw, ch) squares.
        gridStroke = (0.8, 0.8, 0.8), # Stroke of grid lines in part of a template.
        gridStrokeWidth = 1, # Line thickness of the grid.
        # Baseline grid
        showBaselineGrid = showBaselineGrid, # Flag to show baseline grid in output
        baselineGridStroke = 1, # Line thickness of baselines grid.
        # Draw connection arrows between the flow boxes on a page.
        showFlowConnections = showFlowConnection, # Flag to draw arrows between the flows for debugging.
        flowConnectionStroke1 = (0.2, 0.5, 0.1, 0.8), # Stroke color of flow lines inside column,
        flowConnectionStroke2 = (1, 0, 0, 0.8), # Stroke color of flow lines between columns.
        flowConnectionStrokeWidth = 2, # Line width of curved flow lines.
        flowMarkerFill = (0.8, 0.8, 0.8, 0.5), # Fill of flow curve marker.
        flowMarkerSize = 8, # Size of flow marker circle.
        flowCurvatureFactor = 0.15, # Factor of curved flow lines. 0 = straight lines.

        # Image stuff
        missingImageFill = 0.5, # Background color of missing image rectangles.

        # Typographic defaults
        font = 'Georgia', # Default is to avoid existing font and fontSize in the graphic state.
        fallbackFont = 'LucidaGrande',
        fontSize = u * 7/10, # Default font size in points, realted to U

        # Horizontal spacing for absolute and fontsize-related measures
        tracking = 0, # Absloute tracking value. Note that this is different from standard name definition.
        rTracking = 0, # Tracking as factor of the fontSize.
        align = LEFT_ALIGN, # Alignment, one if ('left', 'justified', 'cemter'. 'right')
        # Set tabs,tuples of (float, alignment) Aligment can be “left”, “center”, “right” 
        # or any other character. If a character is provided the alignment will be right and 
        # centered on the specified character.
        listTabs = [(leftIndent, LEFT_ALIGN)], # Default indent for bullet lists. Copy onto style.tabs for usage.
        LIST_INDENT = leftIndent, # Indent for bullet lists, Copy on style.indent for usage in list related styles.
        tabs = None, 
        firstLineIndent = 0, # Indent of first paragraph in a text tag.
        rFirstLineIndent = 0, # First line indent as factor if font size.
        indent = 0, # Left indent (for left-right based scripts)
        rIndent = 0, # Left indent as factor of font size.
        tailIndent = 0, # Tail/right indent (for left-right based scritps)
        rTailIndent = 0, # Tail/right Indent as factor of font size

        # List of supported OpenType features. 
        # c2pc, c2sc, calt, case, cpsp, cswh, dlig, frac, liga, lnum, onum, ordn, pnum, rlig, sinf, 
        # smcp, ss01, ss02, ss03, ss04, ss05, ss06, ss07, ss08, ss09, ss10, ss11, ss12, ss13, ss14, 
        # ss15, ss16, ss17, ss18, ss19, ss20, subs, sups, swsh, titl, tnum
        openTypeFeatures = None,

        # Vertical spacing for absolute and fontsize-related measures
        baselineGrid = baselineGrid,
        leading = baselineGrid, # Relative factor to fontSize.
        rLeading = 0, # Relative factor to fontSize.
        paragraphTopSpacing = 0,
        rParagraphTopSpacing = 0,
        paragraphBottomSpacing = 0,
        rParagraphBottomSpacing = 0,
        baselineGridfit = False,
        firstLineGridfit = True,
        baselineShift = 0, # Absolute baseline shift in points. Positive value is upward.
        rBaselineShift = 0, # Relative baseline shift, multiplyer to current self.fontSize
        needsAbove = 0, # Check if this space is available above, to get amount of text lines above headings.
        rNeedsAbove = 0, # Check if this relative fontSize space is available above, to get amount of text lines above headings.
        needsBelow = 0, # Check if this point space is available below, to get amount of text lines below headings.
        rNeedsBelow = 0, # Check if this relative fontSize space is available below, to get amount of text lines below headings.

        # Language and hyphenation
        language = 'en', # Language for hpyphenation and spelling. Can be altered per style.
        hyphenation = True,
        stripWhiteSpace = ' ', # Strip pre/post white space from e.text and e.tail and add single space

        # Paging
        pageNumberMarker = '#??#', # Text pattern that will be replaced by current page number.
        firstPage = 1, # First page number of the docjment.

        # Color
        NO_COLOR = noColor, # Add no-color flag (-1) to make differenve with "color" None.
        fill = 0, # Default is black
        stroke = None, # Default is to have no stroke.
        cmykFill = noColor, # Flag to ignore, None is valid value for color.
        cmykStroke = noColor, # Flag to ignore, None is valid value for color.
        strokeWidth = None, # Stroke thickness

        # Constants for standardized usage of alignment in FormattedString
        LEFT_ALIGN = LEFT_ALIGN,
        RIGHT_ALIGN = RIGHT_ALIGN,
        JUSTIFIED = JUSTIFIED,
        CENTER = CENTER,

    )
  
