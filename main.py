import sys
from starjeweled import *
from strategy import *

def main():
    """ load tiles """
    tiles = {}
    for tile in glob.glob('gfx/tiles/*.bmp'):
      key, ext = os.path.basename(tile).split('.')
      tiles[key] = (cv.LoadImage(tile))

    b = Board()
    b.setTileImages(tiles, 51, 51)
    b.findBoard('gfx/top_left_corner.bmp')
    
    s = Strategy(b)
    while 1:
      m = s.findMove()
      if( m ):
        b.movePiece(m)
      b.refreshBoard()

if __name__ == '__main__':
    main()
