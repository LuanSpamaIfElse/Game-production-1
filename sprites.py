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
        self.groups = [self.game.all_sprites]  # Certifique-se de que é uma lista
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Propriedades básicas
        self.x = x * TILESIZES
        self.y = y * TILESIZES
        self.width = TILESIZES
        self.height = TILESIZES
        self.x_change = 0
        self.y_change = 0
        self.facing = 'down'
        self.coins = 10

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
        self.damage = 1  # Dano base
        self.speed_boost = 0  # Bônus de velocidade
        self.attack_cooldown_multiplier = 1.0  # Multiplicador de cooldown
        self.dodge_cooldown_multiplier = 1.0  # Multiplicador de cooldown

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
        return current_time - self.last_attack_time >= ATTACK_COOLDOWN * self.attack_cooldown_multiplier
        
    def can_dodge(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_dodge_time >= DODGE_COOLDOWN * self.dodge_cooldown_multiplier

    def get_attack_cooldown_ratio(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.last_attack_time
        return min(elapsed / ATTACK_COOLDOWN, 1.0)
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

        shop_active = False
        for npc in self.game.npcs:
            if isinstance(npc, Seller2NPC) and npc.shop_active:
                shop_active = True
                break
        
        # Se a loja estiver ativa, não permite movimento
        if shop_active:
            self.x_change = 0
            self.y_change = 0
            return
        
        keys = pygame.key.get_pressed()
        # Reset movement
        self.x_change = 0
        self.y_change = 0
        
        # Movement logic - Teclado
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
        
        # Movement logic - Joystick
        if hasattr(self.game, 'joystick') and self.game.joystick:
            # Analógico esquerdo para movimento
            axis_x = self.game.joystick.get_axis(0)
            axis_y = self.game.joystick.get_axis(1)
            
            # Deadzone para evitar drift
            deadzone = 0.3
            if abs(axis_x) > deadzone:
                self.x_change += axis_x * PLAYER_SPEED
                self.facing = 'right' if axis_x > 0 else 'left'
            if abs(axis_y) > deadzone:
                self.y_change += axis_y * PLAYER_SPEED
                self.facing = 'down' if axis_y > 0 else 'up'
        
        # Dodge - Teclado
        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and self.can_dodge():
            self.last_dodge_time = pygame.time.get_ticks()
            self.x_change *= self.dodge_speed_multiplier
            self.y_change *= self.dodge_speed_multiplier
        
        # Dodge - Joystick (Botão 1)
        if (hasattr(self.game, 'joystick') and self.game.joystick and 
            self.game.joystick.get_button(2) and self.can_dodge()):  # Botão 1 (geralmente X no Xbox, Quadrado no PS)
            self.last_dodge_time = pygame.time.get_ticks()
            self.x_change *= self.dodge_speed_multiplier
            self.y_change *= self.dodge_speed_multiplier

    def kill(self):
    # Remove o jogador dos grupos de sprites
        for group in self.groups:
            group.remove(self)
        self.game.playing = False
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

#GROUNDS
            
class Ground1(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Posição do tile
        self.x = x * TILESIZES
        self.y = y * TILESIZES
        self.width = TILESIZES
        self.height = TILESIZES
        
        # Diferentes sprites para cada tilemap
        self.tilemap_sprites = {
            1: game.terrain_spritesheet.get_sprite(0, 352, self.width, self.height),
            2: game.terrain_spritesheet.get_sprite(256, 352, self.width+6, self.height)
        
        }
        
        # Carrega o sprite baseado no nível atual
        self.update_sprite()
        
        # Define o retângulo de colisão
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update_sprite(self):
        """Atualiza o sprite baseado no nível atual"""
        self.image = self.tilemap_sprites.get(self.game.current_level, 
                                            self.tilemap_sprites[1])  # Default para tilemap1
    
    def update(self):
        """Atualiza o sprite se o nível mudar"""
        self.update_sprite()
       

class Plant(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Posição da planta
        self.x = x * TILESIZES
        self.y = y * TILESIZES
        self.width = TILESIZES
        self.height = TILESIZES

        # Diferentes sprites para cada nível
        self.level_sprites = {
            1: self.game.plant_spritesheet.get_sprite(510, 352, self.width, self.height),
            2: self.game.plant_spritesheet.get_sprite(288, 352, self.width, self.height) # Exemplo com coordenadas diferentes
        }
        
        self.update_sprite()
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update_sprite(self):
        """Atualiza o sprite baseado no nível atual"""
        self.image = self.level_sprites.get(self.game.current_level, 
                                          self.level_sprites[1])  # Default para nível 1
    
    def update(self):
        """Atualiza o sprite se o nível mudar"""
        self.update_sprite()

class Portal(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PORTAL_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZES
        self.y = y * TILESIZES
        self.width = TILESIZES
        self.height = TILESIZES
        
        self.activated = False
        self.active = False  # Começa inativo
        self.pulse_effect = 0
        self.pulse_speed = 0.05
        self.pulse_max = 0.2

        # Carrega as animações do portal
        self.animation_frames = [
            self.game.portal_spritsheet.get_sprite(18, 15, self.width, 45),
            self.game.portal_spritsheet.get_sprite(83, 15, self.width, 45),
            self.game.portal_spritsheet.get_sprite(150, 15, self.width, 45)
        ]
        
        self.current_frame = 0
        self.animation_speed = 0.15
        self.animation_counter = 0
        
        self.image = self.animation_frames[self.current_frame]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        if self.active and hasattr(self.game, 'player') and not self.activated:
            if pygame.sprite.collide_rect(self, self.game.player):
                self.activated = True
                # Chama next_level diretamente após um pequeno delay
                pygame.time.delay(300)  # Pequeno delay para efeito visual
                self.game.next_level()
                return True
        return False  # Dispara evento após 300ms

    def animate(self):
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed * 60:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.current_frame]
            self.image.set_colorkey(BLACK)
            
        # Efeito de pulsação quando ativo
        if self.active:
            self.pulse_effect = (self.pulse_effect + self.pulse_speed) % (2 * math.pi)
            scale = 1 + math.sin(self.pulse_effect) * self.pulse_max
            old_center = self.rect.center
            self.image = pygame.transform.scale(self.animation_frames[self.current_frame], 
                                             (int(self.width * scale), int(self.height * scale)))
            self.rect = self.image.get_rect(center=old_center)

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
        self.animation_speed = 5
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
        
        # Aplica o movimento antes de verificar colisões
        self.rect.x += self.x_change
        self.collide_blocks('x')
        
        self.rect.y += self.y_change
        self.collide_blocks('y')
        
        # Verifica se o inimigo morreu
        if self.life <= 0:
            self.kill()
    def kill(self):
    # Remove o inimigo de todos os grupos
        for group in self.groups:
            group.remove(self)
        
        # Verifica se todos os inimigos foram derrotados
        if len(self.game.enemies) == 0:
            # Spawna o portal se não existir
            self.game.check_enemies_and_spawn_portal()

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
                    self.rect.right = hits[0].rect.left
                    self.facing = random.choice(['up', 'down', 'left'])  # Muda de direção
                if self.x_change < 0:  # Colisão ao mover para a esquerda
                    self.rect.left = hits[0].rect.right
                    self.facing = random.choice(['up', 'down', 'right'])  # Muda de direção

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                self.speed = ENEMY_SPEED / 2  # Reduz a velocidade pela metade ao colidir
                if self.y_change > 0:  # Colisão ao mover para baixo
                    self.rect.bottom = hits[0].rect.top
                    self.facing = random.choice(['up', 'left', 'right'])  # Muda de direção
                if self.y_change < 0:  # Colisão ao mover para cima
                    self.rect.top = hits[0].rect.bottom
                    self.facing = random.choice(['down', 'left', 'right'])  # Muda de direção

        

class EnemyCoin(pygame.sprite.Sprite):
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
                self.game.enemycoin_spritesheet.get_sprite(3, 98, self.width, self.height),
                self.game.enemycoin_spritesheet.get_sprite(35, 98, self.width, self.height),
                self.game.enemycoin_spritesheet.get_sprite(68, 98, self.width, self.height)
            ],
            'right': [
                self.game.enemycoin_spritesheet.get_sprite(3, 66, self.width, self.height),
                self.game.enemycoin_spritesheet.get_sprite(35, 66, self.width, self.height),
                self.game.enemycoin_spritesheet.get_sprite(68, 66, self.width, self.height)
           ],
            'up': [
                self.game.enemycoin_spritesheet.get_sprite(3, 35, self.width, self.height),
                self.game.enemycoin_spritesheet.get_sprite(35, 35, self.width, self.height),
                self.game.enemycoin_spritesheet.get_sprite(68, 35, self.width, self.height)
            ],
            'down' :[
                self.game.enemycoin_spritesheet.get_sprite(3, 3, self.width, self.height),
                self.game.enemycoin_spritesheet.get_sprite(35, 3, self.width, self.height),
                self.game.enemycoin_spritesheet.get_sprite(68, 3, self.width, self.height)
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
        
        # Aplica o movimento antes de verificar colisões
        self.rect.x += self.x_change
        self.collide_blocks('x')
        
        self.rect.y += self.y_change
        self.collide_blocks('y')
        
        # Verifica se o inimigo morreu
        if self.life <= 0:
            self.kill()
    def kill(self):
    # Remove o inimigo de todos os grupos
        for group in self.groups:
            group.remove(self)
        # Dropa uma moeda quando morre
        Coin(self.game, self.rect.centerx, self.rect.centery)
        # Verifica se todos os inimigos foram derrotados
        if len(self.game.enemies) == 0:
            # Spawna o portal se não existir
            self.game.check_enemies_and_spawn_portal()

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
        
        # Ícone da moeda
        self.coin_icon = self.game.coin.get_sprite(9, 5, 16, 16)  # Carrega o ícone da moeda
        
        # Textos pré-renderizados
        self.attack_text = self.text_font.render("ESPAÇO / 2", True, ABILITY_TEXT_COLOR)
        self.dodge_text = self.text_font.render("SHIFT / 3", True, ABILITY_TEXT_COLOR)
        
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
        
        # Barra de Dodge
        y_offset += 30
        self.draw_dodge_bar(surface, self.rect.x + 40, self.rect.y + y_offset)

        # Ícone de Moeda
        y_offset += 30
        surface.blit(self.coin_icon, (self.rect.x + 10, self.rect.y + y_offset))
        coin_text = self.text_font.render("Moedas:", True, ABILITY_TEXT_COLOR)
        surface.blit(coin_text, (self.rect.x + 40, self.rect.y + y_offset))
        coins_count = self.text_font.render(str(self.game.player.coins), True, ABILITY_TEXT_COLOR)
        surface.blit(coins_count, (self.rect.x + 120, self.rect.y + y_offset))
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

        # Posição do obstáculo
        self.x = x * TILESIZES
        self.y = y * TILESIZES
        self.width = TILESIZES
        self.height = TILESIZES

        # Diferentes sprites para cada nível
        self.level_sprites = {
            1: self.game.obstacle_spritesheet.get_sprite(640, 203, self.width-4, self.height-4),  # Tronco
            2: self.game.obstacle_spritesheet.get_sprite(670, 260, self.width, self.height)
        }
        
        self.update_sprite()
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update_sprite(self):
        """Atualiza o sprite baseado no nível atual"""
        self.image = self.level_sprites.get(self.game.current_level, 
                                          self.level_sprites[1])  # Default para nível 1
    
    def update(self):
        """Atualiza o sprite se o nível mudar"""
        self.update_sprite()



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
        self.width = TILESIZES   # Aumenta o tamanho do ataque
        self.height = TILESIZES
        
        self.animation_loop = 0
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)  # Surface transparente
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = self.game.player.facing  # Armazena a direção do jogador

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        for enemy in hits:
            enemy.take_damage()

    def update(self):
        self.animate()
        self.collide()

    def animate(self):
        direction = self.direction  # Usa a direção armazenada

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
            self.game.attack_spritsheet.get_sprite(0, 130, self.width, self.height)
        ]

        if direction == 'up':
            self.image = up_animations[0]
        elif direction == 'down':
            self.image = down_animations[0]
        elif direction == 'right':
            self.image = right_animations[0]
        elif direction == 'left':
            self.image = left_animations[0]
            
        # Mantém a posição relativa ao jogador
        
            
        # Remove o ataque após um curto período
        self.animation_loop += 0.5
        if self.animation_loop >= 2:  # Ajuste este valor conforme necessário
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
        #Inicia o diálogo com um NPC"""
        if self.active:
            return
            
        self.active = True
        self.npc = npc
        self.current_speaker = npc.dialog_sequence[0]["speaker"]
        self.current_text = npc.dialog_sequence[0]["text"]
        self.visible_text = ""
        self.text_progress = 1

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
            {'speaker': 'Slime', 'text': 'Blub! Blub! (olá...humano.)'},
            {"speaker": "Slime", "text": "Blub, Blub, Blub! (Derrotar...Goblins...Portal...Ativar)."},
            {"speaker": "Player", "text": "Não entendo o que esse pedaço de gosma fala..."},
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

class Seller1NPC(pygame.sprite.Sprite): #vendedor dialogo
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
                self.game.seller_spritesheet.get_sprite(1, 0, self.width, self.height),
                self.game.seller_spritesheet.get_sprite(1, 32, self.width, self.height)
            ]
        }
        
        # Configuração de animação
        self.current_frame = 0
        self.animation_speed = 30
        self.animation_counter = 0
        self.image = self.animation_frames['idle'][self.current_frame]
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Diálogo sequencial
        self.dialog_sequence = [
            {'speaker': '???', 'text': 'Olá, Forasteiro.'},
            {"speaker": "Player", "text": "Quem é você?"},
            {"speaker": "Mercador", "text": "Apenas um vendedor ambulante pelas regiôes."},
            {"speaker": "Player", "text": "uhm... boto fé..."},
            {"speaker": "Mercador", "text": "Está precisando de algumas melhorias em seu equipamento? Forasteiro."},
            {"speaker": "Player", "text": "Não... por enquanto..."},
            {"speaker": "Mercador", "text": "He he he he, te vejo por aí, Forasteiro"}
        ]
        self.current_dialog_index = 0
        self.in_range = False
        self.can_interact = True  # Adicione esta linha para definir o atributo
        self.last_interact_time = 1
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

