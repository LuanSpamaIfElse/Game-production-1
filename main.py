import pygame
import sys
from sprites import *
from config import *



class Game:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Joystick conectado: {self.joystick.get_name()}")
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont('arial.ttf', 32)
        self.dialog_box = DialogBox(self)
        self.next_level_triggered = False
        
        # Inicializa grupos de sprites
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.npcs = pygame.sprite.LayeredUpdates()

        # Carrega sprites
        self.character_spritesheet = Spritesheet('sprt/img/character.png')
        self.terrain_spritesheet = Spritesheet('sprt/terrain/terrain.png')
        self.obstacle_spritesheet = Spritesheet('sprt/terrain/TreesSpr.png')
        self.portal_spritsheet = Spritesheet('sprt/terrain/portalpurplespr.png')
        self.enemy_spritesheet = Spritesheet('sprt/img/enemy.png')
        self.attack_spritsheet = Spritesheet('sprt/guts-spr-full_noise1_scale.png')
        self.plant_spritesheet = Spritesheet('sprt/terrain/terrain.png')
        self.block_spritesheet = Spritesheet('sprt/terrain/terrain.png')
        self.intro_background = pygame.image.load('sprt/img/introbackground.png')
        self.go_background = pygame.image.load('sprt/img/gameover.png')
        self.slimenpc = Spritesheet('sprt/npc/slime_spr.png')
        self.seller_spritesheet = Spritesheet('sprt/npc/sellernpc_64x100.png')

        #carregar sounds
        
        
        self.ability_panel = AbilityPanel(self)
        self.current_level = 1
        self.max_levels = 3

    def next_level(self):
        if self.current_level < self.max_levels:
            print(f"Transicionando para o nível {self.current_level + 1}")
            
            # Preserva a vida do jogador
            player_life = self.player.life if hasattr(self, 'player') else PLAYER_LIFE
            
            # Limpa todos os sprites
            self.all_sprites.empty()
            self.blocks.empty()
            self.enemies.empty()
            self.attacks.empty()
            self.npcs.empty()
            
            # Avança para o próximo nível
            self.current_level += 1
            
            # Recria o tilemap com o jogador
            self.createTilemap(create_player=True)
            
            # Restaura a vida do jogador
            if hasattr(self, 'player'):
                self.player.life = player_life
        else:
            # Se não há mais níveis, volta para o primeiro
            print("Reiniciando para o nível 1")
            self.current_level = 1
            self.new()

    def createTilemap(self, create_player=True):
        """Cria o tilemap baseado no nível atual"""
        try:
            # Verifica qual mapa usar
            if self.current_level == 1 and 'tilemap' in globals():
                current_tilemap = tilemap
            elif self.current_level == 2 and 'tilemap2' in globals():
                current_tilemap = tilemap2
            else:
                raise ValueError(f"Tilemap para nível {self.current_level} não encontrado")
            
            # Cria uma cópia do tilemap para modificar
            temp_tilemap = [list(row) for row in current_tilemap]
            obstacle_positions = []
            
            # Posiciona obstáculos aleatórios
            while len(obstacle_positions) < OBSTACLE_COUNT:
                x = random.randint(0, len(temp_tilemap[0]) - 1)
                y = random.randint(0, len(temp_tilemap) - 1)
                if temp_tilemap[y][x] == '.':
                    temp_tilemap[y][x] = 'O'
                    obstacle_positions.append((x, y))
            
            # Cria os sprites baseados no tilemap
            for i, row in enumerate(temp_tilemap):
                for j, column in enumerate(row):
                    Ground1(self, j, i)
                    if column == "B":
                        Block(self, j, i)
                    if column == "E":
                        enemy(self, j, i)
                    if column == "P" and create_player:  # Só cria jogador se permitido
                        self.player = Player(self, j, i)
                    if column == "Q":
                        Plant(self, j, i)
                    if column == "O":
                        Obstacle(self, j, i)
                    if column == "S":
                        SlimeNPC(self, j, i)
                    if column == "T":
                        Portal(self, j, i)
                    if column == "M":
                        Seller1NPC(self, j, i)
                        
        except Exception as e:
            print(f"Erro ao criar tilemap: {e}")
            # Tenta recarregar o nível anterior
            if self.current_level > 1:
                self.current_level -= 1
                self.createTilemap(create_player)
            else:
                # Fallback para um mapa básico se o nível 1 também falhar
                temp_tilemap = [["." for _ in range(10)] for _ in range(10)]
                if create_player:
                    temp_tilemap[5][5] = "P"  # Adiciona o player
                self.createTilemap(create_player)
        #

    def new(self):
    #"""Inicia um novo jogo"""
        self.playing = True
        self.current_level = 1  # Sempre começa no nível 1
        
        # Limpa todos os sprites
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.npcs = pygame.sprite.LayeredUpdates()
        
        # Cria o tilemap inicial (cria jogador automaticamente)
        self.createTilemap(create_player=True)
            

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    if self.screen.get_flags() & pygame.FULLSCREEN:
                        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
                    else:
                        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.FULLSCREEN)
                if event.key == pygame.K_SPACE:
                    if hasattr(self, 'dialog_box') and self.dialog_box.active:
                        if self.dialog_box.text_progress < len(self.dialog_box.current_text):
                            self.dialog_box.text_progress = len(self.dialog_box.current_text)
                            self.dialog_box.visible_text = self.dialog_box.current_text
                        else:
                            if not self.dialog_box.next_dialog():
                                self.dialog_box.close()
                    elif hasattr(self, 'player') and self.player.can_attack() and self.player.life > 0:
                        self.player.last_attack_time = pygame.time.get_ticks()
                        self.player_attack()
            
            # Controle de joystick - Ataque (Botão 2)
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 1 and hasattr(self, 'player') and self.player.can_attack() and self.player.life > 0:  # Botão 2 (geralmente A no Xbox, X no PS)
                    self.player.last_attack_time = pygame.time.get_ticks()
                    self.player_attack()
    
    def player_attack(self):
        """Centraliza a lógica de ataque para ser chamada tanto por teclado quanto por joystick"""
        if self.player.facing == 'up':
            Attack(self, self.player.rect.x, self.player.rect.y - 30)
        elif self.player.facing == 'down':
            Attack(self, self.player.rect.x, self.player.rect.y + 40)
        elif self.player.facing == 'right':
            Attack(self, self.player.rect.x + 40, self.player.rect.y)
        elif self.player.facing == 'left':
            Attack(self, self.player.rect.x - 30, self.player.rect.y)

    def update(self):
        # Atualizações do game loop
        self.all_sprites.update()
    
    # Verifica inimigos e spawna portal se necessário
        self.check_enemies_and_spawn_portal()
    
    
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
        # Desenha as barras de vida após os sprites
        if hasattr(self, 'player'):
            self.player.draw_health_bar(self.screen)
        
        for enemy in self.enemies:
            enemy.draw_health_bar(self.screen)

        
        self.clock.tick(FPS)
        self.ability_panel.draw(self.screen)
        self.dialog_box.draw(self.screen)
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
                pygame.mixer.music.load(SongFlorest)
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.15) 
                intro = False
            
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(tittle, tittle_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def check_enemies_and_spawn_portal(self):
        if len(self.enemies) == 0:
            # Procura por portais existentes primeiro
            for sprite in self.all_sprites:
                if isinstance(sprite, Portal):
                    sprite.active = True
                    return
                    
            # Se não encontrou portal, cria um novo
            if hasattr(self, 'player'):
                # Posiciona o portal próximo ao jogador
                x_pos = (self.player.rect.x // TILESIZES) + 2
                y_pos = self.player.rect.y // TILESIZES
                portal = Portal(self, x_pos, y_pos)
                portal.active = True
# Inicializando o jogo
g = Game()
g.intro_screen()
g.new()  # Corrigido: agora o método é chamado corretamente
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
