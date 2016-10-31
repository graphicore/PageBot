# -*- coding: UTF-8 -*-

class TypeSetter(object):
    
    def __init__(self, galley):
        self.galley = galley
                     
    def node_h1(self, node, page, style):
        u"""Collect the page-node-pageNumber connection."""
        # Add line break to whatever style/content there was before. 
        # Add invisible h2-marker in the string, to be retrieved by the composer.
        tb = self.getTextBox(style)
        tb.append('\n')# + getMarker(node.tag) 
        self.typesetNode(node, page, style)

    def node_h2(self, node, page, style):
        u"""Collect the page-node-pageNumber connection."""
        # Add line break to whatever style/content there was before. 
        # Add invisible h2-marker in the string, to be retrieved by the composer.
        tb = self.getTextBox(style)
        tb.append('\n')# + getMarker(node.tag) 
        self.typesetNode(node, page, style)
        

    def node_h3(self, node, page, style):
        u"""Collect the page-node-pageNumber connection."""
        # Add line break to whatever style/content there was before. 
        # Add invisible h3-marker in the string, to be retrieved by the composer.
        tb = self.getTextBox(style)
        tb.append('\n')# + getMarker(node.tag) 
        self.typesetNode(node, page, style)
        
    def node_h4(self, node, page, style):
        u"""Collect the page-node-pageNumber connection."""
        # Add line break to whatever style/content there was before. 
        # Add invisible h3-marker in the string, to be retrieved by the composer.
        tb = self.getTextBox(style)
        tb.append('\n')# + getMarker(node.tag) 
        self.typesetNode(node, page, style)

    def node_br(self, node, page, style):
        u"""Add line break to the formatted string."""
        tb = self.getTextBox(style)
        tb.append('\n')# + getMarker(node.tag) 

    def node_a(self, node, page, style):
        u"""Ignore links, but process the block"""
        return self.typesetNode(node, page, style)
        
    def node_sup(self, node, page, style):
        u"""Collect footnote refereneces on their page number. 
        And typeset the superior footnote index reference."""
        nodeId = node.attrib.get('id')
        if nodeId.startswith('fnref'): # This is a footnote reference.
            footnotes = self.document.footnotes
            footnotes[len(footnotes)+1] = [node, page, style]      
        return self.typesetNode(node, page, style)
 
    def node_literatureref(self, node, page, style):
        u"""Collect literature references."""
        return self.typesetNode(node, page, style)
         
    def node_div(self, node, page, style):
        u"""MarkDown generates <div class="footnote">...</div> and <div class="literature">...</div>
        as output, but we will handle them separetely by looking them up in the XML-tree.
        So we'll skip them in the regular flow process."""
        # TODO: Check specific on the class name. Process otherwise.
        tb = self.getTextBox(style)
        if node.attrib.get('class') == 'literature':
            return
        elif node.attrib.get('class') == 'footnote':
            # Find the content of the footnotes.
            #node.findall('./ol/li/p')
            #for index, p in enumerate(node.findall('./ol/li/p')):
            #    self.document.footnotes[index+1].append(p)
            return
        return self.typesetNode(node, page, style)
                    
    def node_li(self, node, page, style):
        # Bullet/Numbered list item
        tb = self.getTextBox(style)
        tb.append(getFormattedString(u'\n•\t', style))
        self.typesetNode(node, page, style)
                  
    def node_img(self, node, page, style):
        u"""Process the image. Find empty space on the page to place it,
        closest related to the w/h ration of the image."""
        src = node.attrib.get('src')
        imageElement = page.findImageElement(0, 0)
        if imageElement is not None:
            g = Galley()
            imageElement.setPath(src) # Set path, image w/h and image scale.
            imgStyle = self.pushStyle(page.getStyle(node.tag))
            imageElement.fill = imgStyle.fill
            imageElement.stroke = imgStyle.stroke
            imageElement.strokeWidth = imgStyle.strokeWidth
            imageElement.hyphenation = imgStyle.hyphenation
            g.append(imageElement)
            if caption is not None:
                captionStyle = self.pushStyle(page.getStyle('caption'))
                tb = g.getTextBox()
                caption = node.attrib.get('title')
                # Add invisible marker to the FormattedString, to indicate where the image
                # reference went in a textBox after slicing the string.
                tb.append(getFormattedString(caption+'\n', captionStyle))
                tb.append(getMarker(node.tag, src))
                self.popStyle() # captionStyle
            self.galley.append(g)
        else:
            fs += FormattedString('\n[Could not find space for image %s]\n' % src, fill=(1, 0, 0))
                                    
    def pushStyle(self, style):
        u"""As we want cascading font and fontSize in the page elements, we need to keep track
        of the stacking of XML-hiearchy of the tag styles.
        The styles can omit the font or fontSize, and still we need to be able to set the element
        attributes. Copy the current style and add overwrite the attributes in style. This way
        the current style always contains all attributes of the root style."""
        nextStyle = copy.copy(self.gState[-1])
        if style is not None:
            for name, value in style.__dict__.items():
                if name.startswith('_'):
                    continue
                setattr(nextStyle, name, value)
        self.gState.append(nextStyle)
        return nextStyle
        
    def popStyle(self):
        self.gState.pop()
        return self.gState[-1]

    def typeset(self, fs):
        tb = self.galley.getTextBox()
        tb.append(fs)
        
    def typesetNode(self, node, page, style=None):

        if style is None:
            style = page.getStyle(node.tag)
        style = self.pushStyle(style)

        if fs is None:
            fs = getFormattedString('', style)
        
        nodeText = node.text
        if nodeText is not None:
            if style.stripWhiteSpace:
                nodeText = nodeText.strip() #+ style.stripWhiteSpace
            if nodeText: # Anythong left to add?
                #print node.tag, `node.text`
                fs += getFormattedString(nodeText, style)
            # Handle the block text of the tag, add to the latest textBox in the galley.
            self.typeset(page, fs)
            
        # Type set all child node in the current node, by recursive call.
        for child in node:
            hook = 'node_'+child.tag
            # Method will handle the styled body of the element, but not the tail.
            if hasattr(self, hook): 
                page, tb, fs = getattr(self, hook)(child, page, tb, fs)
                childTail = child.tail
                if childTail is not None:
                    if style.stripWhiteSpace:
                        childTail = childTail.strip() #+ style.stripWhiteSpace
                    if childTail: # Anything left to add?
                        #print child.tag, `child.tail`
                        fs += getFormattedString(childTail, style)
                # Handle the tail text of the tag.
                page, tb, fs = self.typeset(page, tb, fs)
                
            else: # If no method hook defined, then just solve recursively.
                page, tb, fs = self.typesetNode(child, page, tb, fs)

        # XML-nodes are organized as: node - node.text - node.children - node.tail
        # If there is no text or if the node does not have tail text, these are None.
        # Restore the graphic state at the end of the element content processing to the 
        # style of the parent in order to process the tail text.
        style = self.popStyle()
        nodeTail = node.tail
        if nodeTail is not None:
            if style.stripWhiteSpace:
                nodeTail = nodeTail.strip() + style.stripWhiteSpace
            if nodeTail: # Anython left to add?
                #print node.tag, `node.tail`
                fs += getFormattedString(nodeTail, style)
        page, tb, fs = self.typeset(page, tb, fs)
        return page, tb, fs
                         
    def typesetFile(self, fileName, page, flowId='main'):
        u"""Read the XML document and parse it into a tree of document-chapter nodes. Make the typesetter
        start at page pageNumber and find the name of the flow in the page template."""

        self.fileName = fileName
        fileExtension = fileName.split('.')[-1]
        if fileExtension == 'md':
            # If we have MarkDown content, conver to HTNK/XML
            f = codecs.open(fileName, mode="r", encoding="utf-8")
            mdText = f.read()
            f.close()
            mdExtensions = [FootnoteExtension(), LiteratureExtension(), Nl2BrExtension()]
            xml = '<document>%s</document>' % markdown.markdown(mdText, extensions=mdExtensions)
            xmlName = fileName + '.xml'
            f = codecs.open(xmlName, mode="w", encoding="utf-8")
            f.write(xml)
            f.close()
            fileName = xmlName

        tree = ET.parse(fileName)
        root = tree.getroot() # Get the root element of the tree.
        # Get the root style that all other styles will be merged with.
        rootStyle = self.document.getRootStyle()
        # Build the formatted string at the same time as filling the flow columns.
        # This way we can keep track where the elemenets go, e.g. for foot note and image references.
        tb = page.findElement(flowId) # Find the named TextBox in the page/template.
        assert tb is not None # Make sure if it is. Otherwise there is a mistage in the template.
        # Collect all flowing text in one formatted string, while simulating the page/flow, because
        # we need to keep track on which page/flow nodes results get positioned (e.g. for toc-head
        # reference, image index and footnote placement.   
        self.typesetNode(root, page, tb)
        # Now run through the footnotes and typeset them on the pages where the reference is located.
        # There are other options to place footnotes (e.g. at the end of a chapter). Either subclass
        # and rewite self.typesetFootnotes() or implement optional behavior to be selected from the outside.
        #self.typesetFootnotes()
        
    def typesetFootnotes(self):
        footnotes = self.document.footnotes
        for index, (page, e, p) in footnotes.items():
            style = page.getStyle('footnote')
            fs = getFormattedString('%d ' % index, style)
            tb = page.findElement('footnote')
            if tb is not None:
                page, tb, fs = self.typesetNode(p, page, tb, fs, style)