class Seller2NPC(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = NPC_LAYER
        self.groups = self.game.all_sprites, self.game.npcs
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZES
        self.y = y * TILESIZES
        self.width = TILESIZES
        self.height = TILESIZES

        self.animation_frames = {
            'idle': [
                self.game.seller_spritesheet.get_sprite(1, 0, self.width, self.height),
                self.game.seller_spritesheet.get_sprite(1, 32, self.width, self.height)
            ]
        }
        
        # Variáveis de animação
        self.current_frame = 0
        self.animation_speed = 30  # Velocidade da animação (ajuste conforme necessário)
        self.animation_counter = 0
        
        # Define a imagem inicial
        self.image = self.animation_frames['idle'][self.current_frame]
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        
        # Variáveis de interação
        self.in_range = False
        self.shop_active = False
        self.selected_option = 0
        self.interact_cooldown = 1000
        self.last_interact_time = 0
        
        # Opções da loja
        self.upgrade_options = [
            {"name": "Vida", "cost": 5, "description": "Recupera toda a vida", "effect": self.upgrade_health},
            {"name": "Dano", "cost": 2, "description": "+2 de dano no ataque", "effect": self.upgrade_damage},
            {"name": "Velocidade", "cost": 2, "description": "+1 de velocidade", "effect": self.upgrade_speed},
            {"name": "Recarga", "cost": 3, "description": "-30% tempo de recarga", "effect": self.upgrade_cooldown}
        ]

    def upgrade_health(self, player):
        if player.coins >= 5:
            player.coins -= 5
            player.life = PLAYER_LIFE
            return True
        return False
    
    def upgrade_damage(self, player):
        if player.coins >= 2:
            player.coins -= 2
            if not hasattr(player, 'damage'):
                player.damage = 1
            player.damage += 2
            return True
        return False
    
    def upgrade_speed(self, player):
        if player.coins >= 2:
            player.coins -= 2
            player.speed_boost = getattr(player, 'speed_boost', 0) + 1
            return True
        return False
    
    def upgrade_cooldown(self, player):
        if player.coins >= 3:
            player.coins -= 3
            player.attack_cooldown_multiplier = getattr(player, 'attack_cooldown_multiplier', 1) * 0.7
            player.dodge_cooldown_multiplier = getattr(player, 'dodge_cooldown_multiplier', 1) * 0.7
            return True
        return False
    
    # Configurações visuais da seleção
        self.selection_bg = pygame.Surface((SHOP_WIDTH - 40, 40), pygame.SRCALPHA)
        self.selection_bg.fill((100, 100, 100, 150))  # Cinza transparente
        
        # Tempo mínimo entre interações
        self.last_interact_time = 0
        self.interact_cooldown = 300  # 0.3 segundos

    def draw_shop(self, surface):
        if not self.shop_active:
            return
            
        # Fundo semi-transparente
        shop_bg = pygame.Surface((SHOP_WIDTH, SHOP_HEIGHT), pygame.SRCALPHA)
        shop_bg.fill(SHOP_BG_COLOR)
        surface.blit(shop_bg, (SHOP_X, SHOP_Y))
        
        # Título
        title_font = pygame.font.SysFont('arial', SHOP_TITLE_FONT_SIZE, bold=True)
        title = title_font.render("Loja de Melhorias", True, SHOP_TITLE_COLOR)
        surface.blit(title, (SHOP_X + SHOP_WIDTH//2 - title.get_width()//2, SHOP_Y + 20))
        
        # Moedas do jogador
        coin_font = pygame.font.SysFont('arial', SHOP_FONT_SIZE)
        coin_text = coin_font.render(f"Moedas: {self.game.player.coins}", True, (255, 215, 0))
        surface.blit(coin_text, (SHOP_X + 20, SHOP_Y + 60))
        
        # Opções de upgrade
        option_font = pygame.font.SysFont('arial', SHOP_FONT_SIZE)
        for i, option in enumerate(self.upgrade_options):
            color = SHOP_SELECTED_COLOR if i == self.selected_option else SHOP_OPTION_COLOR
            text = option_font.render(f"{option['name']} - {option['cost']} moedas", True, color)
            surface.blit(text, (SHOP_X + 40, SHOP_Y + 100 + i * 40))
            
            desc = option_font.render(option['description'], True, SHOP_TEXT_COLOR)
            surface.blit(desc, (SHOP_X + 60, SHOP_Y + 120 + i * 40))
    
    def handle_shop_input(self):
        current_time = pygame.time.get_ticks()
        
        # Controles de teclado
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and current_time - self.last_interact_time > self.interact_cooldown:
            self.selected_option = (self.selected_option - 1) % len(self.upgrade_options)
            self.last_interact_time = current_time
        elif keys[pygame.K_DOWN] and current_time - self.last_interact_time > self.interact_cooldown:
            self.selected_option = (self.selected_option + 1) % len(self.upgrade_options)
            self.last_interact_time = current_time
        
        # Compra com espaço ou botão do joystick
        if (keys[pygame.K_SPACE] or 
            (self.game.joystick and self.game.joystick.get_button(0))):  # Botão 1 (X no Xbox, Quadrado no PS)
            if current_time - self.last_interact_time > self.interact_cooldown:
                selected = self.upgrade_options[self.selected_option]
                if self.game.player.coins >= selected["cost"]:
                    if selected["effect"](self.game.player):
                        # Feedback visual/sonoro de compra bem-sucedida
                        pass
                self.last_interact_time = current_time
        
        # Fechar com ESC ou botão do joystick
        if keys[pygame.K_ESCAPE] or (self.game.joystick and self.game.joystick.get_button(1)):  # Botão 2 (A no Xbox, X no PS)
            if current_time - self.last_interact_time > self.interact_cooldown:
                self.shop_active = False
                self.last_interact_time = current_time
    def animate(self):
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames['idle'])
            self.image = self.animation_frames['idle'][self.current_frame]
            self.image.set_colorkey(BLACK)

    def update(self):
        current_time = pygame.time.get_ticks()
        
        if hasattr(self.game, 'player'):
            colliding = pygame.sprite.collide_rect(self, self.game.player)
            
            # Abre automaticamente quando colide
            if colliding and not self.shop_active and current_time - self.last_interact_time > self.interact_cooldown:
                self.shop_active = True
                self.selected_option = 0
                self.last_interact_time = current_time
            
            # Fecha quando sai de perto
            if not colliding and self.shop_active:
                self.shop_active = False
            
            # Processa inputs se a loja estiver aberta
            if self.shop_active:
                self.handle_shop_input()
    def activate_shop(self):
        self.shop_active = True
        self.selected_option = 0
        self.last_interact_time = pygame.time.get_ticks()
        # Pode adicionar um efeito sonoro aqui
    
    def deactivate_shop(self):
        self.shop_active = False
        self.last_interact_time = pygame.time.get_ticks()
        # Pode adicionar um efeito sonoro aqui
class Coin(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ITEM_LAYER  # Adicione ITEM_LAYER no config.py com valor apropriado
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x
        self.y = y
        self.width = TILESIZES // 2
        self.height = TILESIZES // 2
        
        # Animação da moeda
        self.animation_frames = [
            self.game.coin.get_sprite(9, 5, 16, 16),
            self.game.coin.get_sprite(74, 5, 16, 16),
            self.game.coin.get_sprite(43, 36, 16, 16),
            self.game.coin.get_sprite(43, 70, 16, 16)
        ]
        
        self.current_frame = 0
        self.animation_speed = 0.1
        self.animation_counter = 0
        
        self.image = self.animation_frames[self.current_frame]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        # Tempo de vida da moeda
        self.lifetime = 20000  # 10 segundos
        self.spawn_time = pygame.time.get_ticks()
    
    def update(self):
        # Atualiza animação
        self.animate()
        
        # Verifica colisão com o jogador
        if hasattr(self.game, 'player'):
            if pygame.sprite.collide_rect(self, self.game.player):
                self.game.player.coins += 1  # Incrementa contador de moedas
                self.kill()
        
        # Verifica tempo de vida
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()
    
    def animate(self):
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed * 60:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.current_frame]
            self.image.set_colorkey(BLACK)
