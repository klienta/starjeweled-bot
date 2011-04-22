import os, sys
import glob
import cv
import PIL
import ImageGrab
from numpy import arange

import mouse
import move

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

  def __str__(self):
    return self.board

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

  def movePiece(self, move):
    print 'moving ', move.src, ' to ', move.des
    offset = self.tile_w / 2

    srcXpos = self.x + ( move.src.x * self.tile_w) + offset
    srcYpos = self.y + ( move.src.y * self.tile_h) + offset

    desXpos = self.x + ( move.des.x * self.tile_w) + offset
    desYpos = self.y + ( move.des.y * self.tile_h) + offset

    mouse.click(srcXpos, srcYpos)
    mouse.click(desXpos, desYpos)
    mouse.move(self.x - 100, self.y)