WIN_WIDTH = 1020
WIN_HEIGHT = 660
TILESIZES = 32
ENEMY_COUNT = 10
OBSTACLE_COUNT = 5

PLAYER_LAYER = 5
OBSTACLE_LAYER = 4
ENEMY_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_SPEED = 6
ENEMY_SPEED = 2

# Cores da barra de dodge
DODGE_BAR_WIDTH = 100
DODGE_BAR_HEIGHT = 15
DODGE_BAR_X = 10
DODGE_BAR_Y = 10
DODGE_BAR_COLOR = (0, 255, 0)    # Verde quando disponível
DODGE_COOLDOWN_COLOR = (255, 0, 0)  # Vermelho durante cooldown
DODGE_BAR_BG_COLOR = (50, 50, 50)   # Fundo cinza

# Cooldowns das habilidades
ATTACK_COOLDOWN = 3000  # 3 segundos em milissegundos
DODGE_COOLDOWN = 3000   # 3 segundos em milissegundos

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0,0, 0)
FPS = 25

# Painel de Habilidades
ABILITY_PANEL_WIDTH = 300
ABILITY_PANEL_HEIGHT = 150
ABILITY_PANEL_X = WIN_WIDTH - ABILITY_PANEL_WIDTH - 10
ABILITY_PANEL_Y = 10
ABILITY_PANEL_COLOR = (50, 50, 50, 200)  # Cinza escuro semi-transparente
ABILITY_TEXT_COLOR = WHITE

#fases
tilemap = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B........................B',
    'B........................B',
    'B.....O..........Q.......B',
    'B........................B',
    'B........................B',
    'B...........Q............B',
    'B..........QPQ...........B',
    'B...........Q............B',
    'B........................B',
    'B........................B',
    'B........................B',
    'B.....QQ.................B',
    'B..QQ.Q..Q...............B',
    'BBBBBB.BBBBBBBBBBBBBBBBBBB',
]
