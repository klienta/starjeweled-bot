import mouse
from math import floor
from numpy import arange
import re

class Strategy:
    def __init__(self, board):
      self.board = board
  
    def findNeighborTile(self, color, x, y, directions):
        directions = list(directions)
        print 'inspecting ', x, y, self.board.getTile(x, y, None)
        for dir in directions:
            if dir == 'u':
                if(self.board.tileIsColor(color, x, y - 1)):
                    return {'x':x, 'y':y - 1}
            elif dir == 'r':
                if(self.board.tileIsColor(color, x + 1, y)):
                    return {'x': x + 1, 'y': y}
            elif dir == 'd':
                if(self.board.tileIsColor(color, x, y + 1)):
                    return {'x': x, 'y': y + 1}
            elif dir == 'l':
                if(self.board.tileIsColor(color, x - 1, y)):
                    return {'x': x - 1, 'y': y }
        
    def findMove(self):
        #TODO: fix indention
        
        print "finding moves"
        # look for 4s
        #  xxox
        for m in re.finditer(r'([a-z])\1.\1', self.board.board):
          color = m.group(0)[:1]
          x = m.start() % self.board.num_rows
          y = int(floor(m.start() / self.board.num_rows))
    
          #check that two blocks are on the same row
          if(floor((m.start() + 3) / 8) != y):
            continue
    
          print 'found potential 4 ', x, y, m.group(0)
    
          neighborTile = self.findNeighborTile(color, x + 2, y, 'ud')
          if(neighborTile):
            return Move(neighborTile['x'], neighborTile['y'], x + 2, y)
    
        # look for 4s
        #  xoxx
        for m in re.finditer(r'([a-z]).\1\1', self.board.board):
          color = m.group(0)[:1]
          x = m.start() % self.board.num_rows
          y = int(floor(m.start() / self.board.num_rows))
    
          #check that two blocks are on the same row
          if(floor((m.start() + 3) / 8) != y):
            continue
    
          print 'found potential 4 ', x, y, m.group(0)
    
          neighborTile = self.findNeighborTile(color, x + 1, y, 'ud')
          if(neighborTile):
            return Move(neighborTile['x'], neighborTile['y'], x + 1, y)
    
        # Check for Horizontal Blocks
        #  1  4
        # 3oxxo6
        #  2  5
        print 'finding moves on ', self.board.board
        for m in re.finditer(r'([a-z])\1', self.board.board):
          color = m.group(0)[:1]
          x = m.start() % self.board.num_rows
          y = int(floor(m.start() / self.board.num_rows))
    
          #check that two blocks are on the same row
          if(floor((m.start() + 1) / 8) != y):
            continue
    
          print 'found pair at ', x, y, m.group(0)
    
          neighborTile = self.findNeighborTile(color, x - 1, y, 'udl')
          if(neighborTile):
            return Move(neighborTile['x'], neighborTile['y'], x - 1, y)
    
          neighborTile = self.findNeighborTile(color, x + 2, y, 'udr')
          if(neighborTile):
            return Move(neighborTile['x'], neighborTile['y'], x + 2, y)
    
        # Check for Horizontal blocks with gap
        # xox
        for m in re.finditer(r'([a-z]).\1', self.board.board):
          color = m.group(0)[:1]
          x = m.start() % self.board.num_rows
          y = int(floor(m.start() / self.board.num_rows))
          print 'found pair at ', x, y, m.group(0)
    
          #check that two blocks are on the same row
          if(floor((m.start() + 2) / 8) != y):
            continue
    
          neighborTile = self.findNeighborTile(color, x + 1, y, 'ud')
          if(neighborTile):
            return Move(neighborTile['x'], neighborTile['y'], x + 1, y)
        # Check for vertical blocks
        #  o
        #  x
        #  x
        #  o
        for m in re.finditer(r'([a-z]).{7}\1', self.board.board):
          color = m.group(0)[:1]
          x = m.start() % self.board.num_rows
          y = int(floor(m.start() / self.board.num_rows))
    
          print 'found vertical pair at ', x, y, m.group(0), m.start(), m.end()
    
          neighborTile = self.findNeighborTile(color, x, y - 1, 'ulr')
          if(neighborTile):
            return Move(neighborTile['x'], neighborTile['y'], x, y - 1)
          neighborTile = self.findNeighborTile(color, x, y + 2, 'dlr')
          if(neighborTile):
            return Move(neighborTile['x'], neighborTile['y'], x, y + 2)
    
        # Check for vertical blocks
        #  x
        #  o
        #  x
        for m in re.finditer(r'([a-z]).{15}\1', self.board.board):
          color = m.group(0)[:1]
          x = m.start() % self.board.num_rows
          y = int(floor(m.start() / self.board.num_rows))
    
          print 'found vertical pair at ', x, y, m.group(0), m.start(), m.end()
    
          neighborTile = self.findNeighborTile(color, x, y + 1, 'lr')
          if(neighborTile):
            return Move(neighborTile['x'], neighborTile['y'], x, y + 1)
