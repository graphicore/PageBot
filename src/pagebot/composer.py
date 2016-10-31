# -*- coding: UTF-8 -*-

from drawBot import *

class Composer(object):
    def __init__(self, document):
        self.document = document

    def compose(self, galley, page, flowId=None):
        u"""Compose the galley element, starting with the flowId text box on page.
        The composer negotiates between what the galley needs a sequential space
        for its elements, and what the page has to offer.
        If flowId is omitted, then let the page find the entry point for the first flow."""
        if flowId is None:
            flows = page.getFlows()
            assert len(flows) # There must be at least one, otherwise error in template.
            flowId, _ = sorted(flows.keys()) # Arbitrary which one, if there are mulitple entries.
        tb = page.getElement(flowId) # Find the seed flow box on the page, as derived from template.
        assert tb is not None # Make sure, otherwise there is a template error.
        elements = galley.getElements()
        # Keeping overflow of text boxes here while iterating.
        assert elements is not None # Otherwise we did not get a galley here.
        for element in elements:
            continue # SKIP DEBUGGING
            fs = element.getFs()
            if fs is None: # This is a non-text element. Try to find placement.
                self.tryPlacement(element, page)
                continue
            # As long as where is text, try to fit into the boxes on the page.
            # Otherwise go to the next page, following the flow.
            while fs:
                overflow = tb.append(fs)
                if fs == overflow:
                    print u'NOT ABLE TO PLACE %s' % overflow
                    break
                fs = overflow
                if len(fs):
                    # Overflow in this text box, find new from (page, tbFlow)
                    newPage, tb = page.getNextFlowBox(tb)
                    assert tb is not None # If happens, its a mistake in one of the templates.

    def tryPlacement(self, element, page):
        pass # Don't place for now.
