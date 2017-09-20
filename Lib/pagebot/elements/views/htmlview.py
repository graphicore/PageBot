# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     htmlview.py
#
from pagebot.builders import WebBuilder
from pagebot.elements.views import View

class HtmlView(View):
    u"""Abstract class for HTML/CSS generating views."""

    # Postfix for self.build_html method names. 
    buildType = 'html' 
    # Postfix for self.s_html storage of formatted strings in TextBox.
    stringType = 'html'

    b = WebBuilder() # self.b builder for this view.

