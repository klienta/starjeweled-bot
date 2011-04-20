import sys
import starjeweled

def main():
    """ load tiles """
    tiles = {}
    for tile in glob.glob('gfx/tiles/*.bmp'):
      key, ext = os.path.basename(tile).split('.')
      tiles[key] = (cv.LoadImage(tile))

    b = Board(8, 8)
    b.setTiles(tiles, 51, 51)


if __name__ == '__main__':
    main()
