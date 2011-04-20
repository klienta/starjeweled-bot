import os, sys
import glob
import cv
import PIL
import ImageGrab
import time
from sets import Set
import re
import math
import mouse

def cv_screenshot():
  file = "screen_capture.jpg"
  pil_img = ImageGrab.grab().save(file)
  return cv.LoadImage(file)
  #cv_img = cv.CreateImageHeader(pil_img.size, cv.IPL_DEPTH_32F, 3)
  #cv.SetData(cv_img, pil_img.tostring(), pil_img.size[0]*3*4)
  #return cv_img

def string_replace_index(string, replace, index):
  return string[:index] + replace + string[index + 1:]

"""returns (x,y) coords of small image inside large image."""
def find(template, image):
    image_size = cv.GetSize(image)
    template_size = cv.GetSize(template)
    result_size = [ s[0] - s[1] + 1 for s in zip(image_size, template_size) ]
    result = cv.CreateImage(result_size, cv.IPL_DEPTH_32F, 1)
    cv.CV_BGR2RGB
    cv.MatchTemplate(image, template, result, cv.CV_TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.MinMaxLoc(result)
    x, y = max_loc
    return {'score': max_val, 'x': x, 'y': y }

def findInRegion(template, image, x, y, w, h):
  sub = cv.GetSubRect(image, (x, y, w, h))
  return find(template, sub)

class Board:
  def __init__(self, num_rows, num_cols, top_left_corner_image, tile_images, tile_w, tile_h):
    self.tile_w = tile_w
    self.tile_h = tile_h

    self.num_rows = num_rows
    self.num_cols = num_cols

    screenshot = cv_screenshot()
    top_left_corner = cv.LoadImage(top_left_corner_image)
    board_loc = find(top_left_corner, screenshot)
    if(board_loc['score'] < .7):
      print("board not found :(")
      exit()
      return
    self.x = board_loc['x'] + top_left_corner.width
    self.y = board_loc['y'] + top_left_corner.height
    self.tile_images = tile_images
    self.refreshBoard()

  def refreshBoard(self):
    """ initialize board with 0 """
    screenshot = cv_screenshot()
    self.board = "0" * self.num_rows * self.num_cols
    for y in range(self.num_rows):
      for x in range(self.num_cols):
        string_offset = y * self.num_rows + x
        self.board = string_replace_index(self.board, self.getTile(x, y, screenshot), string_offset)

  def show(self):
    print self.board
    for i in range(self.num_rows):
      offset = i * self.num_cols
      print self.board[offset:offset + self.num_cols]

  def toArray(self):
    a = []
    for i in range(self.num_rows - 1):
      offset = (i) * self.num_cols
      a.append(list(self.board[offset:offset + self.num_cols]))
    return a

  def getTile(self, x, y, screenshot):
    if(x < 0 or x > self.num_cols - 1 or y < 0 or y > self.num_rows - 1):
      return False

    string_offset = y * self.num_rows + x
    if(self.board[string_offset:string_offset + 1] != '0'):
      return self.board[string_offset:string_offset + 1]

    tileX = self.x + (x * self.tile_w)
    tileY = self.y + (y * self.tile_h)

    if(not screenshot):
      screenshot = cv_screenshot()
    for color in self.tile_images:
      results = findInRegion(self.tile_images[color], screenshot, tileX, tileY, self.tile_w, self.tile_h)
      if(results['score'] > .6):
        self.board = string_replace_index(self.board, color, string_offset)
        return color
    return '0'
  def tileIsColor(self, color, x, y):
    return color == self.getTile(x, y, None)

  def movePiece(self, srcX, srcY, desX, desY):
    print 'moving ', srcX, srcY, ' to ', desX, desY
    offset = self.tile_w / 2

    self.last_moves_x = Set([srcX])
    self.last_moves_y = Set([srcY])

    srcXpos = self.x + (srcX * self.tile_w) + offset
    srcYpos = self.y + (srcY * self.tile_h) + offset

    desXpos = self.x + (desX * self.tile_w) + offset
    desYpos = self.y + (desY * self.tile_h) + offset

    mouse.click(srcXpos, srcYpos)
    mouse.click(desXpos, desYpos)
    mouse.move(self.x - 100, self.y)
    time.sleep(1)
    self.refreshBoard()

  def findNeighborTile(self, color, x, y, directions):
    directions = list(directions)
    print 'inspecting ', x, y, self.getTile(x, y, None)
    for dir in directions:
      print 'looking ', dir
      if dir == 'u':
        if(self.tileIsColor(color, x, y - 1)):
          return {'x':x, 'y':y - 1}
      elif dir == 'r':
        if(self.tileIsColor(color, x + 1, y)):
          return {'x': x + 1, 'y': y}
      elif dir == 'd':
        if(self.tileIsColor(color, x, y + 1)):
          return {'x': x, 'y': y + 1}
      elif dir == 'l':
        if(self.tileIsColor(color, x - 1, y)):
          return {'x': x - 1, 'y': y }

  def findMoves(self):
    print "finding moves"
    """  
    # look for 4s
    #  xxox
    for m in re.finditer(r'([a-z])\1.\1', self.board):
      color = m.group(0)[:1]
      x = m.start() % self.num_rows
      y = int(math.floor(m.start() / self.num_rows ))
      
      #check that two blocks are on the same row
      if( math.floor((m.start() + 3)/8) != y ):
        continue
      
      print 'found potential 4 ', x, y, m.group(0)
      
      neighborTile = self.findNeighborTile(color, x + 2, y, 'ud')
      if( neighborTile ):
        self.movePiece( neighborTile['x'], neighborTile['y'], x + 2, y)
        return

    # look for 4s
    #  xoxx
    for m in re.finditer(r'([a-z]).\1\1', self.board):
      color = m.group(0)[:1]
      x = m.start() % self.num_rows
      y = int(math.floor(m.start() / self.num_rows ))
      
      #check that two blocks are on the same row
      if( math.floor((m.start() + 3)/8) != y ):
        continue
      
      print 'found potential 4 ', x, y, m.group(0)
      
      neighborTile = self.findNeighborTile(color, x + 1, y, 'ud')
      if( neighborTile ):
        self.movePiece( neighborTile['x'], neighborTile['y'], x + 1, y)
        return
        
    # Check for Horizontal Blocks
    #  1  4
    # 3oxxo6
    #  2  5
    print 'finding moves on ', self.board
    for m in re.finditer(r'([a-z])\1', self.board):
      color = m.group(0)[:1]
      x = m.start() % self.num_rows
      y = int(math.floor(m.start() / self.num_rows ))
      
      #check that two blocks are on the same row
      if( math.floor((m.start() + 1)/8) != y ):
        continue
      
      print 'found pair at ', x, y, m.group(0)
      
      neighborTile = self.findNeighborTile(color, x - 1, y, 'udl')
      if( neighborTile ):
        self.movePiece( neighborTile['x'], neighborTile['y'], x - 1, y)
        return

      neighborTile = self.findNeighborTile(color, x + 2, y, 'udr')
      if( neighborTile ):
        self.movePiece( neighborTile['x'], neighborTile['y'], x + 2, y)
        return
        
    # Check for Horizontal blocks with gap
    # xox
    for m in re.finditer(r'([a-z]).\1', self.board):
      color = m.group(0)[:1]
      x = m.start() % self.num_rows
      y = int(math.floor(m.start() / self.num_rows ))
      print 'found pair at ', x, y, m.group(0)
      
      #check that two blocks are on the same row
      if( math.floor((m.start() + 2)/8) != y ):
        continue
      
      neighborTile = self.findNeighborTile(color, x + 1, y, 'ud')
      if( neighborTile ):
        self.movePiece( neighborTile['x'], neighborTile['y'], x + 1, y)
        return
    """
    # Check for vertical blocks
    #  o
    #  x
    #  x
    #  o
    for m in re.finditer(r'([a-z]).{7}\1', self.board):
      color = m.group(0)[:1]
      x = m.start() % self.num_rows
      y = int(math.floor(m.start() / self.num_rows))

      print 'found vertical pair at ', x, y, m.group(0), m.start(), m.end()

      neighborTile = self.findNeighborTile(color, x, y - 1, 'ulr')
      if(neighborTile):
        self.movePiece(neighborTile['x'], neighborTile['y'], x, y - 1)
        return
      neighborTile = self.findNeighborTile(color, x, y + 2, 'dlr')
      if(neighborTile):
        self.movePiece(neighborTile['x'], neighborTile['y'], x, y + 2)
        return

    # Check for vertical blocks
    #  x
    #  o
    #  x
    for m in re.finditer(r'([a-z]).{15}\1', self.board):
      color = m.group(0)[:1]
      x = m.start() % self.num_rows
      y = int(math.floor(m.start() / self.num_rows))

      print 'found vertical pair at ', x, y, m.group(0), m.start(), m.end()

      neighborTile = self.findNeighborTile(color, x, y + 1, 'lr')
      if(neighborTile):
        self.movePiece(neighborTile['x'], neighborTile['y'], x, y + 1)
        return

    print 'no moves found, refreshing'

""" load tiles """
tiles = {}
for tile in glob.glob('gfx/tiles/*.bmp'):
  key, ext = os.path.basename(tile).split('.')
  tiles[key] = (cv.LoadImage(tile))

b = Board(8, 8, 'gfx/top_left_corner.bmp', tiles, 51, 51);
b.show()

while 1:
  b.findMoves()
