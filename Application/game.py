import pygame
import pytmx
import pyscroll
import json
from entity import *
from settings import *
from interface import *
from inventory import *
from item import *
from save_system import SaveSystem



class Game:
    def __init__(self):
        # Initialisation de la fenêtre de jeu
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITRE)  # Définir le titre de la fenêtre

        # Création du joueur et ajout au groupe de calques
        self.player = Player(0,0)


        # Initialisation de la liste des items
        self.list_items_on_map = [appel, berry, military, police, uzi, bazooka, pistol]


        self.all_enemies = []  # Liste pour les ennemis

        self.item_rects = []

        # Appel de la méthode switch_map pour charger la première carte
        self.switch_map("map1.tmx", "spawn_player")

        self.all_bullets = pygame.sprite.Group() # Groupe pour les balles tirées par le joueur

        #Font pour le texte: 
        self.font = pygame.font.Font('freesansbold.ttf', 36)
        self.intro_background = pygame.image.load("Application/background.png")
        self.running = True # Variable GLOBALE pour contrôler l'exécution du jeu
        self.new_game = False #Variable globale pour savoir si c'est un nouveau jeu 
        self.prologue_on = False

        #création de l'inventaire 
        self.inventory = Inventory()
        

        #initialise l'inventaire sur fermé
        self.show_inventory = True
        self.interface = Interface(self.player,self.running,self.prologue_on,self.new_game)
        self.npc = None


    def switch_map(self, map_name, spawn_name):
        self.all_enemies = []  # Réinitialiser la liste des ennemis
        try:
            self.group.empty()  # Supprimer tous les sprites du groupe
        except:
            pass
        # Chargement des données de la carte à partir d'un fichier TMX
        tmx_data = pytmx.util_pygame.load_pygame(f"Application/{map_name}")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        self.map = map_name
        # Création d'un rendu de carte avec mise en mémoire tampon pour des performances optimales
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = ZOOM  # Zoom sur la carte
        # Recréer le groupe de calques avec le nouveau rendu de carte
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=2)

        # Recherche de l'objet spawn_map2 dans les données de la carte
        spawn_map = tmx_data.get_object_by_name(spawn_name)
        self.group.add(self.player)

        # Positionnement du joueur aux coordonnées de l'objet spawn_map2
        self.player.position = [spawn_map.x, spawn_map.y]
        self.player.rect.topleft = self.player.position

        # Création des ennemis
        for obj in tmx_data.objects:
            # Création des Zombies à partir des objets spawn_zombie sur la carte
            if obj.type == "spawn_zombie":
                self.all_enemies.append(Zombie(obj.x, obj.y))  # Passer la référence au groupe ici
                self.group.add(self.all_enemies)
            # Création des Skeletons à partir des objets spawn_skeleton sur la carte
            if obj.type == "spawn_skeleton":
                self.all_enemies.append(Skeleton(obj.x, obj.y))  # Passer la référence au groupe ici
                self.group.add(self.all_enemies)
            if obj.type == 'spawn_npc':
                self.npc = Npc(obj.x, obj.y,'test')
                self.group.add(self.npc)
            # Si l'objet est un item
            if obj.type == "item":
                # Parcourir les objets de la liste
                for item in self.list_items_on_map:
                    # Si le nom de l'objet de la liste correspond au nom de l'objet du fichier TMX
                    if item.nom == obj.name:
                        # Positionner l'objet sur la carte
                        item.rect.x = obj.x
                        item.rect.y = obj.y
                        self.group.add(item)

        # Détection des collisions avec les objets de type "colliDeco" sur la carte
        self.collision = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.collision.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                
        # Définir le rectangle de collision pour entrer sur les differentes map
        enter_other_map1 = tmx_data.get_object_by_name("enter_other_map1")
        self.enter_other_map1_rect = pygame.Rect(enter_other_map1.x, enter_other_map1.y, enter_other_map1.width, enter_other_map1.height)
        enter_other_map2 = tmx_data.get_object_by_name("enter_other_map2")
        self.enter_other_map2_rect = pygame.Rect(enter_other_map2.x, enter_other_map2.y, enter_other_map2.width, enter_other_map2.height)
        if map_name == 'map3.tmx':
            enter_map_boss = tmx_data.get_object_by_name("enter_map_boss")
            self.enter_map_boss_rect = pygame.Rect(enter_map_boss.x, enter_map_boss.y, enter_map_boss.width, enter_map_boss.height)

    def update(self): 
        # Mise à jour du groupe de calques
        self.group.update(self.player)

        # Vérification des collisions entre le joueur et les objets de collision
        for collision_rect in self.collision:
            if self.player.rect.colliderect(collision_rect):
                self.player.move_back()
        # BUG Vérification des collisions entre l'ennemi et les objets de collision
        # for enemy in self.all_enemies:
        #     for collision_rect in self.collision:
        #         if enemy.rect.colliderect(collision_rect):
        #             enemy.move_back()

        # Vérification des collisions entre les balles et l'ennemi
        for bullet in self.all_bullets:
            for enemy in self.all_enemies:
                if bullet.rect.colliderect(enemy.rect):
                    self.all_bullets.remove(bullet)
                    enemy.take_damage()
                    if enemy.health <= 0:
                        self.all_enemies.remove(enemy) # Supprimer l'ennemi du groupe (rect)

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
            elif self.player.rect.colliderect(self.enter_map_boss_rect):
                self.switch_map("mapBoss.tmx", "spawn_map_boss")
        elif self.map == 'map4.tmx':
            if self.player.rect.colliderect(self.enter_other_map1_rect):
                self.switch_map("map2.tmx", "spawn_map2_2")
            elif self.player.rect.colliderect(self.enter_other_map2_rect):
                self.switch_map("map3.tmx", "spawn_map3_2")
        elif self.map == 'mapBoss.tmx':
            if self.player.rect.colliderect(self.enter_other_map1_rect):
                self.switch_map('map3.tmx',"spawn_map3_3")
        if self.npc:
            self.npc.update(self.player)

    def take_item(self):
        for item in self.list_items_on_map:
            # Vérifier si le joueur est en collision avec un objet
            if pygame.sprite.collide_rect(self.player, item):
                # Effectuer l'action de ramassage de l'objet
                self.inventory.add_item(item)
                # Supprimer l'item de la liste des items sur la carte pour ne pas qu'il réapparaisse
                self.list_items_on_map.remove(item)
                # Supprimer l'objet du groupe de calques
                self.group.remove(item)
    
    def draw_dialogue_box(self):
        if self.npc and self.npc.dialogue_box:
            self.npc.dialogue_box.draw(self.screen)

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
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_pressed[0]:  # Si le bouton gauche de la souris est enfoncé
            if self.player.attack_cooldown == 0:
                self.player.shoot(mouse_x, mouse_y, self.all_bullets)
                self.player.attack_cooldown = ATTACK_COOLDOWN
                
        # Gestion de l'affichage de l'inventaire avec une seule touche
        if pressed[pygame.K_i]:
            self.show_inventory = not self.show_inventory

        # Gestion de la prise d'objet
        if pressed[pygame.K_e]:
            self.take_item()
        if pressed[pygame.K_f] and self.npc and self.npc.in_interaction_range(self.player):
            self.npc.interact(self.player)
        
    def draw_inventory(self):
        if self.show_inventory:
            self.inventory.show_inventory(self.screen, self.font, 800)
            

    def run(self):
        clock = pygame.time.Clock()
        # Affichage de l'écran d'introduction
        self.interface.intro_screen()
        self.running = self.interface.intro_screen() #pour pouvoir quitter le jeu lors de l'ecran du menu
        self.new_game = self.interface.intro_screen()
        if self.new_game: 
            self.interface.prologue() 
        
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
            for enemy in self.all_enemies:
                pygame.draw.rect(self.screen, (0, 255, 0), enemy.rect, 2)
            
            #affichage de la barre de vie
            self.player.update_healthbar(self.screen)
                        
            #affichage de l'inventaire (i)
            self.draw_inventory()

            #affichage de la dialogue box
            self.draw_dialogue_box()

            
            # Gestion des événements du jeu
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.interface.menu_screen() 
                        self.running = self.interface.menu_screen()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    self.inventory.handle_click(mouse_pos)
                elif event.type == pygame.QUIT:
                    self.running = False
                    
            # Mise à jour de l'affichage de l'écran
            pygame.display.flip()
            clock.tick(FPS)
        
        # Fermeture de la fenêtre pygame
        pygame.quit()
