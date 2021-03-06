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
#     pbpage.py
#
import weakref
from pagebot.elements.element import Element
from pagebot.toolbox.units import pointOffset
from pagebot.style import ORIGIN

class Page(Element):
    """The Page container is typically the root of a tree of Element instances.
    A Document contains a set of pages.

    Since pages an build into fixed media, such as PDF, PNG and animated GIF,
    as well as HTML pages in a site, there is a mixture of meta data available
    in a Page."""

    isPage = True

    VIEW_PORT = "width=device-width, initial-scale=1.0, user-scalable=yes"
    FAVICON_PATH = 'images/favicon.ico'
    INDEX_HTML = 'index.html'
    INDEX_HTML_URL = INDEX_HTML

    def __init__(self, isLeft=None, isRight=None,
        htmlCode=None, htmlPath=None, headCode=None, headPath=None, bodyCode=None, bodyPath=None,
        cssCode=None, cssPaths=None, cssUrls=None, jsCode=None, jsPaths=None, jsUrls=None,
        viewPort=None, favIconUrl=None, fileName=None, url=None, webFontUrls=None,
        **kwargs):

        """Add specific parameters for a page, besides the parameters for standard Elements.

        >>> page = Page()
        >>> page.w, page.h
        (100pt, 100pt)
        >>> page.size = 1111, 2222
        >>> page.size
        (1111pt, 2222pt)
        >>> page
        <Page Unplaced (1111pt, 2222pt)>
        """
        Element.__init__(self, **kwargs)

        self.cssClass = self.cssClass or 'page' # Defined default CSS class for pages.
        # Overwrite flag for side of page. Otherwise test on document pagenumber.
        self._isLeft = isLeft
        self._isRight = isRight

        #   F I L E  S T U F F

        self.fileName = fileName or self.INDEX_HTML

        #   H T M L  S T U F F

        # Site stuff
        self.viewPort = viewPort or self.VIEW_PORT
        self.appleTouchIconUrl = None
        self.favIconUrl = favIconUrl or self.FAVICON_PATH

        self.url = url or self.INDEX_HTML_URL # Used for links to home or current page url

        # Optional resources that can be included for web output (HtmlContext)
        # Define string or file paths where to read content, instead of constructing by the builder.
        # See also self.htmlCode and self.htmlPath as defined for all Element classes.

        self.headCode = headCode # Optional set to string that contains the page <head>...</head>, including the tags.
        self.headPath = headPath # Set to path, if head is available in a single file, including the tags.

        self.cssCode = cssCode # Set to string, if CSS is available as single source. Exported as css file once.
        self.cssPaths = cssPaths # Set to path, if CSS is available in a single file to be included in the page.
        self.cssUrls = cssUrls # Optional CSS, if different from what is defined by the view.

        self.bodyCode = bodyCode # Optional set to string that contains the page <body>...</body>, including the tags.
        self.bodyPath = bodyPath # Set to path, if body is available in a single file, including the tags.

        self.jsCode = jsCode # Set to path, if JS is available in a single file, including the tags.
        self.jsPaths = jsPaths # Optional javascript, to be added at the end of the page, inside <body>...</body> tag.
        self.jsUrls = jsUrls # Optional Javascript Urls in <head>, if different from what is defined by the view.

        self.webFontUrls = webFontUrls # Optional set of webfont urls if different from what is in the view.

    def __repr__(self):
        """Page as string. Similar to general Element.__repr__, except showing
        the (pagenNumber, index) as it is stored in the parent document. And
        not showing (self.x, self.y), as most pages will not be part of another
        page (although it is allowed and there could be situations to do so,
        e.g. if a page is used as illustration in another page.)

        >>> from pagebot.document import Document
        >>> from pagebot.constants import A4
        >>> doc = Document(name='TestDoc', autoPages=8, size=A4)
        >>> doc[5] # Remembers original unit size.
        <Page:default 5 (210mm, 297mm)>
        """
        if self.title:
            name = ':'+self.title
        elif self.name:
            name = ':'+self.name
        else: # No name
            name = ' Unplaced'

        if self.elements:
            elements = ' E(%d)' % len(self.elements)
        else:
            elements = ''

        pn = ''
        if self.parent: # If there is a parent, get the (pageNumber, index) tuple.
            pn_index = self.parent.getPageNumber(self)
            if pn_index is not None:
                if pn_index[1]: # Index > 1, then show.
                    pn = ' %d:%d' % pn_index
                else:
                    pn = ' %d' % pn_index[0]

        return '<%s%s%s (%s, %s)%s>' % (self.__class__.__name__, name, pn, self.w, self.h, elements)

    def _get_isLeft(self):
        """Answer if this is a left page (even pagenumber), unless the
        self._isLeft is overwritten by a boolean, other than None. Note
        that pages can be both left or right.

        >>> from pagebot.document import Document
        >>> doc = Document(name='TestDoc', autoPages=8)
        >>> page = doc[5]
        >>> page.isLeft
        False
        >>> page.isLeft = True
        >>> page.isLeft
        True
        >>> page.isLeft = None # Reset to automatic behavior by setting as None
        >>> page.isLeft
        False
        """
        if self._isLeft is not None:
            return self._isLeft
        if self.parent is not None:
            return self.parent.getPageNumber(self)[0] % 2 == 0
        return None
    def _set_isLeft(self, flag):
        self._isLeft = flag
    isLeft = property(_get_isLeft, _set_isLeft)

    def _get_isRight(self):
        """Answer if this is a right page, if that info is stored. Note that
        pages can be neither left or right. Otherwise, the only one who can
        know that is the document.

        >>> from pagebot.document import Document
        >>> doc = Document(name='TestDoc', autoPages=8)
        >>> page = doc[5]
        >>> page.isLeft # Uneven is automatic right page.
        False
        >>> page.isLeft = True # Unless forced to be left.
        >>> page.isLeft
        True
        >>> page.isLeft = None # Reset to automatic behavior by setting as None
        >>> page.isLeft
        False
        """
        if self._isRight is not None: # Overwritted by external call.
            return self._isRight
        if self.doc is not None:
            return self.parent.getPageNumber(self)[0] % 2 == 1
        return None
    def _set_isRight(self, flag):
        self._isRight = flag
    isRight = property(_get_isRight, _set_isRight)

    def _get_next(self):
        """Answer the page with the next page number the document, relative to
        self. Create a new page if self is the last page in the self.parent
        document. Answer None if the self page has no parent.

        >>> from pagebot.document import Document
        >>> doc = Document(name='TestDoc', autoPages=8)
        >>> page = doc[5]
        >>> page.next.pn # Skip any sub-pages with the same page number.
        (6, 0)
        >>> page.next.next.pn
        (7, 0)
        >>> page.next.prev is page
        True
        """
        if self.parent is None:
            return None
        return self.parent.nextPage(self)
    next = property(_get_next)

    def _get_prev(self):
        u"""Answer the previous page in the document, relative to self. Answer None
        if self is the first page.

        >>> from pagebot.document import Document
        >>> doc = Document(name='TestDoc', autoPages=8)
        >>> page = doc[5]
        >>> page.prev.pn # Skip any sub-pages with the same page number.
        (4, 0)
        >>> page.prev.prev.pn
        (3, 0)
        >>> page.prev.next is page
        True
        """
        if self.parent is None:
            return None
        return self.parent.prevPage(self)
    prev = property(_get_prev)

    def _get_pn(self):
        """Answer the page number by which self is stored in the parent
        document. This property is readonly. To move or remove pages, use
        Document.movePage() or Document.removePage()

        >>> from pagebot.document import Document
        >>> doc = Document(name='TestDoc', autoPages=8)
        >>> sorted(doc.pages.keys())
        [1, 2, 3, 4, 5, 6, 7, 8]
        >>> page = doc[5]
        >>> page.pn
        (5, 0)
        """
        if self.parent is None:
            return None # Not placed directly in a document. No page number known.
        return self.parent.getPageNumber(self)
    pn = property(_get_pn)

    #   D R A W B O T  & F L A T  S U P P O R T

    def build(self, view, origin=ORIGIN, drawElements=True):
        """Draw all elements of this page in DrawBot. Note that this method is only used
        in case pages are drawn as element on another page. In normal usage, pages
        get drawn by PageView.build"""
        p = pointOffset(self.origin, origin) # Ignoe z-axis for now.

        view.drawPageMetaInfo(self, p, background=True)

        # If there are child elements, draw them over the text.
        if drawElements:
            self.buildChildElements(view, p) # Build child elements, depending in context build implementations.

        # Draw addition page info, such as crop-mark, registration crosses, etc. if parameters are set.
        view.drawPageMetaInfo(self, p, background=False)

        # Check if we are in scaled mode. Then restore.
        #self._restoreScale()

    #   H T M L  /  C S S  S U P P O R T

    def build_html(self, view, path):
        """Build the HTML/CSS code through WebBuilder (or equivalent) that is
        the closest representation of self. If there are any child elements,
        then also included their code, using the level recursive indent.

        Single page site, exporting to html source, with CSS inside.
        >>> import os
        >>> from pagebot.document import Document
        >>> doc = Document(name='SinglePageSite', viewId='Site')
        >>> page = doc[1]
        >>> page.title = 'Home'
        >>> page.cssCode = 'body {background-color:black}'
        >>> exportPath = '_export/Home' # No extension for site folder if exporting to a website
        >>> #doc.export(exportPath)
        >>> #result = os.system('open %s/index.html' % exportPath)
        """
        context = view.context # Get current context and builder from this view.
        b = context.b # This is a bit more efficient than self.b once we got the context fixed.
        b.resetHtml()

        self.build_scss(view)

        if self.htmlCode: # In case the full HTML is here, then just output it.
            b.addHtml(self.htmlCode) # This is mostly used for debug and new templates.
        elif self.htmlPaths is not None:
            for htmlPath in self.htmlPaths:
                b.importHtml(htmlPath) # Add HTML content of file, if path is not None and the file exists.
        else:
            b.docType('html')
            b.html()#lang="%s" itemtype="http://schema.org/">\n' % self.css('language'))
            #
            #   H E A D
            #
            # Build the page head. There are 3 option (all including the <head>...</head>)
            # 1 As html string (info.headHtml is defined as not None)
            # 2 As path a html file, containing the string between <head>...</head>.
            # 3 Constructed from info contect, page attributes and styles.
            #
            if self.headCode is not None:
                b.addHtml(self.headCode)
            elif self.headPath is not None:
                b.importHtml(self.headPath) # Add HTML content of file, if path is not None and the file exists.
            else:
                b.head()
                b.meta(charset=self.css('encoding')) # Default utf-8
                # Try to find the page name, in sequence order of importance.
                b.title_(self.title or self.name)

                b.meta(httpequiv='X-UA-Compatible', content='IE=edge,chrome=1')

                # Devices
                if self.viewPort is not None: # Not supposed to be None. Check anyway
                    b.comment('Mobile viewport')
                    b.meta(name='viewport', content=self.viewPort)

                # View and pages can both implements Webfonts urls
                for webFontUrls in (view.webFontUrls, self.webFontUrls):
                    if webFontUrls is not None:
                        for webFontUrl in webFontUrls:
                            b.link(rel='stylesheet', type="text/css", href=webFontUrl, media='all')

                # View and pages can both implements CSS paths
                for cssUrls in (view.cssUrls, self.cssUrls):
                    if cssUrls is not None:
                        for cssUrl in cssUrls:
                            b.link(rel='stylesheet', href=cssUrl, type='text/css', media='all')

                # Use one of both of these options in case CSS needs to be copied into the page.
                for cssCode in (view.cssCode, self.cssCode):
                    if cssCode is not None:
                        # Add the code directly into the page if it is not None
                        b.style()
                        b.addHtml(cssCode)
                        b._style()

                # Use one or both of these options in case CSS is needs to be copied from files into the page.
                for cssPaths in (view.cssPaths, self.cssPaths):
                    if self.cssPaths:
                        b.style()
                        for cssPath in cssPaths:
                            # Include CSS content of file, if path is not None and the file exists.
                            b.importHtml(cssPath)
                        b._style()

                # Icons
                if self.favIconUrl: # Add the icon link and let the type follow the image extension.
                    b.link(rel='icon', href=self.favIconUrl, type='image/%s' % self.favIconUrl.split('.')[-1])
                if self.appleTouchIconUrl: # Add the icon link and let the type follow the image extension.
                    b.link(rel='apple-touch-icon-precomposed', href=self.appleTouchIconUrl, type='image/%s' % self.appleTouchIconUrl.split('.')[-1])

                # Description and keywords
                if self.description:
                    b.meta(name='description', content=self.description)
                if self.keyWords:
                    b.meta(name='keywords', content=self.keyWords)
                b._head()
            #
            #   B O D Y
            #
            # Build the page body. There are 3 option (all excluding the <body>...</body>)
            # 1 As html string (self.bodyCode is defined as not None)
            # 2 As path to a html file, containing the string between <body>...</body>, including the tags
            # 3 Constructed from view parameter context, page attributes and styles.
            #
            if self.bodyCode is not None:
                b.addHtml(self.bodyCode)
            elif self.bodyPath is not None:
                b.importHtml(self.bodyPath) # Add HTML content of file, if path is not None and the file exists.
            else:
                b.body()
                for e in self.elements:
                    e.build_html(view, path)
                #
                #   J A V A S C R I P T
                #
                # Build the JS body. There are 3 option (all not including the <script>...</script>)
                # 1 As html/javascript string (view.jsCode and/or self.jsCode are defined as not None)
                # 2 As path a html file, containing the string between <script>...</script>, including the tags.
                # 3 Constructed from info context, page attributes and styles.
                #
                for jsCode in (view.jsCode, self.jsCode):
                    if jsCode is not None:
                        b.script(type="text/javascript")
                        b.addHtml(self.jsCode)
                        b._script()
                for jsUrls in (view.jsUrls, self.jsUrls):
                    if jsUrls is not None:
                        for jsUrl in jsUrls:
                            b.script(type="text/javascript", src=jsUrl)
                for jsPaths in (view.jsPaths, self.jsPaths):
                    if jsPaths:
                        for jsPath in jsPaths:
                            b.script(type="text/javascript")
                            b.addHtml(jsPath)
                            b._script()

                if b.hasJs():
                    b.script()
                    b.addHtml('\n'.join(b.getJs()))
                    b._script()
                #else no default JS. To be added by the calling application.
                # Close the page body
                b._body()
            b._html()

        # Construct the file name for this page and save the file.
        fileName = self.name
        if not fileName:
            fileName = self.DEFAULT_HTML_FILE
        if not fileName.lower().endswith('.html'):
            fileName += '.html'
        if view.doExport: # View flag to avoid writing, in case of testing.
            b.writeHtml(path + fileName)

class Template(Page):

    def _get_parent(self):
        """Answer the parent of the element, if it exists, by weakref
        reference. Answer None of there is not parent defined or if the parent
        not longer exists."""
        if self._parent is not None:
            return self._parent()
        return None

    def _set_parent(self, parent):
        """Set the parent of the template. Don't call self.appendParent here,
        as we don't want the parent to add self to the page/element list. Just
        a simple reference, to connect to styles, etc."""
        if parent is not None:
            parent = weakref.ref(parent)
        self._parent = parent
    parent = property(_get_parent, _set_parent)

    def draw(self, origin, view):
        raise ValueError('Templates cannot draw themselves in a view. Apply the template to a page first.')

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
