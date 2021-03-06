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
#     codeblock.py
#
from pagebot.elements.element import Element
#from pagebot.constants import ORIGIN
#from pagebot.toolbox.units import pointOffset

class CodeBlock(Element):

    def __init__(self, code, tryExcept=True, **kwargs):
        Element.__init__(self, **kwargs)
        assert isinstance(code, str)
        self.code = code
        self.tryExcept = tryExcept

    def __repr__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.code.replace('\n',';')[:200])

    def run(self, globals=None, verbose=False):
        """Execute the code block. Answer a set of compiled methods, as found in the <code class="Python">...</code>,
        made by Markdown with
        ~~~
        cid = 'NameOfBlock'
        doc = Document(w=300, h=500)
        ~~~
        block code. In this case the MacDown and MarkDown extension libraries
        convert this codeblock to
        <pre><code>
        cid = 'NameOfBlock'
        doc = Document(w=300, h=500)
        </code></pre>
        This way authors can run PageBot generators controlled by content.
        Note that it is the author's responsibility not to overwrite global values
        that are owned by the calling composer instance.

        >>> from pagebot.document import Document
        >>> doc = Document(size=(500, 500), autoPages=10)
        >>> view = doc.view
        >>> page = doc[1]
        >>> code = 'a = 100 * 300\\npage = page.next.next.next\\npage.w = 300'
        >>> cb = CodeBlock(code, parent=page, tryExcept=False)
        >>> cb
        <CodeBlock:a = 100 * 300;page = page.next.next.next;page.w = 300>
        >>> # Create globals dictionary for the script to work with
        >>> g = dict(page=page, view=view, doc=doc)
        >>> result = cb.run(g) # Running the code selects 3 pages ahead
        >>> result is g # Result global dictionary is same object as g
        True
        >>> sorted(result.keys())
        ['__code__', 'a', 'doc', 'page', 'view']
        >>> resultPage = result['page']
        >>> resultPage # Running code block changed width of new selected page.
        <Page:default 4 (300pt, 500pt)>
        >>> resultPage.w, resultPage.pn
        (300pt, (4, 0))
        >>> cb.code = 'aa = 200 * a' # Change code of the code block, using global
        >>> result = cb.run(g) # And run with the same globals dictionary
        >>> sorted(result.keys()), g['aa'] # Result is added to the globals
        (['__code__', 'a', 'aa', 'doc', 'page', 'view'], 6000000)
        """
        if globals is None:
            # If no globals defined, create a new empty dictionary as storage of result.
            globals = {}
        if not self.tryExcept: # For debugging show full error of code block run.
            exec(self.code, globals) # Exectute code block, where result goes dict.
            if '__builtins__' in globals:
                del globals['__builtins__'] # We don't need this set of globals in the returned results.
        else:
            error = None
            try:
                exec(self.code, globals) # Exectute code block, where result goes dict.
                if '__builtins__' in globals:
                    del globals['__builtins__'] # We don't need this set of globals in the results.
            except TypeError:
                error = u'TypeError'
            except NameError:
                error = 'NameError'
            except SyntaxError:
                error = 'SyntaxError'
            except AttributeError:
                error = 'AttributeError'
            globals['__error__'] = error
            if error is not None:
                print(u'### %s ### %s' % (error, self.code))
            # TODO: insert more possible exec() errors here.

        # For convenience, store the last source code of the block in the result dict.
        if '__code__' not in globals:
            globals['__code__'] = self.code

        return globals # Answer the globals attribute, in case it was created.

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
