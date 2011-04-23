import sys
from starjeweled import *
from strategy import *

def main():
    """ load tiles """
    tiles = {}
    for tile in glob.glob('gfx/bejeweled-blitz/tiles/*.bmp'):
      key, ext = os.path.basename(tile).split('.')
      tiles[key] = (cv.LoadImage(tile))

    b = Board()
    b.setTileImages(tiles, 40, 40)
    b.findBoard('gfx/bejeweled-blitz/top_left_corner.bmp')
    
    s = Strategy(b)
    while 1:
      m = s.findMove()
      if( m ):
        b.movePiece(m)
      b.refreshBoard()

if __name__ == '__main__':
    main()
