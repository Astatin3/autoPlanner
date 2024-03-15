import math

render = None
pathEditor = None
bottomBarRect = None

ogNodes = []
ogCtrlNodes = []
ogRotNodes = []

keyFrames = []

matchLength = 15
matchTicks = 15 * 50
displayTickResolution = 4
displayTicks = round(matchTicks / displayTickResolution)

dragFrameIndex = -1
ogDragFramePos = -1

selFrame = -1



def getPosKeyframes():
  frames = []
  for keyFrame in keyFrames:
    if keyFrame['type'] == 'position':
      frames.append(keyFrame)
  return frames



def getKeyframeAtPos(index):
  for frame in keyFrames:
      if frame["timeIndex"] == index:
        return frame
  return None



def getPosKeyframeAtPos(index):
  for frame in keyFrames:
    if frame["timeIndex"] == index and frame['type'] == 'position':
      return frame
  return None



def getBezierPointCounts():
  counts = []
  frames = getPosKeyframes()
  for i in range(1,len(frames)):
    counts.append(frames[i]['timeIndex'] - frames[i-1]['timeIndex'])
  return counts



def getPosKeyframeByIndex(index):
  for frame in keyFrames:
    if frame["index"] == index and frame['type'] == 'position':
      return frame
  return None



def getFrameIndex(frame):
  if frame == None:
    return -1
  return keyFrames.index(frame)



def getSurroundingPosFrames(index):
  prevFrame = None
  for i in range(index,-1,-1):
    frame = getPosKeyframeAtPos(i)
    if frame != None and (dragFrameIndex == -1 or not frame == keyFrames[dragFrameIndex]):
      prevFrame = frame
      break
  nextFrame = None
  for i in range(index,displayTicks,1):
    frame = getPosKeyframeAtPos(i)
    if frame != None and (dragFrameIndex == -1 or not frame == keyFrames[dragFrameIndex]):
      nextFrame = frame
      break
    
  if nextFrame == None and prevFrame == None:
      return prevFrame, nextFrame
  # elif nextFrame == None:
  #   return prevFrame, prevFrame
  # elif prevFrame == None:
  #   return nextFrame, nextFrame
  
  return prevFrame, nextFrame



def getRobotAtIndex(index):
  prevFrame, nextFrame = getSurroundingPosFrames(index)
  
  if prevFrame == None:
    return nextFrame['position'], nextFrame['rotation']
  elif nextFrame == None:
    return prevFrame['position'], prevFrame['rotation']
  elif nextFrame['timeIndex'] - prevFrame['timeIndex'] == 0:
    return prevFrame['position'], prevFrame['rotation']
  
  relPos = -((prevFrame['timeIndex'] - index)/(nextFrame['timeIndex'] - prevFrame['timeIndex']))
  
  pos = calcBezierPoint(prevFrame['position'], ogCtrlNodes[prevFrame['index']], nextFrame['position'], relPos)

  if prevFrame['rotation'] - nextFrame['rotation'] < -math.pi:
    rot = ((nextFrame['rotation']-prevFrame['rotation']-math.pi*2)*relPos) + prevFrame['rotation']
  elif prevFrame['rotation'] - nextFrame['rotation'] > math.pi:
    rot = ((nextFrame['rotation']-prevFrame['rotation']+math.pi*2)*relPos) + prevFrame['rotation']
  else:
    rot = ((nextFrame['rotation']-prevFrame['rotation'])*relPos) + prevFrame['rotation']
  
  # diff = (nextFrame['rotation']-prevFrame['rotation'])
  # if diff >= math.pi:
  #   rot = ((nextFrame['rotation']-prevFrame['rotation']-math.pi*2)*relPos) + prevFrame['rotation']
  # elif diff <= math.pi:
  #   rot = ((nextFrame['rotation']-prevFrame['rotation']+math.pi*2)*relPos) + prevFrame['rotation']
  # else:
  #   rot = ((nextFrame['rotation']-prevFrame['rotation'])*relPos) + prevFrame['rotation']

  
  return pos, rot
    


def getTimeBarColor(index):
  frame = getKeyframeAtPos(index)
  if frame == None:
    return (0,0,0)
  if frame['type'] == 'position':
    return (127,127,0)
  elif frame['type'] == 'controller':
    return (127,0,127)
      
  return (16,16,32)



