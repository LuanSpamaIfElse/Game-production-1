import pygame
import sys
from sprites import *
from config import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont('arial.ttf', 32)
        self.dodge_bar = DodgeBar(self)
        

        #sprites geral
        self.character_spritesheet = Spritesheet('sprt/img/character.png')
        #terrenos
        self.terrain_spritesheet = Spritesheet('sprt/img/terrain.png')
        self.enemy_spritesheet = Spritesheet('sprt/img/enemy.png')
        self.attack_spritsheet = Spritesheet('sprt/guts-spr-full_noise1_scale.png')
        self.obstacle_spritesheet = Spritesheet ('sprt/img/TreesSpr.png')#640, 205
        self.plant_spritesheet = Spritesheet('sprt/img/terrain.png')
        self.block_spritesheet = Spritesheet('sprt/img/terrain.png')
        self.intro_background = pygame.image.load('sprt/img/introbackground.png')
        self.go_background = pygame.image.load('sprt/img/gameover.png')
        self.ability_panel = AbilityPanel(self)
    def createTilemap(self): 


        temp_tilemap = [list(row) for row in tilemap]  #Cria uma cópia modificável
        enemy_positions = []
        Obstacle_positions = []
    # Gerar posições aleatórias para inimigos
        while len(enemy_positions) < ENEMY_COUNT:
            x = random.randint(0, len(temp_tilemap[0]) - 1)
            y = random.randint(0, len(temp_tilemap) - 1)
            if temp_tilemap[y][x] == '.':  # Posição válida
                temp_tilemap[y][x] = 'E'
                enemy_positions.append((x, y))
    #Posição random obstacles
        while len(Obstacle_positions) < OBSTACLE_COUNT:
            x = random.randint(0, len(temp_tilemap[0]) - 1)
            y = random.randint(0, len(temp_tilemap) - 1)
            if temp_tilemap[y][x] == '.':  # Posição válida
                temp_tilemap[y][x] = 'O'
                Obstacle_positions.append((x, y))
        for i, row in enumerate(temp_tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "E":
                    enemy(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)
                if column == "Q":
                    Plant(self, j, i)
                if column == "O":
                    Obstacle(self, j, i)

    def new(self):
        #self.createTilemap()
        # Novo jogo começa
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.createTilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if hasattr(self, 'player') and self.player.can_attack():  # Verifica se o player existe e pode atacar
                        if self.player.facing == 'up':
                            Attack(self, self.player.rect.x, self.player.rect.y - 30)
                        elif self.player.facing == 'down':
                            Attack(self, self.player.rect.x, self.player.rect.y + 40)
                        elif self.player.facing == 'right':
                            Attack(self, self.player.rect.x + 40, self.player.rect.y)
                        elif self.player.facing == 'left':
                            Attack(self, self.player.rect.x - 30, self.player.rect.y)
                    #QUANTO MAIS BAIXO O VALOR, MAIS PROXIMO DO PLAYER
    def update(self):
        # Atualizações do game loop
        self.all_sprites.update()
        if hasattr(self, 'player'):
            # Calcula o deslocamento necessário para centralizar o jogador
            camera_offset_x = WIN_WIDTH // 2 - self.player.rect.centerx
            camera_offset_y = WIN_HEIGHT // 2 - self.player.rect.centery
            
            # Aplica o offset a todos os sprites
            for sprite in self.all_sprites:
                sprite.rect.x += camera_offset_x
                sprite.rect.y += camera_offset_y
            
            # Atualiza a posição real do jogador
            self.player.x += camera_offset_x
            self.player.y += camera_offset_y

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        self.dodge_bar.draw(self.screen)
        self.ability_panel.draw(self.screen)
        pygame.display.update()
    def main(self):
        # Loop do jogo
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        text = self.font.render('Game Over', True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        restart_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'Restart', 32)
        for sprite in self.all_sprites:
            sprite.kill()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.go_background, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True

        tittle = self.font.render('7° Portão', True, BLACK)
        tittle_rect = tittle.get_rect(x=10, y=10)

        play_button = Button(WIN_WIDTH/2, WIN_HEIGHT/2 , 100, 50, WHITE, BLACK, 'Play', 32)
        # adicionar botão Personagens
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(tittle, tittle_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

# Inicializando o jogo
g = Game()
g.intro_screen()
g.new()  # Corrigido: agora o método é chamado corretamente
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
