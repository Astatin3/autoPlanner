pg = None
render = None

class menu:
  name = "Menu"

  def __init__(self, tmppg, tmprender):
    global pg
    pg = tmppg
    global render
    render = tmprender

  def mouseDown(self, pos):
    pass

  def mouseUp(self, pos):
    pass

  def mouseMove(self, pos):
    pass

  def doubleClick(self, pos):
    pass

  def load(self):
    render.clear()
    pg.display.update()