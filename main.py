import math
import pygame as pg
from pygame.locals import *
from sys import exit
import numpy as np

import src.render as render
import src.menu as menu
import src.pathEditor as pathEditor

doubleClickDuration = 200

pg.init()
pg.font.init()

topBarHeight = 40
bottomBarHeight = 40

screen_width = 1200
screen_height = (screen_width * (643/1286)) + topBarHeight + bottomBarHeight

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Auto Planner")

pathR = render.render(pg, screen, topBarHeight)

tabIndex = 1

tabs = [
    menu.menu(pg, pathR),
    pathEditor.pathEditor(pg, pathR)
]

def isInRect(pos, rect):
    return pos[0] >= rect[0] and \
            pos[0] <= rect[2] and \
            pos[1] >= rect[1] and \
            pos[1] <= rect[3]

def refreshTabs(pos):
    for i in range(len(tabs)):
        
        # color = i * (255/(len(tabs)-1))
        # color = (color, color, color)
        
        x1 = i * (screen_width/(len(tabs)))
        x2 = (i+1) * (screen_width/(len(tabs)))
        rect = (x1, 0, x2, topBarHeight)

        if i == tabIndex:
            color = (255, 255, 255)
        elif isInRect(pos, rect):
            color = (127,127,127)
        else:
            color = (63,63,63)
        
        pg.draw.rect(screen, color, rect)
    pg.display.update()

refreshTabs((screen_width/2, screen_height/2))

running = True
last_click = -1

def offsetPos(pos):
    return (pos[0],pos[1])

while running:
    for event in pg.event.get():
        
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            if pos[1] > topBarHeight:
                now = pg.time.get_ticks()
                if now - last_click <= doubleClickDuration:
                    tabs[tabIndex].doubleClick(offsetPos(pos))   
                else:
                    tabs[tabIndex].mouseDown(offsetPos(pos))
                last_click = pg.time.get_ticks()
            
        if event.type == pg.MOUSEMOTION:
            pos = pg.mouse.get_pos()
            if pos[1] > topBarHeight:
                tabs[tabIndex].mouseMove(offsetPos(pos))
            refreshTabs(pos)
        
        if event.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()
            if pos[1] > topBarHeight:
                tabs[tabIndex].mouseUp(offsetPos(pos))

        if event.type == pg.QUIT:
            running = False
            
pg.quit()
