# Imports
import os
import pygame as pg

# Window settings
WIDTH = 752
HEIGHT = 752
TITLE = "Chess"
# Game settings
FPS = 20
# Colors (R, G, B)
BLACK = (0, 0, 0)
BLACK_A = (0, 0, 0, 150)
WHITE = (255, 255, 255)
WHITE_A = (255, 255, 255, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
VIOLET = (128, 0, 128)
ORANGE = (255, 165, 0)
BROWN = (62, 34, 21)
CYAN = (0, 255, 255)
CF_BLUE = (100, 149, 237)
GRAY = (211, 211, 211)
COL1 = (204, 156, 108)
COL2 = (159, 89, 20)
A_COL = (34, 231, 99)
S_GREEN = (20, 184, 96)
S_BLUE = (20, 91, 184)
S_RED = (184, 20, 53)
S_VIOLET = (113, 20, 184)
DIM = (0, 0, 0, 180)
BG_COLOR = BROWN
# In-game settings
FONT = pg.font.match_font("consolas bold")
# In-game constants
BOARD_SHRINK = 3 / 4
BOARD_ROWS = 8
BOARD_COLS = 8
BOARD_WIDTH = WIDTH * BOARD_SHRINK
BOARD_HEIGHT = HEIGHT * BOARD_SHRINK
TILE_WIDTH = BOARD_WIDTH // BOARD_ROWS
TILE_HEIGHT = BOARD_HEIGHT // BOARD_COLS
TILE_OFFSET_X = WIDTH * (1 - BOARD_SHRINK) / 2
TILE_OFFSET_Y = HEIGHT * (1 - BOARD_SHRINK) / 2
# Makes board width and height a multiple of the number of rows/columns there are
if BOARD_WIDTH % TILE_WIDTH != 0:
    BOARD_WIDTH -= BOARD_WIDTH % TILE_WIDTH
if BOARD_HEIGHT % TILE_HEIGHT != 0:
    BOARD_HEIGHT -= BOARD_HEIGHT % TILE_HEIGHT
HIGHLIGHT_A = 180
# Layers
P_LAYER = 1
S_LAYER = 0
# Files
gameFolder = os.path.dirname(__file__)
assetsFolder = os.path.join(gameFolder, "assets")
imagesFolder = os.path.join(assetsFolder, "imgs")
audioFolder = os.path.join(assetsFolder, "audio")
