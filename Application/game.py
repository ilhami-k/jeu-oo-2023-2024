import pygame
import pygame.transform
import pytmx
import pyscroll
import json
from player import *
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # Initialisation de la fenêtre de jeu
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITRE)  # Définir le titre de la fenêtre

        # Chargement des données de la carte à partir d'un fichier TMX
        tmx_data = pytmx.util_pygame.load_pygame("Application/map1.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        self.map = 'map1.tmx'

        # Création d'un rendu de carte avec mise en mémoire tampon pour des performances optimales
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = ZOOM  # Zoom sur la carte

        # Création d'un groupe de calques pour les sprites
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=2)

        # Création du joueur et ajout au groupe de calques
        player_spawn = tmx_data.get_object_by_name("spawn_player")
        self.player = Player(player_spawn.x, player_spawn.y, self.group)  # Passer la référence au groupe ici
        self.group.add(self.player)

        # # Création de l'ennemi1 et ajout au groupe de calques
        enemy1_spawn = tmx_data.get_object_by_name("spawn_enemy1")
        self.enemy1 = Enemy(enemy1_spawn.x, enemy1_spawn.y, self.group)  # Passer la référence au groupe ici
        self.group.add(self.enemy1)

        self.all_bullets = pygame.sprite.Group() # Groupe pour les balles tirées par le joueur

        # Détection des collisions avec les objets de type "colliDeco" sur la carte
        self.collision = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.collision.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        #Font pour le texte: 
        self.font = pygame.font.Font('freesansbold.ttf', 36)
        self.intro_background = pygame.image.load("Application/background.png")
        self.running = True # Variable GLOBALE pour contrôler l'exécution du jeu

        # Définir le rectangle de collision pour entrer sur map2
        enter_other_map1 = tmx_data.get_object_by_name("enter_other_map1")
        self.enter_other_map1_rect = pygame.Rect(enter_other_map1.x, enter_other_map1.y, enter_other_map1.width, enter_other_map1.height)
        enter_other_map2 = tmx_data.get_object_by_name("enter_other_map2")
        self.enter_other_map2_rect = pygame.Rect(enter_other_map2.x, enter_other_map2.y, enter_other_map2.width, enter_other_map2.height)

    def switch_map(self, map_name, spawn_name):
        # Chargement des données de la carte à partir d'un fichier TMX
        tmx_data = pytmx.util_pygame.load_pygame(f"Application/{map_name}")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        self.map = map_name
        # Création d'un rendu de carte avec mise en mémoire tampon pour des performances optimales
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = ZOOM  # Zoom sur la carte
        # Recréer le groupe de calques avec le nouveau rendu de carte
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=2)
        self.group.add(self.player)

        # Recherche de l'objet spawn_map2 dans les données de la carte
        spawn_map = tmx_data.get_object_by_name(spawn_name)
        # Positionnement du joueur aux coordonnées de l'objet spawn_map2
        self.player.position = [spawn_map.x, spawn_map.y]
        self.player.rect.topleft = self.player.position

        # Détection des collisions avec les objets de type "colliDeco" sur la carte
        self.collision = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.collision.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                
        # Définir le rectangle de collision pour entrer sur map2
        enter_other_map1 = tmx_data.get_object_by_name("enter_other_map1")
        self.enter_other_map1_rect = pygame.Rect(enter_other_map1.x, enter_other_map1.y, enter_other_map1.width, enter_other_map1.height)
        enter_other_map2 = tmx_data.get_object_by_name("enter_other_map2")
        self.enter_other_map2_rect = pygame.Rect(enter_other_map2.x, enter_other_map2.y, enter_other_map2.width, enter_other_map2.height)

    def update(self): 
        # Mise à jour du groupe de calques
        self.group.update()

        # Vérification des collisions entre le joueur et les objets de collision
        for collision_rect in self.collision:
            if self.player.rect.colliderect(collision_rect):
                self.player.move_back()
            # Vérification des collisions entre l'ennemi et les objets de collision
            if self.enemy1.rect.colliderect(collision_rect):
                self.enemy1.move_back()

        # Vérification des collisions entre les balles et l'ennemi
        for bullet in self.all_bullets:
            if bullet.rect.colliderect(self.enemy1.rect):
                self.all_bullets.remove(bullet)
                self.enemy1.take_damage()
    
        # Mise à jour des balles tirées par le joueur
        for bullet in self.all_bullets:
            bullet.update()
            if bullet.lifetime <= 0:
                self.all_bullets.remove(bullet)
            else:
                bullet.lifetime -= 1

        # Vérification des transitions entre les cartes
        if self.map == 'map1.tmx':
            if self.player.rect.colliderect(self.enter_other_map1_rect):
                self.switch_map("map2.tmx", "spawn_map2_1")
            elif self.player.rect.colliderect(self.enter_other_map2_rect):
                self.switch_map("map3.tmx", "spawn_map3_1")
        elif self.map == 'map2.tmx':
            if self.player.rect.colliderect(self.enter_other_map1_rect):
                self.switch_map("map1.tmx", "spawn_map1_1")
            elif self.player.rect.colliderect(self.enter_other_map2_rect):
                self.switch_map("map4.tmx", "spawn_map4_1")
        elif self.map == 'map3.tmx':
            if self.player.rect.colliderect(self.enter_other_map1_rect):
                self.switch_map("map1.tmx", "spawn_map1_2")
            elif self.player.rect.colliderect(self.enter_other_map2_rect):
                self.switch_map("map4.tmx", "spawn_map4_2")
        elif self.map == 'map4.tmx':
            if self.player.rect.colliderect(self.enter_other_map1_rect):
                self.switch_map("map2.tmx", "spawn_map2_2")
            elif self.player.rect.colliderect(self.enter_other_map2_rect):
                self.switch_map("map3.tmx", "spawn_map3_2")

    def handle_input(self): 
        pressed = pygame.key.get_pressed() # Gestion des entrées du joueur (mouvement et tir) 
        mouse_pressed = pygame.mouse.get_pressed() # Gestion du tir du joueur (avec le bouton gauche de la souris)

        # Gestion du mouvement du joueur
        if pressed[pygame.K_z]:
            self.player.move(0, -PLAYER_SPEED)
        if pressed[pygame.K_s]:
            self.player.move(0, PLAYER_SPEED)
        if pressed[pygame.K_q]:
            self.player.move(-PLAYER_SPEED, 0)
        if pressed[pygame.K_d]:
            self.player.move(PLAYER_SPEED, 0)

        # Gestion du tir du joueur
        if mouse_pressed[0]:  # Si le bouton gauche de la souris est enfoncé
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.player.shoot_cooldown == 0:
                self.player.shoot(mouse_x, mouse_y, self.all_bullets)
                self.player.shoot_cooldown = SHOOT_COOLDOWN

    def intro_screen(self):
        intro = True
        title = self.font.render("Projet OO", True, 'Black')
        title_rect = title.get_rect(center=(WIDTH/2, HEIGHT/4))
        continue_button = Button(WIDTH/2 - 100, HEIGHT/2 - 150, 200, 50, (255, 255, 255), (0, 0, 0), "Continue", 36)
        play_button = Button(WIDTH/2 - 100, HEIGHT/2 -50 , 200, 50, (255, 255, 255), (0, 0, 0), "New Game", 36)
        exit_button = Button(WIDTH/2 - 100, HEIGHT/2 + 50, 200, 50, (255, 255, 255), (0, 0, 0), "Exit", 36)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if continue_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
                save_load = SaveSystem(".json",'Application/save_data/')
                player_position = save_load.load_data("player_position")
                if player_position:
                    self.player.position = player_position
                    self.player.rect.x, self.player.rect.y = player_position

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            if exit_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
                self.running = False
            
            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(continue_button.image, continue_button.rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(exit_button.image, exit_button.rect)
            
            pygame.display.update()

    def menu_screen(self):
        menu = True
        title = self.font.render("Menu", True, 'Black')
        title_rect = title.get_rect(center=(WIDTH/2, HEIGHT/4))
        continue_button = Button(WIDTH/2 - 100, HEIGHT/2 - 150, 200, 50, (255, 255, 255), (0, 0, 0), "Continue", 36)
        save_game = Button(WIDTH/2 - 100, HEIGHT/2 -50 , 200, 50, (255, 255, 255), (0, 0, 0), "Save game", 36)
        exit_button = Button(WIDTH/2 - 100, HEIGHT/2 + 50, 200, 50, (255, 255, 255), (0, 0, 0), "Exit", 36)

        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if continue_button.is_pressed(mouse_pos, mouse_pressed):
                menu = False
                save_load = SaveSystem(".json",'Application/save_data/')
                player_position = save_load.load_data("player_position")
                if player_position:
                    self.player.position = player_position
                    self.player.rect.x, self.player.rect.y = player_position
            if save_game.is_pressed(mouse_pos, mouse_pressed):
                save_load = SaveSystem(".json",'Application/save_data/')
                save_load.save_data((self.player.rect.x,self.player.rect.y), "player_position")
                print("Game saved")
            if exit_button.is_pressed(mouse_pos, mouse_pressed):
                menu = False
                self.running = False
            
            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(continue_button.image, continue_button.rect)
            self.screen.blit(save_game.image, save_game.rect)
            self.screen.blit(exit_button.image, exit_button.rect)
            
            pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()
        # Affichage de l'écran d'introduction
        self.intro_screen()
        
        while self.running:
            self.player.save_location()
            # Gestion des entrées du joueur et des événements de jeu
            self.handle_input()
            
            # Réduction du délai de tir du joueur
            self.player.cooldown_tick()
            
            # Mise à jour des sprites et de la carte
            self.update()
            
            # Affichage des sprites et de la carte
            self.group.draw(self.screen)

            # Affichage des balles tirées par le joueur
            self.all_bullets.draw(self.screen)
            
            # Centrage de la caméra sur le joueur
            self.group.center(self.player.rect.center)

            # Affichage des rectangles de collision des sprites
            pygame.draw.rect(self.screen, (255, 0, 0), self.player.rect, 2)
            pygame.draw.rect(self.screen, (0, 255, 0), self.enemy1.rect, 2)
    
            # Mise à jour de l'affichage de l'écran
            pygame.display.flip()
            
            # Gestion des événements du jeu
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu_screen() 
                if event.type == pygame.QUIT:
                    self.running = False

            clock.tick(FPS)
        
        # Fermeture de la fenêtre pygame
        pygame.quit()

class SaveSystem:
    def __init__(self, file_extension, save_folder):
        self.file_extension = file_extension
        self.save_folder = save_folder
    
    def save_data(self, data, name):
        data_file_path = self.save_folder + name + self.file_extension
        with open(data_file_path, "w") as data_file:
            json.dump(data, data_file)
    
    def load_data(self, name):
        data_file_path = self.save_folder + name + self.file_extension
        print("Loading data from:", data_file_path)
        try:
            with open(data_file_path, "r") as data_file:
                data = json.load(data_file)
                return data
        except FileNotFoundError or json.decoder.JSONDecodeError:
            print('No save found, Creating a new one.')
            default_data = None
            self.save_data(default_data, name)
            return default_data
