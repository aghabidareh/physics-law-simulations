SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Thermal bodies
BODY_WIDTH = 120
BODY_HEIGHT = 120
BODY1_X = 150
BODY2_X = 530
BODY_Y = 250

# Initial temperatures (Kelvin)
TEMP_HOT_INITIAL = 400.0
TEMP_COLD_INITIAL = 280.0
TEMP_MIN = 200.0
TEMP_MAX = 500.0

# Thermal properties
SPECIFIC_HEAT = 1000.0  # J/(kg·K) - specific heat capacity
MASS = 1.0              # kg - mass of each body
THERMAL_CONDUCTIVITY = 5.0  # heat transfer rate

# Heat flow particles
NUM_FLOW_PARTICLES = 8
PARTICLE_RADIUS = 5

# Reference temperature for entropy calculation
T_REFERENCE = 273.15  # 0°C in Kelvin

# Colours
WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
RED     = (220, 50, 50)
BLUE    = (50, 50, 220)
GREEN   = (50, 200, 50)
YELLOW  = (220, 220, 50)
ORANGE  = (255, 140, 0)
CYAN    = (50, 220, 220)
PURPLE  = (180, 50, 180)
GRAY    = (180, 180, 180)
DARK_GRAY = (100, 100, 100)
LIGHT_GRAY = (220, 220, 220)

# UI
FONT_NAME = None
FONT_SIZE = 22
SMALL_FONT_SIZE = 18
