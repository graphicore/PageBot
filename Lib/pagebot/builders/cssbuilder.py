# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     cssbuilder.py
#
#     U N D E R  D E V E L O P M E N T
#
#     This builder is being worked on. 
#     It will generate the export .css from all CSS-based style values in the element tree,
#     which will be used by the HtmlBuilder to generate a close representation of the 
#     document as interactive & responsive website.
#
#     TODO: Also make available as SCSS generator.
#
import codecs
import pagebot
from basebuilder import BaseBuilder
from pagebot.toolbox.transformer import color2Css, value2Tuple4

HTMLTAGS = set(['h1','h2','h3','h4','h5','h6','p','span','div'])

STYLE2CSS = {
    'fill': ('background-color: %s;', (1, 1, 1), color2Css),
    'font': ('font-family: %s;', 'Verdana, Sans', None),
    'fontSize': ('font-size: %spx;', 12, None),
    'textFill': ('color: %s;', (0, 0, 0), color2Css),
    'leading': ('line-height: %spx;', None, None),
    'rLeading': ('line-height: %sem;', '%0.2f'%1.3, None),
    'padding': ('padding: %spx %spx %spx %spx;', (0, 0, 0, 0), value2Tuple4),
    'pl': ('padding-left: %spx;', 0, None),
    'pt': ('padding-top: %spx;', 0, None),
    'pb': ('padding-bottom: %spx;', 0, None),
    'pr': ('padding-right: %spx;', 0, None),
}

class CssBuilder(BaseBuilder):

    def build(self, e, view):
        u"""
        Builds the CSS for Element e and downwards, using the view parent document 
        as reference for styles.
        """
        assert self.path is not None
        line = '\t'+'.'*70+'\n'
        out = codecs.open(self.path, 'w', 'utf-8')
        out.write('@charset "UTF-8";\n')
        out.write("/*\n%s\tGenerated by PageBot Version %s\n%s*/\n" % (line, pagebot.__version__, line))

        doc = e.doc
        self.buildRootStyle(doc, out)
        self.buildMainStyles(doc, out)
        out.close()

    def _writeStyleValue(self, name, value, out):
        u"""Write the converted style value as CSS, using STYLE2CSS for conversion parameters."""
        if name in STYLE2CSS:
            cssName, default, f = STYLE2CSS[name]
            cssValue = value or default
            if f is not None:
                cssValue = f(cssValue)
            if cssValue is not None:
                out.write('\t'+(cssName % cssValue)+(' /* %s:%s */\n' % (name, `value`)))
                return True # Mark that we found it
        return False

    def _cssId(self, name):
        if name in HTMLTAGS:
            return name
        return 'div.'+name

    def _buildStyle(self, doc, out, style):
        u"""Export the style parameters as translated CSS values."""
        # For now write all values as comment as development reference.
        notProcessed = {}
        for parName, value in sorted(style.items()):
            if parName == 'name':
                continue
            if not self._writeStyleValue(parName, value, out):
                notProcessed[parName] = value

        # For now write all unprocessed values as comments a development reference.
        if notProcessed: # Any style value not processed, then show as comment.
            out.write('/*')
            for parName, value in sorted(notProcessed.items()):
        		out.write('\t%s: %s;\n' % (self._cssId(parName), value))
            out.write('*/\n')

    def buildRootStyle(self, doc, out):
    	u"""Translate the doc.rootStyle to the root body{...} CSS style using doc.rootStyle values."""
    	out.write('body {\n')
        self._buildStyle(doc, out, doc.styles['root'])
    	out.write('} /* body */\n\n')

    def buildMainStyles(self, doc, out):
    	u"""Build the styles for text elements, as defined in the doc.styles dictionary."""
    	for styleName, style in sorted(doc.styles.items()):
            if styleName == 'root':
                continue
            cssId = self._cssId(styleName)
            out.write('%s {\n' % cssId)
            self._buildStyle(doc, out, style)
            out.write('} /* %s */\n\n' % cssId)

    def buildElementStyles(self, doc, out, e=None):
        u"""Recursively build all style values into CSS."""
    	if e is None:
    		self.builfElementStyle(doc, out, self)
    	else:
            cssId = self._cssId(e.name)
            out.write('%s {\n' % cssId)
            self._buildStyle(doc, out, e.style)
            out.write('} /* %s */\n\n' % cssId)
            for child in e.getElements():
                self.buildElementStyles(doc, out, child)


