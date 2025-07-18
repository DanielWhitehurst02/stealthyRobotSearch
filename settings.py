#Setup
# WIDTH = 1280
# HEIGHT = 720
FPS = 60

# WORLD = "worldfile/conestogo_office.png"
# WORLD = "worldfile/maze1.png"
# WORLD = "worldfile/simpleenv.png"
# WORLD = "worldfile/officebuilding.png"
# WORLD = "worldfile/openwarehouse.png"
# WORLD = "worldfile/warehouse1.png"
# WORLD = "worldfile/warehouse2.png"
# WORLD = "worldfile/artgallery1.png"
WORLD = "worldfile/openrooms1.png"
# WORLD = "worldfile/hallways.png"


# ENVIRONMENT = 'office_space'

# ENVIRONMENT = 'openrooms1'

# ENVIRONMENT = 'warehouse'
# ENVIRONMENT = 'hallways'


#Robot Params
ROBOT_WIDTH: int = 4
ROBOT_START_X = 10
ROBOT_START_Y = 10
SPEED = 2
ROBOT_VISION_LENGTH = 100
ROBOT_FOV = 360

ROBOT_PATHFINDING_AVOID_VISION = True
# ROBOT_PATHFINDING_AVOID_VISION = False

PURE_STEALTH = False
# PURE_STEALTH = True
#
INFO_GAIN_DISREGARD_BOOL = True
# INFO_GAIN_DISREGARD_BOOL = False

FRONT_THRESHOLD = 1
WALL_THRESHOLD = 4

UPDATE_STEPS = 200

EXPLORE_PERCENT_FIN = 0.69

## weights

STEALTH_COST = 1
INFO_GAIN = 1
DIST_WEIGHT = 1.5

INFO_GAIN_DISREGARD_STEALTH = 1000
INFO_GAIN_DISREGARD = 200

#Observers
OB_NUMBER = 3
OB_VIEW_DIST = 100
VISION_COST = 0.1   ## percentage

#colours
RED = (255, 0, 0,255)
RED_TRANS = (255,0,0,1)
GREEN = (0, 255, 0,255)
BLUE = (0, 255, 255,255)
YELLOW = (255, 255, 0,255)
YELLOW_TRANS = (255, 255, 0,50)
WHITE = (255, 255, 255,255)
BLACK = (0, 0, 0,255)
PURPLE = (128, 0, 128,255)
ORANGE = (255, 165 ,0,255)
GREY = (128, 128, 128,255)
GREY_TRANS = (128, 128, 128,100)
TURQUOISE = (64, 224, 208,255)

