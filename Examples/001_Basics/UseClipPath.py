from pagebot import getContext

#!/usr/bin/env python
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     UseClipPath.py
#
#     Shows how to get different types of contexts.

from pagebot.contexts.platform import getContext

context = getContext()

context.fill((0, 1, 1))
#Deze verandert het clip path
context.rect(80, 80, 400, 400)

path = context.newPath()
path.moveTo((100, 100))
path.lineTo((100, 150))
path.lineTo((200, 200))
path.lineTo((200, 150))
path.lineTo((100, 150))
path.closePath()

context.save()
context.clipPath(path)
context.fill((1, 0, 0, 0.9))
context.rect(150, 150, 600, 600)
context.restore()

context.fill((1, 1, 0, 0.8))
context.rect(400, 20, 300, 400)


