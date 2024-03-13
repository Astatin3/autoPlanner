import math
import pygame as pg
from pygame.locals import *
from sys import exit
import numpy as np

import src.pathRenderer as pathRenderer
import src.pathEditor as pathEditor

doubleClickDuration = 200

pg.init()

topBarHeight = 40
bottomBarHeight = 40

screen_width = 1200
screen_height = (screen_width * (643/1286)) + topBarHeight + bottomBarHeight

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Auto Planner")

pathR = pathRenderer.pathRenderer(pg, screen, topBarHeight)

tabIndex = 0

tabs = [
    pathEditor.pathEditor(pg, pathR)
]

def refresh():
    pass

running = True
last_click = -1

# clickType = -1
# clickIndex = -1

def offsetPos(pos):
    return (pos[0],pos[1])

while running:
    for event in pg.event.get():
        
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            if pos[1] > topBarHeight and pos[1] < (screen.get_width()-bottomBarHeight):
                now = pg.time.get_ticks()
                if now - last_click <= doubleClickDuration:
                    tabs[tabIndex].doubleClick(offsetPos(pos))   
                else:
                    tabs[tabIndex].mouseDown(offsetPos(pos))
                last_click = pg.time.get_ticks()
            
        if event.type == pg.MOUSEMOTION:
            pos = pg.mouse.get_pos()
            if pos[1] > topBarHeight and pos[1] < (screen.get_width()-bottomBarHeight):
                tabs[tabIndex].mouseMove(offsetPos(pos))
        
        if event.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()
            if pos[1] > topBarHeight and pos[1] < (screen.get_width()-bottomBarHeight):
                tabs[tabIndex].mouseUp(offsetPos(pos))

        if event.type == pg.QUIT:
            running = False
            
pg.quit()
