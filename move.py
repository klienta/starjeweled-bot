class Move:
    def __init__(self, srcX, srcY, desX, desY):
        self.src = {'x': srcX, 'y': srcY}
        self.des = {'x': desX, 'y': desY }
        
    def __str__(self):
      return "(%d, %d) to (%d, %d)" % (self.src['x'], self.src['y'], self.des['x'], self.des['y'])