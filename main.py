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

        #sprites geral
        self.character_spritesheet = Spritesheet('sprt/guts-spr-full_noise1_scale.png')
        #terrenos
        self.terrain_spritesheet = Spritesheet('sprt/img/terrain.png')
        self.enemy_spritesheet = Spritesheet('sprt/img/enemy.png')
        self.plant_spritesheet = Spritesheet('sprt/img/terrain.png')
        self.block_spritesheet = Spritesheet('sprt/img/terrain.png')
        self.intro_background = pygame.image.load('sprt/img/introbackground.png')
        self.go_background = pygame.image.load('sprt/img/gameover.png')
    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "E":
                    enemy(self, j, i)
                if column == "P":
                    Player(self, j, i)
                if column == "Q":
                    Plant(self, j, i)
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
        # Game loop (eventos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                return  # Evita continuar processando eventos após sair

    def update(self):
        # Atualizações do game loop
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.update()
        self.clock.tick(FPS)

    def main(self):
        # Loop do jogo
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        text = self.font.render('Game Over', True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

        restart_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'Restart', 32)

    # Limpa todos os sprites
        for sprite in self.all_sprites:
            sprite.kill()  # Agora sim, usando o kill() original do Pygame

        while self.running:
        # Captura a posição do mouse e o estado dos botões do mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

        # Verifica eventos DENTRO do loop (corrigindo a indentação)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

        # Verifica se o botão de reiniciar foi pressionado
        if restart_button.is_pressed(mouse_pos, mouse_pressed):
            self.new()  # Reinicia o jogo
            self.main()  # Volta ao loop principal do jogo
            return  # Sai da função game_over após reiniciar

        # Desenha a tela de Game Over
        self.screen.blit(self.go_background, (0, 0))
        self.screen.blit(text, text_rect)
        self.screen.blit(restart_button.image, restart_button.rect)

        self.clock.tick(FPS)
        pygame.display.update()

        # Verifica se o botão de reiniciar foi pressionado
        if restart_button.is_pressed(mouse_pos, mouse_pressed):
            self.new()  # Reinicia o jogo
            self.main()  # Volta ao loop principal do jogo

        # Desenha a tela de Game Over
        self.screen.blit(self.go_background, (0, 0))
        self.screen.blit(text, text_rect)
        self.screen.blit(restart_button.image, restart_button.rect)

        self.clock.tick(FPS)
        pygame.display.update()

    def intro_screen(self):
        intro = True

        tittle = self.font.render('Mata Macaco', True, BLACK)
        tittle_rect = tittle.get_rect(x=10, y=10)

        play_button = Button(WIN_WIDTH/2, WIN_HEIGHT/2 , 100, 50, WHITE, BLACK, 'Play', 32)

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
g.new()

while g.running:
    g.main()
    if not g.playing:  # Se o jogo terminou (por morte do jogador)
        g.game_over()  # Agora o game_over é chamado no lugar certo

pygame.quit()
sys.exit()
