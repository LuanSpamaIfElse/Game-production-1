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
        self.character_spritesheet = Spritesheet('sprt/guts-spr-full_noise1_scale.png')
        #terrenos
        self.terrain_spritesheet = Spritesheet('sprt/terraintest.webp')
        self.enemy_spritesheet = Spritesheet('sprt/img/enemy.png')

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
        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass

# Inicializando o jogo
g = Game()
g.intro_screen()
g.new()  # Corrigido: agora o método é chamado corretamente
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
