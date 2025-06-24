import pygame
import sys
from sprites import *
from config import *



class Game:
    def __init__(self):
        pygame.mixer.init()
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
        
        # Atributos do jogador (serão definidos na seleção)
        self.player_attrs = {}  # Atributos serão preenchidos pela tela de seleção
        
        # Inicializa grupos de sprites
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.bats = pygame.sprite.LayeredUpdates() # Mantido como bats
        self.attacks = pygame.sprite.LayeredUpdates()
        self.npcs = pygame.sprite.LayeredUpdates()
        self.water = pygame.sprite.LayeredUpdates()
        self.bosses = pygame.sprite.LayeredUpdates() # Novo grupo para o boss
        self.fire_areas = pygame.sprite.LayeredUpdates() # Novo grupo para áreas de fogo

        self.Player1_spritesheet = Spritesheet('sprt/img/character.png')
        self.terrain_spritesheet = Spritesheet('sprt/terrain/terrain.png')
        self.obstacle_spritesheet = Spritesheet('sprt/terrain/TreesSpr.png')
        self.portal_spritsheet = Spritesheet('sprt/terrain/portalpurplespr.png')
        self.enemy_spritesheet = Spritesheet('sprt/img/enemy.png')
        self.enemycoin_spritesheet = Spritesheet('sprt/img/enemy.png')
        self.bats_spritesheet = Spritesheet('sprt/npc/bat.png')
        self.coin = Spritesheet('sprt/img/coin_spr.png')
        self.attack_spritsheet = Spritesheet('sprt/guts-spr-full_noise1_scale.png')
        self.plant_spritesheet = Spritesheet('sprt/terrain/terrain.png')
        self.block_spritesheet = Spritesheet('sprt/terrain/terrain.png')
        self.intro_background = pygame.image.load('sprt/img/introbackground.png')
        self.go_background = pygame.image.load('sprt/img/gameover.png')
        self.slimenpc = Spritesheet('sprt/npc/slime_spr.png')
        self.seller_spritesheet = Spritesheet('sprt/npc/seller.png')
        
        self.ability_panel = AbilityPanel(self)
        self.current_level = 1
        self.max_levels = 8


    def character_selection_screen(self):
        selected = 1
        
        
        title_font = pygame.font.SysFont('arial', 48, bold=True)
        char_font = pygame.font.SysFont('arial', 36)
        desc_font = pygame.font.SysFont('arial', 24)
        
        left_btn = Button(100, WIN_HEIGHT//2, 50, 50, WHITE, BLACK, "<", 32)
        right_btn = Button(WIN_WIDTH-150, WIN_HEIGHT//2, 50, 50, WHITE, BLACK, ">", 32)
        play_btn = Button(WIN_WIDTH//2 - 60, WIN_HEIGHT - 100, 120, 50, WHITE, BLACK, "Jogar", 32)

        # Carrega imagens dos personagens (como no seu código original)
        
        selecting = True
        while selecting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            if left_btn.is_pressed(mouse_pos, mouse_pressed):
                selected = (selected - 2) % len(CHARACTERS) + 1
                pygame.time.delay(200)
            if right_btn.is_pressed(mouse_pos, mouse_pressed):
                selected = selected % len(CHARACTERS) + 1
                pygame.time.delay(200)
            if play_btn.is_pressed(mouse_pos, mouse_pressed):
                self.player_attrs = CHARACTERS[selected]
                selecting = False
            
            # FUNDO (primeiro)
            self.screen.blit(self.intro_background, (0,0))
            
            # --- PAINEL COM TRANSPARÊNCIA IGUAL À LOJA ---
            panel_width = 640
            panel_height = 400
            panel_x = WIN_WIDTH // 2 - panel_width // 2
            panel_y = WIN_HEIGHT // 2 - panel_height // 2
            
            # Cria uma superfície com alpha
            panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            
            # Preenche com a cor da loja (UI_BG_COLOR) com transparência
            pygame.draw.rect(panel_surface, UI_BG_COLOR, (0, 0, panel_width, panel_height), border_radius=15)
            
            # Borda branca como na loja (UI_BORDER_COLOR)
            pygame.draw.rect(panel_surface, UI_BORDER_COLOR, (0, 0, panel_width, panel_height), width=UI_BORDER_WIDTH, border_radius=15)
            
            # Desenha a superfície na tela
            self.screen.blit(panel_surface, (panel_x, panel_y))
            
            # --- CONTEÚDO DO PAINEL ---
            current_char = CHARACTERS[selected]
            
            # Título
            title = title_font.render("Selecione seu personagem", True, UI_TITLE_COLOR)  # Usa a cor dourada do título
            self.screen.blit(title, (WIN_WIDTH//2 - title.get_width()//2, panel_y +17))
            
            # Imagem do personagem (centralizada no painel) - AJUSTADO
            try:
                char_img = pygame.image.load(current_char["sprite"]).convert_alpha()
                char_img = pygame.transform.scale(char_img, (200, 200))
                # Modificado: de panel_y + 150 para panel_y + 160
                img_rect = char_img.get_rect(center=(WIN_WIDTH//2, panel_y + 170))
                self.screen.blit(char_img, img_rect)
            except:
                # Fallback se a imagem não carregar
                placeholder = pygame.Surface((200, 200))
                placeholder.fill(RED)
                # Modificado: de panel_y + 50 para panel_y + 60
                self.screen.blit(placeholder, (WIN_WIDTH//2 - 100, panel_y + 60))
            
            # Textos com as cores da UI - AJUSTADOS
            name_text = char_font.render(current_char["name"], True, UI_FONT_COLOR)  # Branco
            # Modificado: de panel_y + 250 para panel_y + 260
            self.screen.blit(name_text, (WIN_WIDTH//2 - name_text.get_width()//2, panel_y + 280))
            
            stats_text = desc_font.render(
                f"Vida: {current_char['life']} | Dano: {current_char['damage']} | Velocidade: {current_char['speed']}", 
                True, SELECTED_COLOR  # Amarelo brilhante
            )
            # Modificado: de panel_y + 290 para panel_y + 300
            self.screen.blit(stats_text, (WIN_WIDTH//2 - stats_text.get_width()//2, panel_y + 320))
            
            desc_text = desc_font.render(current_char["description"], True, UI_FONT_COLOR)  # Branco
            # Modificado: de panel_y + 320 para panel_y + 330
            self.screen.blit(desc_text, (WIN_WIDTH//2 - desc_text.get_width()//2, panel_y + 350))
            
            # Botões
            self.screen.blit(left_btn.image, left_btn.rect)
            self.screen.blit(right_btn.image, right_btn.rect)
            self.screen.blit(play_btn.image, play_btn.rect)
            
            
            pygame.display.update()
            self.clock.tick(FPS)
    
    

    def intro_screen(self):
        intro = True
        
        title = self.font.render('GameAdventure', True, BLACK)
        title_rect = title.get_rect(x=10, y=10)

        play_button = Button(WIN_WIDTH/2, WIN_HEIGHT/2, 100, 50, WHITE, BLACK, 'Play', 32)
        
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                self.character_selection_screen()  # Chama a nova tela de seleção
                intro = False
            
            #self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
    def start_game(self):
        """Inicia o jogo com o personagem selecionado"""
        try:
            pygame.mixer.music.load(MUSIC_LEVELS[1])
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.15)
        except Exception as e:
            print(f"Erro ao carregar música: {e}")
        
        self.new()
    def next_level(self):
        player_life = self.player.life if hasattr(self, 'player') else PLAYER_LIFE
        player_coins = self.player.coins if hasattr(self, 'player') else 0

        # Limpa todos os sprites
        self.all_sprites.empty()
        self.blocks.empty()
        self.bats.empty() # Corrigido para bats
        self.enemies.empty()
        self.attacks.empty()
        self.npcs.empty()
        self.water.empty()
        self.bosses.empty() # Limpa o grupo do boss ao mudar de nível
        self.fire_areas.empty() # Limpa as áreas de fogo

        # Verifica se deve carregar a loja ou o próximo nível normal
        if getattr(self, 'loading_store', False):
            # Jogador está na loja, agora deve avançar para o próximo level normal
            self.loading_store = False
            self.current_level += 1
            next_map = self.current_level
            music = MUSIC_LEVELS.get(self.current_level, MUSIC_LEVELS[1])
            create_player = True
        else:
            # Jogador terminou level normal, agora vai para a loja
            self.loading_store = True
            next_map = 'store'
            music = MUSIC_LEVELS.get('store')
            create_player = True

        if self.current_level > self.max_levels: # Verifica se é o último nível antes do boss
            print("Todos os níveis normais completados! Preparando para o boss...")
            self.load_boss_level() # Chama o método para carregar o nível do boss
            return

        print(f"Loading {next_map}")

        # Cria o mapa
        self.createTilemap(create_player=create_player, force_map=next_map)

        # Mantém a vida e moedas do jogador
        if hasattr(self, 'player'):
            self.player.life = player_life
            self.player.coins = player_coins

        # Toca a música
        if music:
            try:
                pygame.mixer.music.load(music)
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.15)
            except Exception as e:
                print(f"Erro ao carregar música: {e}")


    def load_boss_level(self):
        # Limpa todos os sprites novamente para o nível do boss
        self.all_sprites.empty()
        self.blocks.empty()
        self.enemies.empty()
        self.bats.empty()
        self.attacks.empty()
        self.npcs.empty()
        self.water.empty()
        self.bosses.empty()
        self.fire_areas.empty()

        # Carrega o mapa do boss (o último mapa na sua lista MAPS em sprites.py)
        self.createTilemap(create_player=True, force_map='boss_arena') # Adicionado 'boss_arena' como um identificador
        
        # Mantém a vida e moedas do jogador, recria o player no novo mapa
        if hasattr(self, 'player'):
            self.player.life = self.player.life # Mantém a vida atual
            self.player.coins = self.player.coins # Mantém as moedas atuais

        print("Carregando mapa do boss!")
        # Adicione música específica para o boss, se tiver
        try:
            # Assumindo que a música do boss está em MUSIC_LEVELS['boss']
            pygame.mixer.music.load(MUSIC_LEVELS.get('boss', MUSIC_LEVELS[1]))
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.15)
        except Exception as e:
            print(f"Erro ao carregar música do boss: {e}")


                
    def createTilemap(self, create_player=True, force_map=None):
        try:
            # Determina qual mapa usar
            if force_map == 'store':
                current_tilemap = store
            elif force_map == 'boss_arena': # Nova condição para o mapa do boss
                current_tilemap = MAPS[-1] # Pega o último mapa da lista, que é a arena do boss
            elif self.current_level == 1:
                current_tilemap = tilemap
            elif self.current_level == 2:
                current_tilemap = tilemap2
            elif self.current_level == 3:
                current_tilemap = tilemap3
            elif self.current_level == 4:
                current_tilemap = tilemap4

            
            # Restante do método permanece o mesmo...
            # Cria uma cópia do tilemap para modificar
            temp_tilemap = [list(row) for row in current_tilemap]
            obstacle_positions = []
            
            # Só adiciona obstáculos se não for a loja
            if force_map not in ['store', 'boss_arena'] and self.current_level != 2: # Exclui boss_arena também
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
                    if column == "E" and force_map not in ['store', 'boss_arena']:  # Só inimigos fora da loja e arena do boss
                        enemy(self, j, i)
                    if column == "C" and force_map not in ['store', 'boss_arena']:
                        EnemyCoin(self, j, i)
                    if column == "P" and create_player:
                        self.player = Player(self, j, i)
                    if column == "Q":
                        Plant(self, j, i)
                    if column == "O" and force_map not in ['store', 'boss_arena'] and self.current_level != 2:
                        Obstacle(self, j, i)
                    if column == "S":
                        SlimeNPC(self, j, i)
                    if column == "T":
                        Portal(self, j, i)
                    if column == "M":
                        Seller1NPC(self, j, i)
                    if column == "V":
                        Seller2NPC(self, j, i)
                    if column == "W":
                        Water1(self, j, i)
                    if column == "G" and self.current_level == 3:
                        Bat(self, j, i)
                    if column == "N": # Spawna Nero apenas na arena do boss
                        self.nero = Nero(self, j, i)
                        
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

    def new(self):
    #"""Inicia um novo jogo"""
        pygame.mixer.init()
        self.playing = True
        self.character_selection_screen()
        self.current_level = 1  # Sempre começa no nível 1, não no 4
        
        # Limpa todos os sprites
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.bats = pygame.sprite.LayeredUpdates() # Corrigido para bats
        self.attacks = pygame.sprite.LayeredUpdates()
        self.npcs = pygame.sprite.LayeredUpdates()
        self.bosses = pygame.sprite.LayeredUpdates() # Reinicia o grupo do boss
        self.fire_areas = pygame.sprite.LayeredUpdates() # Reinicia o grupo de áreas de fogo
        
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
                        self.perform_attack()
            
            # Controle de joystick - Ataque (Botão 2)
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 1 and hasattr(self, 'player') and self.player.can_attack() and self.player.life > 0:  # Botão 2 (geralmente A no Xbox, X no PS)
                    self.player.last_attack_time = pygame.time.get_ticks()
                    self.perform_attack()

                if event.button == 1 and hasattr(self, 'dialog_box') and self.dialog_box.active:
                    if self.dialog_box.text_progress < len(self.dialog_box.current_text):
                        self.dialog_box.text_progress = len(self.dialog_box.current_text)
                        self.dialog_box.visible_text = self.dialog_box.current_text
                    else:
                        if not self.dialog_box.next_dialog():
                            self.dialog_box.close()
                
    def perform_attack(self):
        """
        Performs an attack based on the player's character type.
        This is where you will add logic for other characters.
        """
        # --- SWORDSMAN ATTACK (Player 1) ---
        if self.player.char_type == 'swordsman':
            if self.player.facing == 'up':
                SwordAttack(self, self.player.rect.x, self.player.rect.y - 35)
            elif self.player.facing == 'down':
                SwordAttack(self, self.player.rect.x, self.player.rect.y + 40)
            elif self.player.facing == 'right':
                SwordAttack(self, self.player.rect.x + 40, self.player.rect.y)
            elif self.player.facing == 'left':
                SwordAttack(self, self.player.rect.x - 30, self.player.rect.y)
        
        # --- ARCHER ATTACK (Player 2) - FUTURE IMPLEMENTATION ---
        elif self.player.char_type == 'archer':
            # TODO: Add logic to fire an arrow here.
            # Example: Arrow(self, self.player.rect.centerx, self.player.rect.centery, self.player.facing)
            print("Archer attack is not implemented yet.")

        # --- TANK ATTACK (Player 3) - FUTURE IMPLEMENTATION ---
        elif self.player.char_type == 'tank':
            # TODO: Add logic for the tank's attack here.
            # Example: GroundSlam(self, self.player.rect.center)
            print("Tank attack is not implemented yet.")

    def update(self):

        shop_active = any(isinstance(npc, Seller2NPC) and npc.shop_active for npc in self.npcs)
        
        # Atualiza todos os sprites, exceto o player se a loja estiver ativa
        for sprite in self.all_sprites:
            if not (shop_active and isinstance(sprite, Player)):
                sprite.update()
        # Atualizações do game loop
        self.all_sprites.update()
    # Verifica inimigos e spawna portal se necessário
        self.check_enemies_and_spawn_portal()

        # Verifica se o boss foi derrotado
        for boss in self.bosses:
            if boss.life <= 0:
                print("Nero derrotado!")
                boss.kill() # Remove o boss do jogo
                self.playing = False # Termina o jogo ou transiciona para a tela de vitória
                self.win_screen() # Chama a tela de vitória
    
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
        for bats in self.bats: # Corrigido para bats
            bats.draw_health_bar(self.screen)
        
        # Desenha a barra de vida do boss se ele existir
        for boss in self.bosses:
            boss.draw_health_bar()

        for npc in self.npcs:
            if isinstance(npc, Seller2NPC):
                npc.draw_shop(self.screen)
        
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
            self.clock.tick(FPS)

    def game_over(self):
        text = self.font.render('Game Over, TENTE NOVAMENTE!', True, WHITE)
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
    
    def win_screen(self): # Nova tela de vitória
        text = self.font.render('VOCÊ VENCEU!', True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        restart_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'Reiniciar', 32)
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

            self.screen.blit(self.intro_background, (0, 0)) # Pode ser uma imagem de vitória diferente
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True
        
        tittle = self.font.render('GameAdventure', True, BLACK)
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
                try:
                    pygame.mixer.music.load(MUSIC_LEVELS[1])
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.15)
                    print("Música do menu carregada com sucesso")
                except Exception as e:
                    print(f"Erro ao carregar música do menu: {e}")
                intro = False
            
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(tittle, tittle_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def check_enemies_and_spawn_portal(self):
        # Apenas cria portal se não for o nível do boss e não houver inimigos (e morcegos)
        if len(self.enemies) == 0 and len(self.bats) == 0 and not any(isinstance(boss, Nero) for boss in self.bosses):
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
g.character_selection_screen()  # Mostra a seleção primeiro
g.new()  # Inicia o jogo com o personagem selecionado

while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
