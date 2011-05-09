import sys
from starjeweled import *
from strategy import *

def main():
    """ load tiles """
    tiles = {}
    
    game = 'starjeweled'
    tile_size = 51
    
    #uncomment for bejeweled blitz
    #game = 'bejeweled-blitz'
    #tile_size = 40
    
    for tile in glob.glob('gfx/' + game + '/tiles/*.bmp'):
      key, ext = os.path.basename(tile).split('.')
      tiles[key] = (cv.LoadImage(tile))

    b = Board()
    b.setTileImages(tiles, tile_size, tile_size)
    b.findBoard('gfx/' + game + '/top_left_corner.bmp')
    
    s = Strategy(b)
    while 1:
      m = s.findMove()
      if( m ):
        b.movePiece(m)
      b.refreshBoard()

if __name__ == '__main__':
    main()
