# Archivo: config.py
# Descripción: Almacena todas las constantes y configuraciones del juego.
import os

# --- Dimensiones ---
TOP_UI_HEIGHT = 50
BOARD_WIDTH, BOARD_HEIGHT = 600, 600
BOTTOM_UI_HEIGHT = 100
WIDTH, HEIGHT = BOARD_WIDTH, TOP_UI_HEIGHT + BOARD_HEIGHT + BOTTOM_UI_HEIGHT
ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_WIDTH // COLS

# --- Colores (RGB) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
UI_BG = (40, 40, 40)

# Colores por defecto del tablero
DEFAULT_LIGHT_SQUARE = (238, 238, 210)
DEFAULT_DARK_SQUARE = (118, 150, 86)

# --- Paleta de Colores para la UI ---
COLOR_PALETTE = [
    (238, 238, 210), (118, 150, 86),  # Clásicos
    (255, 255, 255), (0, 128, 255),    # Blanco y Azul
    (200, 200, 200), (80, 80, 80),      # Grises
    (210, 180, 140), (139, 69, 19),     # Madera
    (255, 105, 180), (148, 0, 211),     # Rosa y Morado
]

# --- Rutas ---
# Construye una ruta absoluta para que el programa siempre encuentre los assets.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_DIR, 'assets', 'images')

# --- Juego ---
FPS = 60

# --- Fuentes ---
UI_FONT_SIZE = 24
UI_FONT_COLOR = (220, 220, 220)
ABILITY_FONT_COLOR = (255, 223, 0) # Amarillo dorado