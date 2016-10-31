# -*- coding: UTF-8 -*-

class Composer(object):
    def __init__(self, document):
        self.document = document
        self.gState = [document.getRootStyle()] # State of current state of (font, fontSize)

    def typeset(self, page, tb):
        u"""Typeset the text in the textbox tb. Since we are adding to the galley, the textBox
        can have infinite length."""
        overflow = tb.typeset(page, fs)
        if overflow: # Any overflow from typesetting in the text box, then find new from page/flow
            page, tb = page.getNextFlowBox(tb)
            assert tb is not None # If happes, its a mistake in one of the templates.
            #print u'++++%s++++' % fs
            #print u'====%s====' % overflow
            fs = overflow
        return page, tb, fs
    
      