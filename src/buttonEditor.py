render = None
pathEditor = None
bottomBarRect = None

ogNodes = []
ogCtrlNodes = []

events = []

matchLength = 15
matchTicks = 15 * 50
displayTickResolution = 5
displayTicks = round(matchTicks / displayTickResolution)

indicatorBarRect = None

selFrame = -1

# def addTab(i):
#     x1 = i * (render.width/(displayTicks))
#     x2 = (render.width/(displayTicks))
#     rect = (x1, bottomBarRect[1], x2, bottomBarRect[3])
    
#     def getIsSelected():
#       return False
    
#     def onClick(pos):
#       pass
    
#     render.addButton(rect, "", getIsSelected, onClick)

def getTimeBarColor(index):
  for event in events:
    if event["timeIndex"] == index:
      if event['type'] == 'position':
        return (127,127,0)
      elif event['type'] == 'controller':
        return (0,127,0)
      
  return (16,16,32)

def renderSelectIndicator(i):
  x1 = i * (render.width/(displayTicks))
  x2 = (render.width/(displayTicks))
  rect = (x1, indicatorBarRect[1], x2, indicatorBarRect[3])
  
  if i == selFrame:
    render.drawrect((255,0,0), rect)
  

  


def reloadBar(pos):
  toggle = False
  for i in range(displayTicks):
    x1 = i * (render.width/(displayTicks))
    x2 = (render.width/(displayTicks))
    rect = (x1, bottomBarRect[1], x2, bottomBarRect[3])
    
    color = getTimeBarColor(i)
    
    if i == selFrame:
      color = (color[0]+64,color[1]+64,color[2]+64)
    
    if render.isInRect(pos, rect):
      color = (color[0]+64,color[1]+64,color[2]+64)
    else:
      color = (color[0]+16+(toggle*16),color[1]+16+(toggle*16),color[2]+32+(toggle*16))
      
    toggle = not toggle
    
    render.drawrect(color, rect)
    renderSelectIndicator(i)
  render.update()

def clickBar(pos):
  for i in range(displayTicks):
    x1 = i * (render.width/(displayTicks))
    x2 = (render.width/(displayTicks))
    rect = (x1, bottomBarRect[1], x2, bottomBarRect[3])
    
    if render.isInRect(pos, rect):
      global selFrame
      selFrame = i
      reloadBar(pos)
      return
    
class buttonEditor:
  name = "Button Editor"

  def __init__(self, tmprender, tmppathEditor):
    global render
    render = tmprender
    global pathEditor
    pathEditor = tmppathEditor
    
    global indicatorBarRect
    indicatorBarHeight = round(render.screen.get_width()/displayTicks)
    indicatorBarRect = (0, render.screen.get_height()-indicatorBarHeight, render.screen.get_width(), indicatorBarHeight)
    
    global bottomBarRect
    bottomBarRect = (0, (render.screen.get_height()-render.bottomBarHeight), render.screen.get_width(), render.screen.get_height())

  def refresh(self):
    render.clear()
    render.drawField()
    render.renderBezier(pathEditor.nodes, pathEditor.curveEditPoints)
    reloadBar((0,0))
    render.update()
        
  def mouseDown(self, pos):
    if pos[1] > bottomBarRect[1]:
      clickBar(pos)
    pass

  def mouseUp(self, pos):
    pass

  def mouseMove(self, pos):
    reloadBar(pos)

  def doubleClick(self, pos):
    pass

  def keyDown(self, key):
    pass

  def load(self):
    
    global ogNodes
    global ogCtrlNodes
    global selFrame
    selFrame = -1
    
    # for i in range(displayTicks):
    #   addTab(i)
    
    if ogNodes != pathEditor.nodes or \
    ogCtrlNodes != pathEditor.curveEditPoints:
      
      ogNodes = pathEditor.nodes
      ogCtrlNodes = pathEditor.curveEditPoints
      
      # for i in range(len(ogNodes)):
      #   events
      
    self.refresh()