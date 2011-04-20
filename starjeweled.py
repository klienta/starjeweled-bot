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
from numpy import arange

def cv_screenshot():
  file = "screen_capture.jpg"
  pil_img = ImageGrab.grab()#.save(file)
  print pil_img.info
  #return cv.LoadImage(file)

  channels = 3
  cv_img = cv.CreateImageHeader(pil_img.size, cv.IPL_DEPTH_32F, channels)
 # cv.SetData(cv_img, pil_img.tostring(), (pil_img.size[0] * channels * (  ) )
  return cv_img

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

class Move:
    def __init__(self, srcX, srcY, desX, desY):
        self.src = {'x': srcX, 'y': srcY}
        self.des = {'x': desX, 'y': desY }

class Board:
  board = ""
  num_rows = 8
  num_cols = 8


  def findBoard(self, top_left_corner):
      screenshot = cv_screenshot()
      top_left_corner = cv.LoadImage(top_left_corner_image)
      board_loc = find(top_left_corner, screenshot)
      if(board_loc['score'] < .7):
          print("board not found :(")
          exit()
          return
      self.x = board_loc['x'] + top_left_corner.width
      self.y = board_loc['y'] + top_left_corner.height


  def setTileImages(self, tile_images, tile_w, tile_h):
      self.tile_images = tile_images
      self.tile_w = tile_w
      self.tile_h = tile_h

  def refreshBoard(self):
    """ initialize board with 0 """
    screenshot = cv_screenshot()
    self.board = "0" * self.num_rows * self.num_cols
    for y in arange(self.num_rows):
      for x in arange(self.num_cols):
        string_offset = y * self.num_rows + x
        self.board = string_replace_index(self.board, self.getTile(x, y, screenshot), string_offset)
  def setBoard(self, board_string):
      self.board = board_string

  def show(self):
    print self.board
    for i in arange(self.num_rows):
      offset = i * self.num_cols
      print self.board[offset:offset + self.num_cols]

  def toArray(self):
    a = []
    for i in arange(self.num_rows):
      offset = (i) * self.num_cols
      a.append(list(self.board[offset:offset + self.num_cols]))
    return a

  def fromArray(self, arr):
      self.board = ""
      for row in arr:
          for col in row:
              self.board += col

      return self.board

  def getTile(self, x, y, screenshot):
    if(x < 0 or x > self.num_cols - 1 or y < 0 or y > self.num_rows - 1):
      return False

    string_offset = y * self.num_rows + x
    if(self.board[string_offset:string_offset + 1]):
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

  def findMove(self):
    print "finding moves"
    # look for 4s
    #  xxox
    for m in re.finditer(r'([a-z])\1.\1', self.board):
      color = m.group(0)[:1]
      x = m.start() % self.num_rows
      y = int(math.floor(m.start() / self.num_rows))

      #check that two blocks are on the same row
      if(math.floor((m.start() + 3) / 8) != y):
        continue

      print 'found potential 4 ', x, y, m.group(0)

      neighborTile = self.findNeighborTile(color, x + 2, y, 'ud')
      if(neighborTile):
        return Move(neighborTile['x'], neighborTile['y'], x + 2, y)

    # look for 4s
    #  xoxx
    for m in re.finditer(r'([a-z]).\1\1', self.board):
      color = m.group(0)[:1]
      x = m.start() % self.num_rows
      y = int(math.floor(m.start() / self.num_rows))

      #check that two blocks are on the same row
      if(math.floor((m.start() + 3) / 8) != y):
        continue

      print 'found potential 4 ', x, y, m.group(0)

      neighborTile = self.findNeighborTile(color, x + 1, y, 'ud')
      if(neighborTile):
        return Move(neighborTile['x'], neighborTile['y'], x + 1, y)

    # Check for Horizontal Blocks
    #  1  4
    # 3oxxo6
    #  2  5
    print 'finding moves on ', self.board
    for m in re.finditer(r'([a-z])\1', self.board):
      color = m.group(0)[:1]
      x = m.start() % self.num_rows
      y = int(math.floor(m.start() / self.num_rows))

      #check that two blocks are on the same row
      if(math.floor((m.start() + 1) / 8) != y):
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
    for m in re.finditer(r'([a-z]).\1', self.board):
      color = m.group(0)[:1]
      x = m.start() % self.num_rows
      y = int(math.floor(m.start() / self.num_rows))
      print 'found pair at ', x, y, m.group(0)

      #check that two blocks are on the same row
      if(math.floor((m.start() + 2) / 8) != y):
        continue

      neighborTile = self.findNeighborTile(color, x + 1, y, 'ud')
      if(neighborTile):
        return Move(neighborTile['x'], neighborTile['y'], x + 1, y)
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
        return Move(neighborTile['x'], neighborTile['y'], x, y - 1)
      neighborTile = self.findNeighborTile(color, x, y + 2, 'dlr')
      if(neighborTile):
        return Move(neighborTile['x'], neighborTile['y'], x, y + 2)

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
        return Move(neighborTile['x'], neighborTile['y'], x, y + 1)
