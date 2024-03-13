import math
from pygame.locals import *
import numpy as np

curvePointCount = 300
curvePointColor = (255, 255, 0)
curvePointRadius = 2

class pathRenderer():  
  def __init__(self, pg, screen, offsetY):
    self.pg = pg
    self.screen = screen

    self.offsetY = offsetY
    self.width = self.screen.get_width()
    self.height = self.screen.get_width() * (643/1286)
    self.rect = (0, self.offsetY, self.width, self.height)

    self.fieldImg = pg.image.load("frc2024.png").convert_alpha()

    self.offsetSize = self.fieldImg.get_width() / self.width

    self.fieldImg = pg.transform.scale(self.fieldImg, (self.width, self.height))

  def line(self, color, pos1, pos2, width):
     self.pg.draw.line(self.screen, color, pos1, pos2, round(width/self.offsetSize))

  def circle(self, color, pos, radius):
     self.pg.draw.circle(self.screen, color, pos, radius/self.offsetSize)

  def bezier(self, p0, p1, p2):
    #for p in [p0, p1, p2]:
    #    pg.draw.circle(self.screen, (255, 255, 255), p, 5)
    for t in np.arange(0, 1, 1/curvePointCount):
        px = p0[0]*(1-t)**2 + 2*(1-t)*t*p1[0] + p2[0]*t**2
        py = p0[1]*(1-t)**2 + 2*(1-t)*t*p1[1] + p2[1]*t**2
        self.circle(curvePointColor, (px, py), curvePointRadius)
    
  def render(self, nodes, curveEditPoints):
    self.pg.draw.rect(self.screen, (0, 0, 0), self.rect)
    self.screen.blit(self.fieldImg, self.rect)
    for i in range(0,len(curveEditPoints)):
        # self.pg.draw.line(self.screen, lineApproximationLineColor, nodes[i], curveEditPoints[i], lineApproximationLineWidth)
        # self.pg.draw.line(self.screen, lineApproximationLineColor, curveEditPoints[i], nodes[i+1], lineApproximationLineWidth)
        self.bezier(nodes[i], curveEditPoints[i], nodes[i+1])
        # self.pg.draw.circle(self.screen, curveEditPointColor, curveEditPoints[i], curveEditPointRadius)
    self.pg.display.update()
  