def calcBezierPoint(p0, p1, p2, t):
  px = p0[0]*(1-t)**2 + 2*(1-t)*t*p1[0] + p2[0]*t**2
  py = p0[1]*(1-t)**2 + 2*(1-t)*t*p1[1] + p2[1]*t**2
  return (px, py)




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
      if dragFrameIndex != -1 and getKeyframeAtPos(i) == None:
        if keyFrames[dragFrameIndex]['type'] == 'position':
          prevFrame, nextFrame = getSurroundingPosFrames(ogDragFramePos)
          
          # print(prevFrame['timeIndex'] == nextFrame['timeIndex'])
          if prevFrame == nextFrame: 
            pass
          elif prevFrame == None:
            if i < nextFrame['timeIndex']:
              keyFrames[dragFrameIndex]['timeIndex'] = i
          elif nextFrame == None:
            if i > prevFrame['timeIndex']:
              keyFrames[dragFrameIndex]['timeIndex'] = i
          elif i > prevFrame['timeIndex'] and i < nextFrame['timeIndex']:
            keyFrames[dragFrameIndex]['timeIndex'] = i
            
        else:
          keyFrames[dragFrameIndex]['timeIndex'] = i
    else:
      color = (color[0]+16+(toggle*16),color[1]+16+(toggle*16),color[2]+32+(toggle*16))
      
    toggle = not toggle
    
    render.drawrect(color, rect)
    # renderSelectIndicator(i)
  render.update()



def clickBar(pos, doubleClick):
  for i in range(displayTicks):
    x1 = i * (render.width/(displayTicks))
    x2 = (render.width/(displayTicks))
    rect = (x1, bottomBarRect[1], x2, bottomBarRect[3])
    
    if render.isInRect(pos, rect):
      global selFrame
      global dragFrameIndex
      global ogDragFramePos
      selFrame = i
      if not doubleClick and dragFrameIndex == -1:
        dragFrameIndex = getFrameIndex(getKeyframeAtPos(i))      
        ogDragFramePos = i
      if doubleClick and getKeyframeAtPos(i) == None:
        keyFrames.append({
          'type': 'controller',
          'timeIndex': i
        })
      return
    
class buttonEditor:
  name = "Button Editor"

  def __init__(self, tmprender, tmppathEditor):
    global render
    global pathEditor
    render = tmprender
    pathEditor = tmppathEditor
    
    global indicatorBarHeight
    indicatorBarHeight = round(render.screen.get_width()/displayTicks)
    
    global bottomBarRect
    bottomBarRect = (0, (render.screen.get_height()-render.bottomBarHeight), render.screen.get_width(), render.bottomBarHeight)

    

  def refresh(self):
    global ogNodes
    global ogCtrlNodes
    global ogRotNodes
    
    render.clear()
    render.drawField()
    
    pointCounts = getBezierPointCounts()
    for i in range(0,len(ogCtrlNodes)):
      render.bezier(ogNodes[i], ogCtrlNodes[i], ogNodes[i+1], pointCounts[i])
    
    if selFrame != -1 and len(ogNodes) > 0:
      pos, rot = getRobotAtIndex(selFrame)
      render.robotSquare(pos, rot)
    
    reloadBar((0,0))
    render.update()
          
    

  def mouseDown(self, pos):
    if pos[1] > bottomBarRect[1]:
      clickBar(pos, False)
      self.refresh()

    

  def mouseUp(self, pos):
    global dragFrameIndex
    if dragFrameIndex != -1:
      dragFrameIndex = -1
      ogDragFramePos = -1
      self.refresh()
      reloadBar((0, 0))

    

  def mouseMove(self, pos):
    global dragFrameIndex
    if dragFrameIndex != -1 or pos[1] > bottomBarRect[1]:
      reloadBar(pos)
    # if pos[1] > bottomBarRect[1]:

    

  def doubleClick(self, pos):
    if pos[1] > bottomBarRect[1]:
      clickBar(pos, True)
      self.refresh()

    

  def keyDown(self, key):
    global selFrame
    if key == render.pg.K_LEFT and selFrame > 0:
      selFrame -= 1
      self.refresh()
    elif key == render.pg.K_RIGHT and selFrame < displayTicks-1:
      selFrame += 1
      self.refresh()
        
    

  def updateNodes(self, loadKeyframes):
    global ogNodes
    global ogCtrlNodes
    global ogRotNodes
    ogNodes = pathEditor.nodes.copy()
    ogCtrlNodes = pathEditor.curveEditPoints.copy()
    ogRotNodes = pathEditor.nodeRotations.copy()
    
    if not loadKeyframes:
      return
    
    for i in range(len(ogNodes)):
      frame = getPosKeyframeByIndex(i)
      frame['position'] = ogNodes[i]
      frame['rotation'] = ogRotNodes[i]

    

  def load(self):
    global selFrame
    selFrame = -1
    
    global ogNodes
    global ogCtrlNodes
    global ogRotNodes
    
    if len(ogNodes) != len(pathEditor.nodes):
      
      global keyFrames
      keyFrames = []
      
      self.updateNodes(False)
      
      for i in range(len(ogNodes)):
        if len(ogNodes) == 1:
          timeIndex = 0
        else:
          timeIndex = round((i)/(len(ogNodes)-1) * (displayTicks-1))
        keyFrames.append({
          "type": "position",
          "timeIndex": timeIndex,
          "index": i,
          "position": ogNodes[i],
          "rotation": ogRotNodes[i]
        })
      # print(keyFrames)
    else:
      self.updateNodes(True)
      
    self.refresh()