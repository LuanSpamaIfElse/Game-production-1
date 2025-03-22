import pygame
import pygame.sprite
from config import *
import math
import random


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height], pygame.SRCALPHA)  # Permite transparência
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Posição inicial do jogador
        self.x = x * TILESIZES
        self.y = y * TILESIZES
        self.width = TILESIZES
        self.height = TILESIZES

        # Variáveis de movimento
        self.x_change = 0
        self.y_change = 0
        self.facing = 'down'
        # Carrega a imagem do personagem
        #self.image = self.game.character_spritesheet.get_sprite(1, 3, 38, 39)
        self.animation_frames = {
    'left': [
        self.game.character_spritesheet.get_sprite(1, 42, self.width+1, 39 ),
        #self.game.character_spritesheet.get_sprite(1, 60, 28, 38)
    ],
    'right': [
        self.game.character_spritesheet.get_sprite(33, 42, self.width+1, 39),
    ],
    'up': [
        self.game.character_spritesheet.get_sprite(79, 4, self.width, self.height+1),
    ],
    'down': [
        self.game.character_spritesheet.get_sprite(1, 4, self.width, self.height+1),
    ]
}

        self.current_frame = 0
        self.animation_speed = 1
        self.animation_counter = 0

        self.image = self.animation_frames[self.facing][self.current_frame]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def animate(self):
        # Alterna entre os frames de animação
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames[self.facing])
            self.image = self.animation_frames[self.facing][self.current_frame]
        
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        

        # Aplica o movimento
        self.rect.x += self.x_change
        self.collide_enemy()
        self.collide_blocks('x')
        self.x = self.rect.x

        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.y = self.rect.y
        self.animate()
        # Reseta os valores de movimento após cada frame
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_d]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_w]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_s]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def kill(self):
        self.game.playing = False  # Interrompe o jogo
        self.game.all_sprites.remove(self)  # Remove o jogador da lista de sprites
        self.game.game_over()  # Chama a tela de game over


    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False  

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Posição do tile
        self.x = x * TILESIZES
        self.y = y * TILESIZES
        self.width = TILESIZES
        self.height = TILESIZES

        # Carrega a imagem do terreno
        self.image = self.game.terrain_spritesheet.get_sprite(300, 295, self.width, self.height)

        # Define o retângulo de colisão
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZES
        self.y = y * TILESIZES
        self.width = TILESIZES
        self.height = TILESIZES

        self.x_change = 0
        self.y_change = 0
        self.facing = random.choice(['left', 'right'])
        self.movement_loop = 0  # Inicialização correta da variável
        self.max_travel = random.randint(7, 30)

        # Animação
        self.animation_frames = {
            'left': [
                self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)
            ],
            'right': [
                self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)
           ]
        }
        self.current_frame = 0
        self.animation_speed = 10
        self.animation_counter = 0

        self.image = self.animation_frames[self.facing][self.current_frame]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()  # Atualiza a animação
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'

        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def animate(self):
        # Alterna entre os frames de animação
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames[self.facing])
            self.image = self.animation_frames[self.facing][self.current_frame]

class Plant(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER  # Plantas devem estar no mesmo layer do solo
        self.groups = self.game.all_sprites  # Apenas visível, sem colisão
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Posição da planta
        self.x = x * TILESIZES
        self.y = y * TILESIZES
        self.width = TILESIZES
        self.height = TILESIZES

        # Define a aparência da planta
        self.image = self.game.plant_spritesheet.get_sprite(350, 547, self.width, self.height)
        self.image.set_colorkey(BLACK)  # Verde para representar plantas

        # Define a posição no mapa
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Posição do bloco
        self.x = x * TILESIZES
        self.y = y * TILESIZES
        self.width = TILESIZES
        self.height = TILESIZES

        # Define a aparência do bloco
        self.image = self.game.plant_spritesheet.get_sprite(960, 448, self.width, self.height)
        self.image.set_colorkey(BLACK)

        # Define o retângulo de colisão
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Button:
    def __init__(self, x ,y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.SysFont('arial.ttf', fontsize)
        self.content = content
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)


        self.x = x
        self.y = y
        self.width = TILESIZES
        self.height = TILESIZES

        self.animation_loop = 0
        self.image = self.game.attack_spritsheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    def animate(self):
        direction = self.game.player.facing

        right_animations = [
                self.game.attack_spritsheet.get_sprite(40, 122, self.width, self.height)
            ]
        down_animations = [
                self.game.attack_spritsheet.get_sprite(114, 130, self.width, self.height)
            ]
        left_animations = [
                self.game.attack_spritsheet.get_sprite(77, 123, self.width, self.height)
            ]
        up_animations = [
                self.game.attack_spritsheet.get_sprite(0, 130, self.width, self.height - 5)
            ]
        if direction == 'up':
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 1:
                self.kill()

        if direction == 'down':
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.9
            if self.animation_loop >= 1:
                self.kill()

        if direction == 'right':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.9
            if self.animation_loop >= 1:
                self.kill()

        if direction == 'left':
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.9
            if self.animation_loop >= 1:
                self.kill()
