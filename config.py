WIN_WIDTH = 1020
WIN_HEIGHT = 660
TILESIZES = 32
#ENEMY_COUNT = 0
OBSTACLE_COUNT = 25


PLAYER_LAYER = 6
OBSTACLE_LAYER = 5
PORTAL_LAYER = 5
ENEMY_LAYER = 4
NPC_LAYER = 4
BLOCK_LAYER = 3
GROUND_LAYER = 2
SOIL_LAYER = 1
WIN_WIDTH = 1020
WIN_HEIGHT = 660
TILESIZES = 32
#ENEMY_COUNT = 0
OBSTACLE_COUNT = 25


PLAYER_LAYER = 6
OBSTACLE_LAYER = 5
PORTAL_LAYER = 5
ENEMY_LAYER = 4
NPC_LAYER = 4
BLOCK_LAYER = 3
GROUND_LAYER = 2
SOIL_LAYER = 1
ITEM_LAYER = 4

PLAYER_LIFE = 9
ENEMY_LIFE = 3

PLAYER_SPEED = 6
ENEMY_SPEED = 2

# Barra de cooldown do ataque
ATTACK_BAR_WIDTH = 100
ATTACK_BAR_HEIGHT = 15
ATTACK_BAR_X = 10
ATTACK_BAR_Y = 30  # Abaixo da barra de dodge (se você quiser manter ambas)
ATTACK_BAR_COLOR = (255, 0, 0)   
ATTACK_COOLDOWN_COLOR = (0, 255, 0)  

# Cores da barra de dodge
DODGE_BAR_WIDTH = 100
DODGE_BAR_HEIGHT = 15
DODGE_BAR_X = 10
DODGE_BAR_Y = 10
DODGE_BAR_COLOR = (0, 255, 0)    # Verde quando disponível
DODGE_COOLDOWN_COLOR = (255, 0, 0)  # Vermelho durante cooldown
DODGE_BAR_BG_COLOR = (50, 50, 50)   # Fundo cinza

# Cooldowns das habilidades
ATTACK_COOLDOWN = 1000  # 1 segundos em milissegundos
DODGE_COOLDOWN = 3000   # 3 segundos em milissegundos

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0,0, 0)
FPS = 25


HEALTH_BAR_WIDTH = 40
HEALTH_BAR_HEIGHT = 5
HEALTH_BAR_OFFSET = 10  # Distância acima do sprite
PLAYER_HEALTH_COLOR = (0, 255, 0)  # Verde
ENEMY_HEALTH_COLOR = (255, 0, 0)   # Vermelho
HEALTH_BAR_BG_COLOR = (50, 50, 50) # Cinza escuro

# Painel de Habilidades
ABILITY_PANEL_WIDTH = 300
ABILITY_PANEL_HEIGHT = 180
ABILITY_PANEL_X = WIN_WIDTH - ABILITY_PANEL_WIDTH - 10
ABILITY_PANEL_Y = 10
ABILITY_PANEL_COLOR = (50, 50, 50, 200)  # Cinza escuro semi-transparente
ABILITY_TEXT_COLOR = WHITE

# Diálogo
DIALOG_BOX_WIDTH = WIN_WIDTH - 40
DIALOG_BOX_HEIGHT = 140  # Aumentei a altura para acomodar o texto adicional
DIALOG_BOX_X = 20
DIALOG_BOX_Y = WIN_HEIGHT - DIALOG_BOX_HEIGHT - 20
DIALOG_BOX_COLOR = (50, 50, 50)
DIALOG_TEXT_COLOR = WHITE
DIALOG_FONT_SIZE = 24
DIALOG_SMALL_FONT_SIZE = 18  # Adicionei para o texto "APERTE ESPAÇO"
DIALOG_TEXT_MARGIN = 15
DIALOG_TEXT_SPEED = 2

#audios
SongFlorest = 'audios/som_da_floresta (mp3).mp3'
#fases
tilemap = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B......O........................M................B',
    'B.P.....O........................................B',
    'B....S...O.......................................B',
    'BOQQOOOOO........................................B',
    'B..Q....C........................................B',
    'B................................................B',
    'BQ.........................Q.....................B',
    'BTQQ...............Q.............................B',
    'BQ..............E................................B',
    'B................................................B',
    'B................................................B',
    'B....Q...........................................B',
    'B................................................B',
    'B...........................Q....................B',
    'B......................Q.Q.......................B',
    'B...................Q............................B',
    'B................................................B',
    'B............................Q...................B',
    'B................................................B',
    'B...........................QQQ..................B',
    'B......................................Q.........B',
    'B................................................B',
    'B................................................B',
    'B.............................Q..................B',
    'B................................................B',
    'B.Q..............................................B',
    'B................................................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
]

# Fase 2 - Tilemap com spawn na parte inferior
tilemap2 = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B...............................M................B',
    'B................................................B',
    'B................................................B',
    'B.QQ.............................................B',
    'B..Q.............................................B',
    'B................................................B',
    'BQ.........................Q.....................B',
    'BQ.Q...............Q.............................B',
    'B................................................B',
    'B................................................B',
    'B................................................B',
    'B....Q...........................................B',
    'B................................................B',
    'B...........................Q....................B',
    'B......................Q.Q.......................B',
    'B...................Q............................B',
    'B................................................B',
    'B...........Q................Q...................B',
    'B................................................B',
    'B...........................QQQ..................B',
    'B........Q.............................Q.........B',
    'B..............Q.................QQ.............QB',
    'B...........................................Q..QTB',
    'B.........Q...................Q...Q.Q.QQ......QQQB',
    'BOOOO............................................B',
    'BQQQQQQ....QC......................Q.............B',
    'BTQPQQ...........................................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
]

store = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B..OMO...................B',
    'B.......................TB',
    'B.........P..............B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBB'
]



PLAYER_LIFE = 15
ENEMY_LIFE = 3

PLAYER_SPEED = 6
ENEMY_SPEED = 2

# Barra de cooldown do ataque
ATTACK_BAR_WIDTH = 100
ATTACK_BAR_HEIGHT = 15
ATTACK_BAR_X = 10
ATTACK_BAR_Y = 30  # Abaixo da barra de dodge (se você quiser manter ambas)
ATTACK_BAR_COLOR = (255, 0, 0)   
ATTACK_COOLDOWN_COLOR = (0, 255, 0)  

# Cores da barra de dodge
DODGE_BAR_WIDTH = 100
DODGE_BAR_HEIGHT = 15
DODGE_BAR_X = 10
DODGE_BAR_Y = 10
DODGE_BAR_COLOR = (0, 255, 0)    # Verde quando disponível
DODGE_COOLDOWN_COLOR = (255, 0, 0)  # Vermelho durante cooldown
DODGE_BAR_BG_COLOR = (50, 50, 50)   # Fundo cinza

# Cooldowns das habilidades
ATTACK_COOLDOWN = 1000  # 1 segundos em milissegundos
DODGE_COOLDOWN = 3000   # 3 segundos em milissegundos

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0,0, 0)
FPS = 25


HEALTH_BAR_WIDTH = 40
HEALTH_BAR_HEIGHT = 5
HEALTH_BAR_OFFSET = 10  # Distância acima do sprite
PLAYER_HEALTH_COLOR = (0, 255, 0)  # Verde
ENEMY_HEALTH_COLOR = (255, 0, 0)   # Vermelho
HEALTH_BAR_BG_COLOR = (50, 50, 50) # Cinza escuro

# Painel de Habilidades
ABILITY_PANEL_WIDTH = 300
ABILITY_PANEL_HEIGHT = 150
ABILITY_PANEL_X = WIN_WIDTH - ABILITY_PANEL_WIDTH - 10
ABILITY_PANEL_Y = 10
ABILITY_PANEL_COLOR = (50, 50, 50, 200)  # Cinza escuro semi-transparente
ABILITY_TEXT_COLOR = WHITE

# Diálogo
DIALOG_BOX_WIDTH = WIN_WIDTH - 40
DIALOG_BOX_HEIGHT = 140  # Aumentei a altura para acomodar o texto adicional
DIALOG_BOX_X = 20
DIALOG_BOX_Y = WIN_HEIGHT - DIALOG_BOX_HEIGHT - 20
DIALOG_BOX_COLOR = (50, 50, 50)
DIALOG_TEXT_COLOR = WHITE
DIALOG_FONT_SIZE = 24
DIALOG_SMALL_FONT_SIZE = 18  # Adicionei para o texto "APERTE ESPAÇO"
DIALOG_TEXT_MARGIN = 15
DIALOG_TEXT_SPEED = 2

#audios
SongFlorest = 'audios/som_da_floresta (mp3).mp3'
#fases
tilemap = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B......O........................M................B',
    'B.P.....O........................................B',
    'B....S...O.......................................B',
    'BOQQOOOOO........................................B',
    'B..Q.............................................B',
    'B................................................B',
    'BQ.........................Q.....................B',
    'BTQQ...............Q.............................B',
    'BQ..............E................................B',
    'B................................................B',
    'B................................................B',
    'B....Q...........................................B',
    'B................................................B',
    'B...........................Q....................B',
    'B......................Q.Q.......................B',
    'B...................Q............................B',
    'B................................................B',
    'B............................Q...................B',
    'B................................................B',
    'B...........................QQQ..................B',
    'B......................................Q.........B',
    'B................................................B',
    'B................................................B',
    'B.............................Q..................B',
    'B................................................B',
    'B.Q..............................................B',
    'B................................................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
]

# Fase 2 - Tilemap com spawn na parte inferior
tilemap2 = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B...............................M................B',
    'B................................................B',
    'B................................................B',
    'B.QQ.............................................B',
    'B..Q.............................................B',
    'B................................................B',
    'BQ.........................Q.....................B',
    'BQ.Q...............Q.............................B',
    'B................................................B',
    'B................................................B',
    'B................................................B',
    'B....Q...........................................B',
    'B................................................B',
    'B...........................Q....................B',
    'B......................Q.Q.......................B',
    'B...................Q............................B',
    'B................................................B',
    'B...........Q................Q...................B',
    'B................................................B',
    'B...........................QQQ..................B',
    'B........Q.............................Q.........B',
    'B..............Q.E...............QQ.............QB',
    'B...........................................Q..QTB',
    'B.........Q...................Q...Q.Q.QQ......QQQB',
    'BOOOO............................................B',
    'BQQQQ..............................Q.............B',
    'BTQPQ............................................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
]

