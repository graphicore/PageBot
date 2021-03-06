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
#     __init__.py
#
#     New Elements to be added
#     Graphs, Maps, 3Dto2DContainers.
#
from pagebot.elements.element import Element

# Simple elements
from pagebot.elements.pbtext import Text
from pagebot.elements.pbtextbox import TextBox
from pagebot.elements.pbrect import Rect
from pagebot.elements.pbgroup import Group
from pagebot.elements.pbline import Line
from pagebot.elements.pbruler import Ruler
from pagebot.elements.pbpolygon import Polygon
from pagebot.elements.pboval import Oval
from pagebot.elements.pboval import Circle

# Page elements
from pagebot.elements.pbimage import Image
from pagebot.elements.pbgalley import Galley
from pagebot.elements.pbpage import Page, Template
from pagebot.elements.pbpage import Page, Template
from pagebot.elements.pbplacer import Placer # Place holder element, typically for Templates.

# Path and mask elements
from pagebot.elements.paths.pbpath import Path
from pagebot.elements.paths.glyphpath import GlyphPath

# Table elements
from pagebot.elements.pbtable import Table

# Views and code
from pagebot.elements.views import viewClasses
from pagebot.elements.pbquire import Quire
from pagebot.elements.pbcodeblock import CodeBlock

#   S H O R T  C U T S  F O R  C H I L D  E L E M E N T S  G E N E R A T O R S

def newView(viewId, **kwargs):
    """In most cases views are initialized as dictionary by the Document class.
    But since they inherit from Element, they also can be used as placable
    elements. Make sure to define the right parent (likely to be a Page or
    Template)."""
    return viewClasses[viewId](**kwargs)

def newPage(**kwargs):
    """In most cases views are initialized as dictionary by the Document class.
    But since they inherit from Element, they also can be used as placable
    elements. Make sure to define the right parent (likely to be a Page or
    Template). Embed the page in a View element, to control appearance, such as
    cropmarks."""
    return Page(**kwargs)

def newTemplate(**kwargs):
    """In most cases views are initialized as dictionary by the Document class.
    But since they inherit from Element, they also can be used as placable
    elements."""
    return Template(**kwargs)

def newPlacer(**kwargs):
    """Placer occupying a space on Page or Template. Is not visible exported
    documets."""
    return Placer(**kwargs)

def newTextBox(bs='', **kwargs):
    """Caller must supply formatted string. Note that w and h can also be
    defined in the style."""
    return TextBox(bs, **kwargs)

def newText(bs='', **kwargs):
    """Draw formatted string. Normally we don't need w and h here, as it is
    made by the text and style combinations. But in case the defined font is a
    Variable Font, then we can use the width and height to interpolate a font
    that fits the space for the given string and weight. Caller must supply
    formatted string. Support both (x, y) and x, y as position."""
    return Text(bs, **kwargs)

def newRect(**kwargs):
    """Draw the rectangle. Note that points can also be defined in the style.
    When omitted, a square is drawn."""
    return Rect(**kwargs)

def newGroup(**kwargs):
    """Create a new group. Note that points can also be defined in the style.
    When omitted, a square is drawn."""
    return Group(**kwargs)

def newOval(**kwargs):
    """Draw the oval. Note that points can also be defined in the style."""
    return Oval(**kwargs)

def newCircle(**kwargs):
    """Draw the circle. Note that points can also be defined in the style."""
    return Circle(**kwargs)

def newLine(**kwargs):
    return Line(**kwargs)

def newPolygon(points=None, **kwargs):
    return Polygon(points=points, **kwargs)

def newRuler(**kwargs):
    return Ruler(**kwargs)

def newImage(path, **kwargs):
    """Create Image element as position (x, y) and optional width, height (w,
    h) of which at least one of them should be defined. The path can be None,
    to be filled later. If the image is drawn with an empty path, a
    missingImage cross-frame is shown. The optional imo attribute is an
    ImageObject() with filters in place. The Image element is answered for
    convenience of the caller."""
    return Image(path, **kwargs)

def newTable(cols=1, rows=1, **kwargs):
    """Answer a new Table instanec."""
    return Table(rows=rows, cols=cols, **kwargs)

def newGalley(**kwargs):
    """Answer a new Galley instance."""
    return Galley(**kwargs)
