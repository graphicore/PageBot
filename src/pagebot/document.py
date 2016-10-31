# -*- coding: UTF-8 -*-
               
class Document(object):
    u"""Container of Page instance, Style instances and Template instances."""
    
    PAGE_CLASS = Page # Allow inherited versions of the Page class.
    TEMPLATE_CLASS = Template # Allow inherited versions of the Template class.
    FIRST_PAGE_NUMBER = 1

    U = 8
    DEFAULT_PW = 595 # 210mm, international generic fit.
    DEFAULT_PH = 11 * 72 # 11", international generic fit.
    ML = MT = MR = 3*U
    MB = 5*U
    CW = CH = 10*U
    GUTTER = U
    
    GRID_FILL = (0.8, 0.9, 1)
    GRID_STROKE = (0.8, 0.8, 0.9)
    GRID_STROKEWIDTH = 1
    
    def __init__(self, w=DEFAULT_PW, h=DEFAULT_PH, ml=ML, mt=MT, mr=MR, mb=MB, cw=CW, ch=None,
        g=GUTTER, gridFill=GRID_FILL, gridStroke=GRID_STROKE, gridStrokeWidth=GRID_STROKEWIDTH,
        missingImageFill=NO_COLOR, baselineGrid=None, baselineGridStroke=None, title=None, styles=None, pages=1, template=None):
        u"""Contains a set of Page instance and formatting methods. Allows to compose the pages
        without the need to send them directly to the output. This allows "asynchronic" page filling."""
 
        rootStyle = Style(
            name = 'root',
            w = w or self.DEFAULT_PW,
            h = h or self.DEFAULT_PH, # Size of the document..
            ml = ml, mt = mt, mr = mr, mb = mb, # Margins 
            cw = cw, ch = ch or cw , # Column width for column2point calculations.
            g = g, # Gutter
            # Grid
            showGrid = False,
            gridFill = gridFill,
            gridStroke = gridStroke, # Stroke of grid lines in part of a template.
            gridStrokeWidth = gridStrokeWidth,
            missingImageFill = missingImageFill,
            baselineGrid = baselineGrid or self.U,
            baselineGridStroke = baselineGridStroke or gridStroke,
            # Typographic defaults
            font = 'Georgia', # Default is to avoid existing font and fontSize in the graphic state.
            fallbackFont = 'LucidaGrande',
            fontSize = 12, # Font size in points
            tracking = 0, # Tracking of the current font/fontSize
            align = 'left', # Alignment, one if ('left', 'justified', 'right')
            tabs = None, # Set tabs,tuples of (float, alignment) Aligment can be “left”, “center”, “right” 
                # or any other character. If a character is provided the alignment will be right and 
                # centered on the specified character.
            openTypeFeatures = None, # List of supported OpenType features. 
                # c2pc, c2sc, calt, case, cpsp, cswh, dlig, frac, liga, lnum, onum, ordn, pnum, rlig, sinf, 
                # smcp, ss01, ss02, ss03, ss04, ss05, ss06, ss07, ss08, ss09, ss10, ss11, ss12, ss13, ss14, 
                # ss15, ss16, ss17, ss18, ss19, ss20, subs, sups, swsh, titl, tnum
            leading = None, # Relative factor to fontSize.
            rLeading = 1.4, # Relative factor to fontSize.
            paragraphTopSpacing = None,
            rParagraphTopSpacing = None,
            paragraphBottomSpacing = None,
            rParagraphBottomSpacing = None,
            baselineGridfit = False,
            firstLineGridfit = True,
            baselineShift = None, # Absolute baseline shift in points. Positive value is upward.
            rBaselineShift = None, # Relative baseline shift, multiplyer to current self.fontSize 
            needsBelow = 0, # Check if this space is available below, to get text lines below headings.
            firstLineIndent = None, # Indent of first paragraph in a text tag
            rFirstLineIndent = None, # First line indent as factor if font size.
            indent = None,
            rIndent = None, # indent as factor of font size.
            tailIndent = None,
            rTailIndent = None, # tailIndent as factor of font size
            language = 'en',
            hyphenation = True,
            wordSpace = 1, # Wordspace multiplication factor
            stripWhiteSpace = ' ', # Strip pre/post white space from e.text and e.tail and add single space
            # Color
            fill = 0, # Default is black
            stroke = None, # Default is to have no stroke.
            cmykFill = NO_COLOR, # Flag to ignore, None is valid value for color.
            cmykStroke = NO_COLOR, # Flag to ignore, None is valid value for color.
            strokeWidth = None, # Stroke thickness
        )
        self.w = w
        self.h = h
        self.title = title or 'Untitled'
        self.pages = {} # Key is pageID, often the page number. Value is Page instances.
        self.initializeStyles(styles, rootStyle)
        # Before we can do any text format (for which the graphic state needs to be set,
        # we need to create at least one first page as canvas. Otherwise a default page will be opened
        # by Drawbot. 
        self.makePages(max(pages, 1), w, h, template) # Expand the document to the request anount of pages.
        # Mark that the first page is already initialized, to avoid rendering a new page on page.export( )         
        self.needsCanvasPage = False
        # Storage for collected content, referring to their pages after composition.
        self.footnotes = {} # Keys is sequential order. Value is (page, e)
        self.literatureRefs = {}
        self.toc = {}
                       
    def initializeStyles(self, styles, rootStyle):
        u"""Make sure that the default styles always exist."""
        if styles is None:
            styles = {}
        self.styles = styles
        # Make sure that the default styles for document and page are always there.
        name = 'root'
        self.addStyle(name, rootStyle)
        name = 'page'
        if not name in self.styles:
            self.addStyle(name, Style(name=name, showGrid=True))
        name = 'document'
        if not name in self.styles:
            self.addStyle(name, Style(name=name, showGrid=True))
        self.styles = styles # Dictionary of styles. Key is XML tag name value is Style instance.

    def fromRootStyle(self, **kwargs):
        u"""Answer a new style as copy from the root style. Overwrite the defined arguments."""
        style = copy.copy(self.styles['root'])
        for name, value in kwargs.items():
            setattr(style, name, value)
        return style
        
    def getStyles(self):
        return self.styles
 
    def getStyle(self, name):
        u"""Answer the names style. If that does not exist, answer the default root style."""
        self.styles.get(name) or self.styles['root']
        
    def getRootStyle(self):
        u"""Answer the default root style, used by the composer as default for all other stacked styles."""
        return self.styles['root']
              
    def setStyles(self, styles):
        u"""Set the dictionary of styles for the document. This method can be used to swap in/out a complete
        set of styles while processing specific pages. It is the responsibility of the caller to save the existing
        style set."""
        self.styles = styles

    def __repr__(self):
        return '[Document: %s Pages: %d]' % (self.title, len(self))
        
    def __len__(self):
        return len(self.pages)
    
    def __getitem__(self, pIndex):
        u"""Answer page by index, which may be the same a the page number."""
        return self.pages[pIndex]
    
    def addToc(self, node, page, fs, tag):
        u"""Add stuff for the Table of Content, connecting the node with the composed page."""
        if not page.pageNumber in self.toc:
            self.toc[page.pageNumber] = []
        self.toc[page.pageNumber].append((node, page, fs, tag))

    def getPage(self, pageNumber):
        u"""Answer the pageNumber, where the first pages #1 is self.pages[1]"""
        return self[pageNumber]
  
    def nextPage(self, page, nextPage=1, template=None, makeNew=True):
        u"""Answer the next page of page. If it does not exist, create a new page."""
        pageNumber = page.pageNumber + nextPage
        if not pageNumber in self.pages:
            self.newPage(pageNumber=pageNumber, template=page.template)
        return self.getPage(pageNumber)
          
    def makePages(self, count, w=None, h=None, template=None):
        for n in range(count):
            self.newPage(w, h, n, template=template)
            if n == 0:
                # Actually make the first page as current canvas for textbox to calculate on.
                # Create a new Drawbot viewport page to draw template + page, if not already done.
                # Skip if the first page of the document was already made as graphic state canvas by a Composer instance.
                newPage(w, h)
                 
    def newPage(self, w=None, h=None, pageNumber=None, template=None):
        u"""Create a new page with the optional (w,h). Use (self.w, self.h) if one of the values is omitted.
        If pageNumber is omitted, then use the highest page number in self.pages as previous page.
        If pageNumber already exists, then raise an error."""
        if pageNumber is None:
            if not self.pages:
                pageNumber = self.FIRST_PAGE_NUMBER
            else:
                pageNumber = max(self.pages.keys())+1
        assert not pageNumber in self.pages # Make sure that we don't accidentally overwite existing pages.
        page = self.PAGE_CLASS(self, w or self.w, h or self.h, pageNumber, template)
        self.pages[pageNumber] = page
        return page
  
    def getStyle(self, name):
        return self.styles[name]
        
    def getTemplate(self, name):
        return self.templates[name]
        
    def addStyle(self, name, style):
        u"""Add the style to the self.styles dictionary."""
        assert not name in self.styles # Make sure that styles don't get overwritten. Remove them first.
        self.styles[name] = style
      
    def replaceStyle(self, name, style):
        self.styles[name] = style
 
    def newStyle(self, **kwargs):  
        return self.replaceStyle(kwargs['name'], Style(**kwargs))
         
    def export(self, fileName, pageSelection=None):
        u"""Export the document to fileName for all pages in sequential order. If pageSelection is defined,
        it must be a list with page numbers to export. This allows the order to be changed and pages to
        be omitted."""
        if pageSelection is None:
            pageSelection = range(1, len(self.pages)+1) # [1,2,3,4,...]
        for pIndex in pageSelection:
            # Get the current Page instance, indicated by the page number.
            page = self.pages[pIndex-1] # Page numbering stars at #1
            # Create a new Drawbot viewport page to draw template + page, if not already done.
            # Skip if the first page of the document was already made as graphic state canvas by a Composer instance.
            if pIndex > 0:
                newPage(page.w, page.h)
            # Let the page draw itself on the current Drawbot view port. pIndex can be used on output.
            page.draw() 
        saveImage(fileName)
 