import os.path

TITLE = 'Sacred Stones'

TILESIZE = 52
NR_BLOCKS_WIDE = 20
NR_BLOCKS_HIGH = 16
SCREEN_WIDTH = TILESIZE * NR_BLOCKS_WIDE
SCREEN_HEIGHT = TILESIZE * NR_BLOCKS_HIGH
FRAME_RATE = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (55, 55, 255)
LIGHT_BLUE = (164, 219, 232)
GREEN = (0, 200, 0)
DARK_GREY = (90, 90, 90)
LIGHT_GREY = (210, 210, 210)
UGLY_PINK = (255, 0, 255)
BROWN = (153, 76, 0)
GOLD = (153, 153, 0)
DARKGREEN = (0, 102, 0)
DARKORANGE = (255, 128, 0)
LIGHT_PURPLE = (255, 153, 255)
ORANGE = (255, 128, 0)
PURPLE = (128, 0, 128)

UP = 90
DOWN = -90
RIGHT = 0
LEFT = 180

PLAYER_IMG = 'player.png'
PLAYER_IMG_DEAD = 'player_dead.png'
MONSTER_IMG = 'giant_bat.png'
MONSTER_IMG_DEAD = 'giant_bat_dead.png'

SRC_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(ROOT_DIR, 'data')

GAME_DATA_FILE = 'game.json'
ORIGINAL_GAME_FILE = os.path.join(DATA_DIR, 'original', GAME_DATA_FILE)
CURRENT_GAME_FILE = os.path.join(DATA_DIR, 'current', GAME_DATA_FILE)

