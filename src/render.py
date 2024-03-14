import math
from pygame.locals import *
import numpy as np

curvePointCount = 300
curvePointColor = (255, 255, 0)
curvePointRadius = 2

selTabBorderSize = 2
selTabBorderIndent = 3

class render():
  def __init__(self, pg, screen, topBarHeight, bottomBarHeight):
    self.pg = pg
    self.screen = screen

    self.topBarHeight = topBarHeight
    self.bottomBarHeight = bottomBarHeight
    
    self.width = self.screen.get_width()
    self.height = self.screen.get_width() * (643/1286)
    self.rect = (0, self.topBarHeight, self.width, self.height+bottomBarHeight)
    
    self.font = self.pg.font.Font(None, 25)

    self.fieldImg = pg.image.load("frc2024.png").convert_alpha()
    self.offsetSize = self.fieldImg.get_width() / self.width
    self.fieldImg = pg.transform.scale(self.fieldImg, (self.width, self.height))
    
    self.elements = []
    
  def line(self, color, pos1, pos2, width):
     self.pg.draw.line(self.screen, color, pos1, pos2, round(width/self.offsetSize))

  def circle(self, color, pos, radius):
     self.pg.draw.circle(self.screen, color, pos, radius/self.offsetSize)

  def drawrect(self, color, rect):
     self.pg.draw.rect(self.screen, color, rect)

  def isInRect(self, pos, rect):
    return pos[0] >= rect[0] and \
            pos[0] <= rect[0]+rect[2] and \
            pos[1] >= rect[1] and \
            pos[1] <= rect[1]+rect[3]


  def bezier(self, p0, p1, p2):
    #for p in [p0, p1, p2]:
    #    pg.draw.circle(self.screen, (255, 255, 255), p, 5)
    for t in np.arange(0, 1, 1/curvePointCount):
        px = p0[0]*(1-t)**2 + 2*(1-t)*t*p1[0] + p2[0]*t**2
        py = p0[1]*(1-t)**2 + 2*(1-t)*t*p1[1] + p2[1]*t**2
        self.circle(curvePointColor, (px, py), curvePointRadius)

  def clear(self):
    self.pg.draw.rect(self.screen, (0, 0, 0), self.rect)

  def drawField(self):
    self.screen.blit(self.fieldImg, self.rect)

  def renderElements(self, pos):
    for elem in self.elements:
      if elem['type'] == 'button':
        # print(elem['getIsSelected']())
        self.renderButton(elem['rect'], elem['text'], elem['getIsSelected'](), pos)

  def clickElement(self, pos):
    for elem in self.elements:
      if elem['type'] == 'button' and self.isInRect(pos, elem['rect']):
        elem['onClick'](pos)

  def renderBezier(self, nodes, curveEditPoints):
    for i in range(0,len(curveEditPoints)):
      self.bezier(nodes[i], curveEditPoints[i], nodes[i+1])

  def update(self):
    self.pg.display.update()
  
  def addButton(self, rect, text, getIsSelected, onClick):
    self.elements.append({
      "type": "button",
      "text": text,
      "getIsSelected": getIsSelected,
      "onClick": onClick,
      "rect": rect
    })
  
  def renderButton(self, rect, text, selected, mousePos):
    
    # print(isInRect(mousePos, rect))
    
    if self.isInRect(mousePos, rect):
      color = (16,64,32)
    else:
      color = (16,16,32)
      
    if selected:
      borderColor = (0,255,0)
    else:
      borderColor = (64,127,127)
  
    text = self.font.render(text, True, (255,255,255))
    text_rect = text.get_rect(center=(rect[0]+(rect[2]/2), rect[1]+(rect[3]/2)))
        
    self.pg.draw.rect(self.screen, color, rect)
    rect = (rect[0]+selTabBorderIndent,rect[1]+selTabBorderIndent,
            rect[2]-selTabBorderIndent*2,rect[3]-selTabBorderIndent*2)
    self.pg.draw.rect(self.screen, borderColor, rect)
    rect = (rect[0]+selTabBorderSize,rect[1]+selTabBorderSize,
            rect[2]-selTabBorderSize*2,rect[3]-selTabBorderSize*2)
    self.pg.draw.rect(self.screen, color, rect)
  
    self.screen.blit(text, text_rect)
    
    self.update()