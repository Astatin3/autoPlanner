import math
import pygame as pg
from pygame.locals import *
from sys import exit
import numpy as np

doubleClickDuration = 200

nodeColor = (255, 255, 255)
nodeRadius = 15

lineApproximationLineColor = (127, 127, 127, 0.5)
lineApproximationLineWidth = 3

curvePointCount = 300
curvePointColor = (255, 255, 0)
curvePointRadius = 2

curveEditPointColor = (0, 255, 255)
curveEditPointRadius = 5

pg.init()

# fieldImg = Background("frc2024.png", (0, 0))

fieldImg = pg.image.load("frc2024.png")

screen_width = fieldImg.get_width()
screen_height = fieldImg.get_height()

screen = pg.display.set_mode((screen_width, screen_height))
fieldImg = pg.image.load("frc2024.png").convert_alpha()
pg.display.set_caption("Auto Planner")


curveEditPoints = []
nodes = []

def addNode(pos):
    nodes.append(pos)
    if len(nodes) > 1:
        index = len(nodes)-1
        # Middle point between current point and previous point
        editPos = (nodes[index-1][0]+pos[0])/2,(nodes[index-1][1]+pos[1])/2
        curveEditPoints.append(editPos)

def bezier(p0, p1, p2):
    #for p in [p0, p1, p2]:
    #    pg.draw.circle(screen, (255, 255, 255), p, 5)
    for t in np.arange(0, 1, 1/curvePointCount):
        px = p0[0]*(1-t)**2 + 2*(1-t)*t*p1[0] + p2[0]*t**2
        py = p0[1]*(1-t)**2 + 2*(1-t)*t*p1[1] + p2[1]*t**2       
        pg.draw.circle(screen, curvePointColor, (px, py), curvePointRadius) 
    
def refresh():
    pg.draw.rect(screen, (0, 0, 0), (0, 0, screen_width, screen_height))
    screen.blit(fieldImg, screen.get_rect())
    for i in range(0,len(curveEditPoints)):
        pg.draw.line(screen, lineApproximationLineColor, nodes[i], curveEditPoints[i], lineApproximationLineWidth)
        pg.draw.line(screen, lineApproximationLineColor, curveEditPoints[i], nodes[i+1], lineApproximationLineWidth)
        bezier(nodes[i], curveEditPoints[i], nodes[i+1])
        pg.draw.circle(screen, curveEditPointColor, curveEditPoints[i], curveEditPointRadius)
    for pos in nodes:
        pg.draw.circle(screen, nodeColor, pos, nodeRadius)
    pg.display.update()

def getElemAt(pos):
    for i in range(0,len(curveEditPoints)):
        if getDist(pos, curveEditPoints[i], curveEditPointRadius):
            return 1, i
    for i in range(0,len(nodes)):
        if getDist(pos, nodes[i], nodeRadius):
            return 0, i
    return -1, -1

def getDist(pos1, pos2, dist):
    return math.sqrt(math.pow(pos1[0]-pos2[0], 2) + math.pow(pos1[1]-pos2[1], 2)) <= dist

def singleClick():
    pos = pg.mouse.get_pos()
    addNode(pos)
    refresh()

def doubleClick():
    curveEditPoints = []
    nodes = []
    refresh()

refresh()

running = True
last_click = -1

clickType = -1
clickIndex = -1

while running:
    for event in pg.event.get():
        
        if event.type == pg.MOUSEBUTTONDOWN:
            clickType, clickIndex = getElemAt(pg.mouse.get_pos())
            
            now = pg.time.get_ticks()
            if now - last_click <= doubleClickDuration:
                if clickType == -1:
                    pass
                if clickType == 0:
                    print(nodes)
                    if clickIndex > 0:
                        if clickIndex < len(nodes)-1:
                            newPos = (nodes[clickIndex-1][0]+nodes[clickIndex][0])/2,(nodes[clickIndex-1][1]+nodes[clickIndex][1])/2
                            curveEditPoints[clickIndex] = newPos
                        curveEditPoints.pop(clickIndex-1)
                    elif clickIndex == 0 and len(nodes) > 1:
                        curveEditPoints.pop(clickIndex)
                    # if len(nodes) != 1:
                    nodes.pop(clickIndex)
                    # else: nodes = []
                    refresh()
                    
                    
            else:
                if clickType == -1:
                    singleClick()
            last_click = pg.time.get_ticks()
        
        if event.type == pg.MOUSEMOTION and clickType != -1:
            if clickType == 0:
                nodes[clickIndex] = pg.mouse.get_pos()
            if clickType == 1:
                curveEditPoints[clickIndex] = pg.mouse.get_pos()
            refresh()
        
        if event.type == pg.MOUSEBUTTONUP:
            if clickType != -1:
                clickType = -1
                clickIndex = -1

        if event.type == pg.QUIT:
            running = False
pg.quit()
