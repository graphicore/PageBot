# -*- coding: UTF-8 -*-

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
        assert elements is not None # Otherwise we did not get a galley here.
        for element in elements:
            fs = element.getFs()
            if fs is None: # This is a non-text element. Try to find placement.
                self.tryPlacement(element, page)
                continue
            # As long a s where is text, try to fit into the boxes on the page.
            # Otherwise go to the next page, following the flow.
            while fs:
                
        """
        overflow = tb.typeset(page, fs)
        if overflow: # Any overflow from typesetting in the text box, then find new from page/flow
            page, tb = page.getNextFlowBox(tb)
            assert tb is not None # If happes, its a mistake in one of the templates.
            #print u'++++%s++++' % fs
            #print u'====%s====' % overflow
            fs = overflow
        return page, tb, fs
        """

    def tryPlacement(self, element, page):
        pass # Don't place for now.
