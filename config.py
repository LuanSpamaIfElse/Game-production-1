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
ITEM_LAYER = 4

PLAYER_LIFE = 15
ENEMY_LIFE = 1
BAT_LIFE = 5

PLAYER_SPEED = 4
ENEMY_SPEED = 1.0
BAT_SPEED = 5

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
FPS = 45


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

# Melhorias do vendedor
SHOP_BG_COLOR = (30, 30, 40, 200)  # Cor de fundo semi-transparente
SHOP_TEXT_COLOR = WHITE
SHOP_TITLE_COLOR = (255, 215, 0)  # Cor dourada para o título
SHOP_OPTION_COLOR = (200, 200, 200)
SHOP_SELECTED_COLOR = (55, 255, 55)  # Verde
SHOP_OPTION_COLOR = (180, 180, 180)    # Cinza
SHOP_FONT_SIZE = 24
SHOP_TITLE_FONT_SIZE = 28
SHOP_WIDTH = 300
SHOP_HEIGHT = 300
SHOP_X = WIN_WIDTH // 2 - SHOP_WIDTH // 2
SHOP_Y = WIN_HEIGHT // 2 - SHOP_HEIGHT // 2

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
# config.py (adicionar no final)
# Músicas para cada nível
MUSIC_LEVELS = {
    1: 'audios/som_da_floresta (mp3).mp3',
    2: 'audios/som_da_floresta (mp3)mp3',
    'store': 'audios/som_da_floresta (mp3)mp3'
}
#fases
tilemap = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B......O........................M................B',
    'B.P.....O........................................B',
    'B....S...O.......................................B',
    'BOQQOOOOO........................................B',
    'B..Q....C........................................B',
    'B...........G....................................B',
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
    'BT.....WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW..WWWWWQ...B',
    'B......WWWW..WWWWWWWWWWWWWWWWWWWWWWWW....C..QQ...B',
    'B......WQWWWWWWWWW.............WWWWWWW...E..WWQ..B',
    'B......WQWWWWW..................WWQQWW......WW...B',
    'B......WQQWW.....................QQQ....W..WW....B',
    'B......WWWWWW....................QWW.........W...B',
    'B......WQQWWW....................WWWWW.....WWWQ..B',
    'B......WWWWWWWWWWWWW...........WWWWWWW...WWWWW...B',
    'B......WWWWWQQWWWWW.W........WWWWWWWWWWWWQQWW....B',
    'B......WWWWWW....WW..............WWWWWWW.WWWWW...B',
    'B......WWWWWWWWWWWWW...........WWWWWWWQWWWWWW....B',
    'B......WQWWWWWQWWWWWWWWWWWW..QWWWWWWWWWWW..WWW...B',
    'B......WWWWWWWWWWWWWWQQWWWWQQ.WWWWWWW......WWWW..B',
    'B......WWWQQWWWW...WWWWWWWW..Q..........WWWWWW...B',
    'B......WWWWWWWWWWWWWWWWWWWWWWWW..........WWWWW...B',
    'B......WWWWWWW.......WWWWWW.WWWWWWW......WW.WWQ..B',
    'B......QQ...........WQQWW...W.QQQ........WW.WQ...B',
    'B........QQW..........QQ.....Q..........WWWQWWQ..B',
    'B......QWWWWWWWWWWWWWWWQQWWWWW.....WWWWWWWWWWW..PB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
]

tilemap3 = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B..T...O.......................QQQ...............B',
    'B.PQ....O........................................B',
    'B.QQQ..........GGGG.........Q....................B',
    'B..QQ.Q..............................QQ..Q.......B',
    'B..Q....C........................................B',
    'B...........................Q....................B',
    'BQ.........................Q.....................B',
    'B.QQ...............Q.............................B',
    'BQ..............E................................B',
    'B................................................B',
    'B................................................B',
    'B....Q.........GGGG...............................B',
    'B........Q.......................................B',
    'B...........................Q....................B',
    'B......................Q.Q.......................B',
    'B........Q..........Q..................Q.........B',
    'B................................................B',
    'B............QQQ..............Q........QQQ.......B',
    'B......................................Q.........B',
    'B..........QQQQ.............QQQ........Q.........B',
    'B......................................Q.........B',
    'B................................................B',
    'B..........................................QQ....B',
    'B........Q....................Q..................B',
    'B........QQ...................................QQQB',
    'B.Q......Q...................................QQQTB',
    'B.............................................Q..B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
]

store = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B..OVO...................B',
    'B.......................TB',
    'B.........P..............B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBB'
]
