# NR_BLOCKS_WIDE = 12
# NR_BLOCKS_HIGH = 12
# BLOCK_WIDTH = 40
# BLOCK_HEIGHT = 40
# SCREEN_WIDTH = NR_BLOCKS_WIDE * BLOCK_WIDTH
# SCREEN_HEIGHT = NR_BLOCKS_HIGH * BLOCK_HEIGHT

# SCREEN_WIDTH = 480
# SCREEN_HEIGHT = 480
# NUMBER_OF_BLOCKS_WIDE = 12
# NUMBER_OF_BLOCKS_HIGH = 12
# BLOCK_HEIGHT = round(SCREEN_HEIGHT/NUMBER_OF_BLOCKS_HIGH)
# BLOCK_WIDTH = round(SCREEN_WIDTH/NUMBER_OF_BLOCKS_WIDE)

TILESIZE = 52
NR_BLOCKS_WIDE = 20
NR_BLOCKS_HIGH = 16
WIDTH = TILESIZE * NR_BLOCKS_WIDE
HEIGHT = TILESIZE * NR_BLOCKS_HIGH
FRAME_RATE = 20

CHAR_KINDS = ["warrior", "mage"]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (55, 55, 255)
GREEN = (0, 200, 0)
DARKGREY = (90, 90, 90)
LIGHTGREY = (210, 210, 210)
UGLY_PINK = (255, 0, 255)
BROWN = (153, 76, 0)
GOLD = (153, 153, 0)
DARKGREEN = (0, 102, 0)
DARKORANGE = (255, 128, 0)
LIGHT_PURPLE = (255, 153, 255)
ORANGE = (255, 128, 0)
PURPLE = (128,  0, 128)

UP = 90
DOWN = -90
RIGHT = 0
LEFT = 180

GRASS_IMG = 'grass.gif'
WALL_IMG = 'trees.png'
PLAYER_IMG = 'player.png'
PLAYER_IMG_DEAD = 'player_dead.png'
MONSTER_IMG = 'giant_bat.png'
MONSTER_IMG_DEAD = 'giant_bat_dead.png'

MAPFILE = 'map.txt'
GAME_DATA_FILE = 'game.json'
PLAYER_DATA_FILE = 'player.json'
MONSTER_DATA_FILE = 'monster.json'

TITLE = 'Broken Skull'
FOOD_ENERGY = 10