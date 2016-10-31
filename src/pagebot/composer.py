# -*- coding: UTF-8 -*-

from drawBot import *

class Composer(object):
    def __init__(self, document):
        self.document = document

    def compose(self, galley, page, flowId):
        u"""Compose the galley element, starting with the flowId text box on page.
        The composer negotiates between what the galley needs a sequential space
        for its elements, and what the page has to offer."""
        tb = page.getElement(flowId) # Find the seed text box on the page, as derived from template.
        assert tb is not None # Otherwise there is a template error.
        elements = galley.getElements()
        # Keeping overflow of text boxes here while iterating.
        fs = None
        assert elements is not None # Otherwise we did not get a galley here.
        for element in elements:
            if fs is None:
                fs = FormattedString()
            eFs = element.getFs()
            if eFs is None: # This is a non-text element. Try to find placement.
                self.tryPlacement(element, page)
                continue
            fs += eFs # Add element string to the overflow we already had.
            # As long a s where is text, try to fit into the boxes on the page.
            # Otherwise go to the next page, following the flow.
            while 0 and fs:
                fs = tb.append(fs)
                if fs:
                    # Overflow in this text box, find new from (page, tbFlow)
                    newPage, tb = page.getNextFlowBox(tb)
                    print page, newPage, tb
                    assert tb is not None # If happens, its a mistake in one of the templates.

    def tryPlacement(self, element, page):
        pass # Don't place for now.
