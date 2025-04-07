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

        # Propriedades básicas
        self.x = x * TILESIZES
        self.y = y * TILESIZES
        self.width = TILESIZES
        self.height = TILESIZES
        self.x_change = 0
        self.y_change = 0
        self.facing = 'down'

        # Sistema de cooldown
        self.last_attack_time = 0
        self.last_dodge_time = 0
        self.is_dodging = False
        self.dodge_duration = 500
        self.dodge_speed_multiplier = 10
        
        # Dodge Bar
        self.dodge_cooldown = DODGE_COOLDOWN
        self.last_dodge_time = -DODGE_COOLDOWN  
    
            

        # Sistema de animação
        self.animation_speed = 10
        self.animation_counter = 0
        self.current_frame = 0
        
        # Carregar animações
        self.load_animations()
        
        # Imagem inicial
        self.image = self.animation_frames['down'][0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.life = PLAYER_LIFE  # Adicione esta linha
        self.invulnerable = False
        self.invulnerable_time = 0

    def draw_health_bar(self, surface):
        # Calcula a posição da barra
        bar_x = self.rect.x + (self.rect.width // 2) - (HEALTH_BAR_WIDTH // 2)
        bar_y = self.rect.y - HEALTH_BAR_OFFSET
        
        # Desenha o fundo da barra
        pygame.draw.rect(surface, HEALTH_BAR_BG_COLOR, (bar_x, bar_y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
        
        # Calcula a largura da vida atual
        health_width = (self.life / PLAYER_LIFE) * HEALTH_BAR_WIDTH
        # Pisca entre branco e verde durante invulnerabilidade
        health_color = WHITE if pygame.time.get_ticks() % 200 < 100 else PLAYER_HEALTH_COLOR

        # Desenha a barra de vida
        pygame.draw.rect(surface, PLAYER_HEALTH_COLOR, (bar_x, bar_y, health_width, HEALTH_BAR_HEIGHT))

    def take_damage(self):
        if not self.invulnerable:
            self.life -= 1
            self.invulnerable = True
            self.invulnerable_time = pygame.time.get_ticks()
            if self.life <= 0:
                self.kill()

    def can_attack(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_attack_time >= ATTACK_COOLDOWN

    def get_attack_cooldown_ratio(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.last_attack_time
        return min(elapsed / ATTACK_COOLDOWN, 1.0)

    def can_dodge(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_dodge_time >= DODGE_COOLDOWN

    def get_dodge_cooldown_ratio(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.last_dodge_time
        return min(elapsed / self.dodge_cooldown, 1.0)
    
    def load_animations(self):
        self.animation_frames = {
            'left': [
                self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)
            ],
            'right': [
                self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)
            ],
            'up': [
                self.game.character_spritesheet.get_sprite(3, 35, self.width, self.height),
                self.game.character_spritesheet.get_sprite(35, 35, self.width, self.height),
                self.game.character_spritesheet.get_sprite(68, 35, self.width, self.height)
            ],
            'down': [
                self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                self.game.character_spritesheet.get_sprite(65, 2, self.width, self.height)
            ]
        }

    def animate(self):
        self.animation_counter += 1
        
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            frames = self.animation_frames.get(self.facing, [self.image])
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.image = frames[self.current_frame]
            self.image.set_colorkey(BLACK)
            
            # Atualiza rect mantendo a posição
            old_center = self.rect.center if hasattr(self, 'rect') else (self.x, self.y)
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.movement()
        self.animate()
        # Aplica o movimento
        self.rect.x += self.x_change
        self.collide_enemy()
        self.collide_blocks('x')
        self.x = self.rect.x

        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.y = self.rect.y
        
        if self.invulnerable and pygame.time.get_ticks() - self.invulnerable_time > 1000:
             self.invulnerable = False
        # Reseta os valores de movimento após cada frame
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        
        # Reset movement
        self.x_change = 0
        self.y_change = 0
        
        # Movement logic
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
        
        # Dodge
        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and self.can_dodge():
            self.last_dodge_time = pygame.time.get_ticks()
            self.x_change *= self.dodge_speed_multiplier
            self.y_change *= self.dodge_speed_multiplier

    def kill(self):
        self.game.playing = False  # Interrompe o jogo
        self.game.all_sprites.remove(self)  # Remove o jogador da lista de sprites
        self.game.game_over()  # Chama a tela de game over


    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits and not self.invulnerable:
            self.take_damage()
            #self.game.playing = False  

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
    
    def collide_obstacle (self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.obstacle, False)
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
            hits = pygame.sprite.spritecollide(self, self.game.obstacle, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED

        
    def draw(self, surface):
        # Fundo da barra
        pygame.draw.rect(surface, DODGE_BAR_BG_COLOR, 
                        (self.x, self.y, self.width, self.height))
        
        if hasattr(self.game, 'player'):
            ratio = self.game.player.get_dodge_cooldown_ratio()
            fill_width = int(self.width * ratio)
            
            # Barra de preenchimento
            color = DODGE_BAR_COLOR if ratio == 1 else DODGE_COOLDOWN_COLOR
            pygame.draw.rect(surface, color, 
                           (self.x, self.y, fill_width, self.height))
            
            # Texto
            font = pygame.font.SysFont('Arial', 12)
            text = font.render("Dodge", True, WHITE)
            surface.blit(text, (self.x + 5, self.y - 15))
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
        self.image = self.game.terrain_spritesheet.get_sprite(21, 91, self.width, self.height)

        # Define o retângulo de colisão
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.life = ENEMY_LIFE
        self.speed = ENEMY_SPEED
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZES
        self.y = y * TILESIZES
        self.width = TILESIZES
        self.height = TILESIZES

        self.x_change = 0
        self.y_change = 0
        self.facing = random.choice(['left', 'right', 'up', 'down'])
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
           ],
            'up': [
                self.game.enemy_spritesheet.get_sprite(3, 35, self.width, self.height),
                self.game.enemy_spritesheet.get_sprite(35, 35, self.width, self.height),
                self.game.enemy_spritesheet.get_sprite(68, 35, self.width, self.height)
            ],
            'down' :[
                self.game.enemy_spritesheet.get_sprite(3, 3, self.width, self.height),
                self.game.enemy_spritesheet.get_sprite(35, 3, self.width, self.height),
                self.game.enemy_spritesheet.get_sprite(68, 3, self.width, self.height)
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
    def draw_health_bar(self, surface):
        # Calcula a posição da barra
        bar_x = self.rect.x + (self.rect.width // 2) - (HEALTH_BAR_WIDTH // 2)
        bar_y = self.rect.y - HEALTH_BAR_OFFSET
        
        # Desenha o fundo da barra
        pygame.draw.rect(surface, HEALTH_BAR_BG_COLOR, (bar_x, bar_y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
        
        # Calcula a largura da vida atual
        health_width = (self.life / ENEMY_LIFE) * HEALTH_BAR_WIDTH
        
        # Desenha a barra de vida
        pygame.draw.rect(surface, ENEMY_HEALTH_COLOR, (bar_x, bar_y, health_width, HEALTH_BAR_HEIGHT))

    def take_damage(self):
        self.life -= 1
        if self.life <= 0:
            self.kill()

    def update(self):
        self.movement()
        self.animate()  # Atualiza a animação
        
        #self.rect.x += self.x_change
        #self.rect.y += self.y_change

        self.collide_blocks('x')
        #self.X = self.rect.X

        self.rect.x += self.x_change
        block_hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if block_hits:
            if self.x_change > 0:  # Movendo para a direita
                self.rect.x = block_hits[0].rect.left - self.rect.width
                self.facing = random.choice(['left', 'up', 'down'])
            if self.x_change < 0:  # Movendo para a esquerda
                self.rect.x = block_hits[0].rect.right
                self.facing = random.choice(['right', 'up', 'down'])
    
    # Movimento no eixo Y com verificação de colisão
        self.rect.y += self.y_change
        block_hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if block_hits:
            if self.y_change > 0:  # Movendo para baixo
                self.rect.y = block_hits[0].rect.top - self.rect.height
                self.facing = random.choice(['up', 'left', 'right'])
            if self.y_change < 0:  # Movendo para cima
                self.rect.y = block_hits[0].rect.bottom
                self.facing = random.choice(['down', 'left', 'right'])

    def movement(self):
        if self.facing == 'left':
            self.x_change = -ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['up', 'down', 'right'])

        if self.facing == 'up':
            self.y_change = -ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['right', 'left', 'down'])
                 
        if self.facing == 'down':
            self.y_change = ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['up', 'left', 'right'])

        if self.facing == 'right':
            self.x_change = ENEMY_SPEED 
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['up', 'down', 'left'])

    def animate(self):
        # Alterna entre os frames de animação
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames[self.facing])
            self.image = self.animation_frames[self.facing][self.current_frame]

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                self.speed = ENEMY_SPEED / 2  # Reduz a velocidade pela metade ao colidir
                if self.x_change > 0:  # Colisão ao mover para a direita
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += self.speed
                if self.x_change < 0:  # Colisão ao mover para a esquerda
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= self.speed

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                self.speed = ENEMY_SPEED / 2  # Reduz a velocidade pela metade ao colidir
                if self.y_change > 0:  # Colisão ao mover para baixo
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += self.speed
                if self.y_change < 0:  # Colisão ao mover para cima
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= self.speed

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
        self.image = self.game.plant_spritesheet.get_sprite(510, 352, self.width, self.height)
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
        self.image = self.game.block_spritesheet.get_sprite(960, 448, self.width, self.height)
        self.image.set_colorkey(BLACK)

        # Define o retângulo de colisão
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class AbilityPanel:
    def __init__(self, game):
        self.game = game
        self.panel = pygame.Surface((ABILITY_PANEL_WIDTH, ABILITY_PANEL_HEIGHT), pygame.SRCALPHA)
        self.panel.fill(ABILITY_PANEL_COLOR)
        self.rect = self.panel.get_rect(topleft=(ABILITY_PANEL_X, ABILITY_PANEL_Y))
        
        # Fontes
        self.title_font = pygame.font.SysFont('arial', 20, bold=True)
        self.text_font = pygame.font.SysFont('arial', 16)
        self.small_font = pygame.font.SysFont('arial', 12)  # Fonte para a barra
        
        # Ícones
        self.attack_icon = pygame.Surface((20, 20))
        self.attack_icon.fill(RED)
        self.dodge_icon = pygame.Surface((20, 20))
        self.dodge_icon.fill(BLUE)
        
        # Textos pré-renderizados
        self.attack_text = self.text_font.render("ESPAÇO", True, ABILITY_TEXT_COLOR)
        self.dodge_text = self.text_font.render("SHIFT", True, ABILITY_TEXT_COLOR)
        
    def draw(self, surface):
        # Desenha o painel
        surface.blit(self.panel, self.rect)
        
        # Título
        title = self.title_font.render("Habilidades", True, ABILITY_TEXT_COLOR)
        surface.blit(title, (self.rect.x + 10, self.rect.y + 10))
        
        # Espaçamento
        y_offset = 40
        surface.blit(self.attack_icon, (self.rect.x + 10, self.rect.y + y_offset))
        attack_key = self.text_font.render("Ataque:", True, ABILITY_TEXT_COLOR)
        surface.blit(attack_key, (self.rect.x + 40, self.rect.y + y_offset))
        surface.blit(self.attack_text, (self.rect.x + 120, self.rect.y + y_offset))
        
        # Barra de Ataque
        y_offset += 20
        self.draw_attack_bar(surface, self.rect.x + 40, self.rect.y + y_offset)

        
        # Esquiva
        y_offset += 30
        surface.blit(self.dodge_icon, (self.rect.x + 10, self.rect.y + y_offset))
        dodge_key = self.text_font.render("Esquiva:", True, ABILITY_TEXT_COLOR)
        surface.blit(dodge_key, (self.rect.x + 40, self.rect.y + y_offset))
        surface.blit(self.dodge_text, (self.rect.x + 120, self.rect.y + y_offset))
        
        # Barra de Dodge (substitui a indicação de direção)
        y_offset += 30
        self.draw_dodge_bar(surface, self.rect.x + 40, self.rect.y + y_offset)
    def draw_attack_bar(self, surface, x, y):
        #Desenha a barra de cooldown do ataque
        if not hasattr(self.game, 'player'):
            return
            
        # Fundo da barra
        pygame.draw.rect(surface, DODGE_BAR_BG_COLOR, (x, y, DODGE_BAR_WIDTH, DODGE_BAR_HEIGHT))
        
        # Calcula o preenchimento
        ratio = self.game.player.get_attack_cooldown_ratio()
        fill_width = int(DODGE_BAR_WIDTH * ratio)
        
        # Cor baseada no estado
        color = GREEN if ratio >= 1.0 else (255, 0, 0)  # Verde quando pronto, vermelho durante cooldown
    
    # Barra de preenchimento
        pygame.draw.rect(surface, color, (x, y, fill_width, DODGE_BAR_HEIGHT))
    def draw_dodge_bar(self, surface, x, y):
        """Desenha a barra de cooldown do dodge"""
        if not hasattr(self.game, 'player'):
            return
            
        # Fundo da barra
        pygame.draw.rect(surface, DODGE_BAR_BG_COLOR, (x, y, DODGE_BAR_WIDTH, DODGE_BAR_HEIGHT))
        
        # Calcula o preenchimento
        ratio = self.game.player.get_dodge_cooldown_ratio()
        fill_width = int(DODGE_BAR_WIDTH * ratio)
        
        # Cor baseada no estado
        color = DODGE_BAR_COLOR if ratio >= 1.0 else DODGE_COOLDOWN_COLOR
        
        # Barra de preenchimento
        pygame.draw.rect(surface, color, (x, y, fill_width, DODGE_BAR_HEIGHT))
        
        # Texto de status
        #status = "PRONTO" if ratio >= 1.0 else f"{int(ratio*100)}%"
        #status_text = self.small_font.render(status, True, WHITE)
        #surface.blit(status_text, (x + DODGE_BAR_WIDTH + 5, y))

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = OBSTACLE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Posição do bloco
        self.x = x * TILESIZES
        self.y = y * TILESIZES
        self.width = TILESIZES
        self.height = TILESIZES

        # Define a aparência do bloco
        #self.image = self.game.obstacle_spritesheet.get_sprite(320, 185, 80, 85) #arvore
        self.image = self.game.obstacle_spritesheet.get_sprite(640, 195, self.width-4, self.height-1) #tronco
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

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        for enemy in hits:
            enemy.take_damage()

    def update(self):
        self.animate()
        self.collide()

    #def collide(self):
        #hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

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
            self.animation_loop += 0.5
            if self.animation_loop >= 1:
                self.kill()

        if direction == 'right':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 1:
                self.kill()

        if direction == 'left':
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 1:
                self.kill()
class DialogBox:
    def __init__(self, game):
        self.game = game
        self.active = False
        self.current_text = ""
        self.visible_text = ""
        self.text_progress = 0
        self.font = pygame.font.SysFont('arial', DIALOG_FONT_SIZE)
        self.small_font = pygame.font.SysFont('arial', DIALOG_SMALL_FONT_SIZE)
        
        # Caixa de diálogo
        self.box = pygame.Surface((DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT))
        self.box.fill(DIALOG_BOX_COLOR)
        self.rect = self.box.get_rect(topleft=(DIALOG_BOX_X, DIALOG_BOX_Y))
        
        # Variáveis para diálogo sequencial
        self.current_speaker = ""
        self.npc = None

    def start_dialog(self, npc):
        """Inicia o diálogo com um NPC"""
        if self.active:
            return
            
        self.active = True
        self.npc = npc
        self.current_speaker = npc.dialog_sequence[0]["speaker"]
        self.current_text = npc.dialog_sequence[0]["text"]
        self.visible_text = ""
        self.text_progress = 0

    def update(self):
        """Atualiza a animação do texto"""
        if self.active and self.text_progress < len(self.current_text):
            self.text_progress += DIALOG_TEXT_SPEED
            self.visible_text = self.current_text[:int(self.text_progress)]

    def next_dialog(self):
        """Avança para o próximo diálogo na sequência"""
        if self.npc and self.npc.next_dialog():
            current_dialog = self.npc.get_current_dialog()
            if current_dialog:
                self.current_speaker = current_dialog["speaker"]
                self.current_text = current_dialog["text"]
                self.visible_text = ""
                self.text_progress = 0
                return True
        return False

    def draw(self, surface):
        """Desenha a caixa de diálogo"""
        if not self.active:
            return
            
        # Desenha a caixa
        surface.blit(self.box, self.rect)
        
        # Desenha nome do speaker
        speaker_color = (200, 200, 0) if self.current_speaker == "Player" else (0, 200, 200)
        speaker_surface = self.font.render(f"{self.current_speaker}:", True, speaker_color)
        surface.blit(speaker_surface, (self.rect.x + 10, self.rect.y + 10))
        
        # Desenha texto
        text_surface = self.font.render(self.visible_text, True, DIALOG_TEXT_COLOR)
        surface.blit(text_surface, (self.rect.x + 10, self.rect.y + 40))
        
        # Mostra "APERTE ESPAÇO" quando o texto estiver completo
        if self.text_progress >= len(self.current_text):
            continue_text = self.small_font.render("APERTE ESPAÇO PARA CONTINUAR", True, (200, 200, 200))
            surface.blit(continue_text, (self.rect.right - continue_text.get_width() - 10, 
                                       self.rect.bottom - continue_text.get_height() - 5))

    def close(self):
        """Fecha a caixa de diálogo"""
        self.active = False
        self.current_text = ""
        self.visible_text = ""
        self.text_progress = 0
        self.current_speaker = ""
        self.npc = None
class SlimeNPC(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = NPC_LAYER
        self.groups = self.game.all_sprites, self.game.npcs
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZES
        self.y = y * TILESIZES
        self.width = TILESIZES
        self.height = TILESIZES
        
        # Carrega as animações do slime
        self.animation_frames = {
            'idle': [
                self.game.slimenpc.get_sprite(1, 1, self.width, self.height)
            ]
        }
        
        # Configuração de animação
        self.current_frame = 0
        self.animation_speed = 10
        self.animation_counter = 0
        self.image = self.animation_frames['idle'][self.current_frame]
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Diálogo sequencial
        self.dialog_sequence = [
            {"speaker": "Slime", "text": "Blub! Blub! (olá...humano)"},
            {"speaker": "Slime", "text": "Blub, Blub, Blub! (Por favor, derrotar...goblins...malvados)"},
            {"speaker": "Player", "text": "Não entendo o que esse pedaço de catarro fala..."},
            {"speaker": "Player", "text": "Mas suponho que tenha a ver com aquelas coisas feias"}
        ]
        self.current_dialog_index = 0
        self.in_range = False
        self.can_interact = True  # Adicione esta linha para definir o atributo
        self.last_interact_time = 0
        self.interact_cooldown = 1000  # 1 segundo de cooldown
        
    def next_dialog(self):
        """Avança para o próximo diálogo na sequência"""
        self.current_dialog_index += 1
        if self.current_dialog_index < len(self.dialog_sequence):
            return True
        return False
    
    def get_current_dialog(self):
        """Retorna o diálogo atual"""
        if self.current_dialog_index < len(self.dialog_sequence):
            return self.dialog_sequence[self.current_dialog_index]
        return None
        
    def animate(self):
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames['idle'])
            self.image = self.animation_frames['idle'][self.current_frame]
            self.image.set_colorkey(BLACK)
            
    def update(self):
        self.animate()
        
        current_time = pygame.time.get_ticks()
        
        # Verifica colisão com o jogador
        if hasattr(self.game, 'player'):
            colliding = pygame.sprite.collide_rect(self, self.game.player)
            
            if colliding and not self.in_range and self.can_interact:
                self.in_range = True
                if not self.game.dialog_box.active:
                    self.current_dialog_index = 0
                    current_dialog = self.get_current_dialog()
                    if current_dialog:
                        self.game.dialog_box.start_dialog(self)
                        self.last_interact_time = current_time
                        self.can_interact = False
            
            if not colliding and self.in_range:
                self.in_range = False
                if self.game.dialog_box.active and self.game.dialog_box.npc == self:
                    self.game.dialog_box.close()
        
        # Verifica cooldown de interação
        if not self.can_interact and current_time - self.last_interact_time > self.interact_cooldown:
            self.can_interact = True
