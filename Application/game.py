import pygame
import pytmx
import pyscroll
import random
from entity import *
from settings import *
from interface import *
from inventory import *
from item import *
from save_system import SaveSystem
from quest import *
from bullet import *


class Game:
    def __init__(self):
        # Initialisation de la fenêtre de jeu
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.SRCALPHA)
        pygame.display.set_caption(TITRE)  # Définir le titre de la fenêtre

        # Création du joueur et ajout au groupe de calques
        self.player = Player(0,0)

        self.quest1active = False #Pour le compteur de monstres tues

        self.golem_killed = False

        self.frame_count = 0

        self.bullet_types = [Bullet, SuperBullet]

        # Initialisation de la liste des items
        self.list_items_on_map = [apple, military, police, peluche]

        self.list_items_on_monster = [tooth]

        self.item_rects = []

        self.current_bullet = Bullet

        # Appel de la méthode switch_map pour charger la première carte
        self.switch_map("map1.tmx", "spawn_player")

        self.boss_bullets = pygame.sprite.Group() # Groupe pour les balles tirées par le joueur
        self.all_bullets = pygame.sprite.Group() # Groupe pour les balles tirées par les ennemis

        #Font pour le texte: 
        self.font = pygame.font.Font('freesansbold.ttf', 36)
        self.intro_background = pygame.image.load("Application/images/background.png")
        self.running = True # Variable GLOBALE pour contrôler l'exécution du jeu
        self.new_game = False #Variable globale pour savoir si c'est un nouveau jeu 
        self.prologue_on = False

        #création de l'inventaire 
        self.inventory = Inventory()

        self.questmanager = QuestManager()
         #premiere quete
        self.main_quest = Quest("Quête principale", "Vaincre le boss", 1,self.questmanager)

        # deuxieme quete
        self.secondary_quest1 = Quest("Quête secondaire_1", "Tuer 10 ennemis", 10,self.questmanager)
        #troisieme quete
        self.secondary_quest2 = Quest("Quête secondaire_2", "Obtenir 5 dents", 5,self.questmanager)
        #quatrieme quete
        self.secondary_quest3 = Quest("Quete secondaire_3","Obtenir 5 coeurs",5,self.questmanager)
        #cinquieme quete
        self.secondary_quest4 = Quest("Quête secondaire_4", "Récuperer un item caché", 1, self.questmanager)

        # Ajoute les quêtes dans le gestionnaire de quetes
        self.questmanager.add_quest(self.main_quest)
        
        self.show_inventory = True
        self.interface = Interface(self.player,self.prologue_on,self.new_game)
        self.npc = None
        self.in_dialogue = False

        #initialise l'affichage des quetes sur fermé
        self.show_quests = False
        self.save_load = SaveSystem('.json','Application/save_data/')
        self.quest_background = pygame.image.load("Application/images/quest_background.png")
        self.quest_1_dialogue = DialogueBox(NPC_DIALOGUE_10_MONSTER_QUEST, 22, 700, 150, 50, HEIGHT - 250, (255, 255, 128, 128), (0, 0, 0))


    def give_reward_quests(self):
        if self.main_quest.completed and not self.main_quest.reward_given:
            self.inventory.add_item(apple)
            self.main_quest.reward_given = True

        if self.secondary_quest1.completed and not self.secondary_quest1.reward_given:
            self.inventory.add_item(apple)
            self.secondary_quest1.reward_given = True

        if self.secondary_quest2.completed and not self.secondary_quest2.reward_given:
            self.inventory.add_item(apple)
            self.secondary_quest2.reward_given = True

        if self.secondary_quest3.completed and not self.secondary_quest3.reward_given:
            self.inventory.add_item(apple)
            self.secondary_quest3.reward_given = True

        if self.secondary_quest4.completed and not self.secondary_quest4.reward_given:
            self.inventory.add_item(apple)
            self.secondary_quest4.reward_given = True

    def switch_map(self, map_name, spawn_name = None):
        self.all_enemies = []  # Réinitialiser la liste des ennemis

        # Chargement des données de la carte à partir d'un fichier TMX
        tmx_data = pytmx.util_pygame.load_pygame(f"Application/{map_name}")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        self.map = map_name
        # Création d'un rendu de carte avec mise en mémoire tampon pour des performances optimales
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = ZOOM  # Zoom sur la carte
        # Recréer le groupe de calques avec le nouveau rendu de carte
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=2)

        # Recherche de l'objet spawn_map dans les données de la carte
        spawn_map = tmx_data.get_object_by_name(spawn_name)
        self.group.add(self.player)

        # Positionnement du joueur aux coordonnées de l'objet spawn_map
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
            if obj.type == "spawn_nohead":
                self.all_enemies.append(Nohead(obj.x, obj.y))
                self.group.add(self.all_enemies)
            if obj.type == "spawn_golem" and not self.golem_killed:
                self.all_enemies.append(Golem(obj.x, obj.y))
                self.group.add(self.all_enemies)
            if obj.type == 'spawn_npc':
                self.npc = Npc(obj.x, obj.y)
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
                    enemy.take_damage(self.player.damage)
                    if enemy.health <= 0:
                        if type(enemy) == Golem: # Si le type(class) de enemy est Golem, ..
                            self.golem_killed = True  # Le Golem a été tué
                            self.main_quest.updateProgress()
                            self.interface.ending_screen()
                            self.running = self.interface.ending_screen() #pour pouvoir quitter le jeu

                        self.all_enemies.remove(enemy) # Supprimer l'ennemi du groupe (rect)
                        self.drop_item(enemy) # Laisser tomber un objet
                        if self.quest1active == True:
                            self.secondary_quest1.updateProgress() #Met à jour la quête secondaire 
         
        for enemy in self.all_enemies:
            if enemy.rect.colliderect(self.player.rect):
                enemy.attack(self.player, enemy.damage)
            if type(enemy) == Golem:
                enemy.rage()
                self.frame_count += 1
                for bullet in self.boss_bullets:
                    if bullet.rect.colliderect(self.player.rect):
                        self.player.take_damage(enemy.damage)
                        self.boss_bullets.remove(bullet)

                if self.frame_count >= GOLEM_SHOOT_COOLDOWN:
                    enemy.shoot_all_directions(self.boss_bullets)
                    self.frame_count = 0
            
        # Mise à jour des balles tirées par le joueur
        for bullet in self.all_bullets:
            bullet.update()
            if bullet.lifetime <= 0:
                self.all_bullets.remove(bullet)
            else:
                bullet.lifetime -= 1

        for bullet in self.boss_bullets:
            bullet.update()
            if bullet.lifetime <= 0:
                self.boss_bullets.remove(bullet)
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

    def drop_item(self, enemy):
        drop_rate = DROP_RATE  # Taux de drop de 10%
        if random.random() < drop_rate:
            item_type = random.choice(["tooth", "heart"])
            if item_type == "tooth":
                dropped_item = Item(enemy.rect.x, enemy.rect.y, "dent", TOOTH_INFO, TOOTH_SCALE, TOOTH_COLOR)
            elif item_type == "heart":
                dropped_item = Item(enemy.rect.x, enemy.rect.y, "coeur", HEART_INFO, HEART_SCALE, HEART_COLOR)
            self.list_items_on_monster.append(dropped_item)  # Ajouter l'item à la liste des items sur la carte
            self.group.add(dropped_item)  # Ajouter l'item au groupe de sprites pour qu'il soit affiché

    def take_item(self):
        for item in self.list_items_on_map:
            # Vérifier si le joueur est en collision avec un objet
            if pygame.sprite.collide_rect(self.player, item):
                # Effectuer l'action de ramassage de l'objet
                self.inventory.add_item(item)
                if item == peluche:
                    self.secondary_quest4.updateProgress()
                elif item == tooth:
                    self.secondary_quest2.updateProgress()
                elif item == heart:
                    self.secondary_quest3.updateProgress()
                # Supprimer l'item de la liste des items sur la carte pour ne pas qu'il réapparaisse
                self.list_items_on_map.remove(item)
                self.group.remove(item)

        for item in self.list_items_on_monster:
            # Vérifier si le joueur est en collision avec un objet
            if pygame.sprite.collide_rect(self.player, item):
                # Effectuer l'action de ramassage de l'objet
                self.inventory.add_item(item)
                # Supprimer l'objet du groupe de calques
                self.list_items_on_monster.remove(item)
                self.group.remove(item)
                self.secondary_quest2.updateProgress()

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.menu_screen()
                if event.key == pygame.K_i:
                        self.show_inventory = not self.show_inventory
                if  event.key == pygame.K_1:
                    self.player.bullet_type = Bullet 
                if  event.key == pygame.K_2:
                    self.player.bullet_type = SuperBullet
        

                if event.key == pygame.K_o:
                        self.inventory.use_item(apple, self.player)

                if event.key == pygame.K_p:
                        self.inventory.use_item(military, self.player)

                if event.key == pygame.K_t:
                        self.show_quests = not self.show_quests

                if event.key == pygame.K_e:
                        self.take_item()

                if event.key == pygame.K_f and self.npc and self.npc.in_interaction_range(self.player):
                    if not self.in_dialogue:
                        self.in_dialogue = self.npc.interact(self.player,NPC_DIALOGUE_BASIC)
                
                if event.key == pygame.K_RETURN:
                    if self.in_dialogue:
                        if not self.npc.advance_dialogue():
                            self.in_dialogue = False
                            self.npc_interaction_screen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.inventory.handle_click(mouse_pos=pygame.mouse.get_pos())
                       

    def draw_inventory(self):
        if self.show_inventory:
            self.inventory.show_inventory(self.screen, self.font, 800)
    
    def draw_quests(self):
        if self.show_quests:
            self.questmanager.show_quests(self.screen, self.font, WIDTH)
    def load_quests(self, quest_data):
        for quest_info in quest_data:
            quest_name = quest_info['name']
            # Check if the quest is already present in the quest manager
            if not self.questmanager.has_quest(quest_name):
                quest = Quest(quest_info['name'], quest_info['description'], quest_info['goal'], self.questmanager, quest_info['current'])
                quest.completed = quest_info['completed']
                self.questmanager.add_quest(quest)


    def save_game_state(self):
        active_quests = []
        for quest in self.questmanager.quests:
            quest_data = {
                'name': quest.name,
                'description': quest.description,
                'goal': quest.goal,
                'current': quest.current,
                'completed': quest.completed
            }
            active_quests.append(quest_data)

        game_state = {
            'map': self.map,
            'player_position': (self.player.rect.x, self.player.rect.y),
            'inventory': self.inventory.save_inventory(),
            'active_quests': active_quests,
            'quest_1_active': self.quest1active
        }
        self.save_load.save_data(game_state, 'game_state')

    def load_game_state(self):
        game_state = self.save_load.load_data('game_state')
        if game_state:
            self.map = game_state.get('map', 'map1.tmx')
            self.switch_map(self.map)
            self.player.rect.x, self.player.rect.y = game_state.get('player_position', (0, 0))
            self.player.position = [self.player.rect.x, self.player.rect.y]
            self.inventory.load_inventory(game_state.get('inventory', []))
            active_quests_data = game_state.get('active_quests', [])
            self.quest1active = game_state.get('quest_1_active',False)
            for quest_info in active_quests_data:
                quest_name = quest_info['name']
                quest_description = quest_info['description']
                quest_goal = quest_info['goal']
                quest_current = quest_info['current']
                quest_completed = quest_info['completed']
                if quest_name == "Quête secondaire_1":
                    self.secondary_quest1 = Quest(quest_name, quest_description, quest_goal, self.questmanager, quest_current)
                    self.secondary_quest1.completed = quest_completed
                    self.questmanager.add_quest(self.secondary_quest1)
                elif quest_name == "Quête secondaire_2":
                    self.secondary_quest2 = Quest(quest_name, quest_description, quest_goal, self.questmanager, quest_current)
                    self.secondary_quest2.completed = quest_completed
                    self.questmanager.add_quest(self.secondary_quest2)
                elif quest_name == "Quête secondaire_3":
                    self.secondary_quest3 = Quest(quest_name, quest_description, quest_goal, self.questmanager, quest_current)
                    self.secondary_quest3.completed = quest_completed
                    self.questmanager.add_quest(self.secondary_quest3)
                elif quest_name == "Quête secondaire_4":
                    self.secondary_quest4 = Quest(quest_name, quest_description, quest_goal, self.questmanager, quest_current)
                    self.secondary_quest4.completed = quest_completed
                    self.questmanager.add_quest(self.secondary_quest4)
            

    def run(self):
        clock = pygame.time.Clock()
        # Affichage de l'écran d'introduction
        self.intro_screen()
        
        if self.new_game: 
            self.reset_game_state()
            self.interface.prologue() 
        while self.running:
            self.update()
            self.player.save_location()
            # Gestion des entrées du joueur et des événements de jeu
            self.handle_input()
            
            # Réduction du délai de tir du joueur
            self.player.cooldown_tick()
            
            # Mise à jour des sprites et de la carte
            
            
            # Affichage des sprites et de la carte
            self.group.draw(self.screen)

            # Affichage des balles tirées par le joueur
            self.all_bullets.draw(self.screen)
            self.boss_bullets.draw(self.screen)
            # Centrage de la caméra sur le joueur
            self.group.center(self.player.rect.center)

            # Affichage des rectangles de collision des sprites
            pygame.draw.rect(self.screen, (255, 0, 0), self.player.rect, 2)
            for enemy in self.all_enemies:
                pygame.draw.rect(self.screen, (0, 255, 0), enemy.rect, 2)
            
            #affichage de la barre de vie
            self.player.update_healthbar(self.screen)
            if self.player.health <= 0:
                self.death_screen()
                
                        
            #affichage de l'inventaire (i)
            self.draw_inventory()

            #affichage des quetes (t)
            self.draw_quests()
            #donne les récompenses quand les quetes sont complétées
            self.give_reward_quests()
            #affichage de la dialogue box
            self.draw_dialogue_box()

            
            # Gestion des événements du jeu
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu_screen() 
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        pass
  
                if event.type == pygame.QUIT:
                    self.running = False
                
            # Mise à jour de l'affichage de l'écran
            pygame.display.flip()
            clock.tick(FPS)
        
        # Fermeture de la fenêtre pygame
        pygame.quit()


    def intro_screen(self):
            intro = True
            self.reset_game_state()
            self.death = False
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
                    self.load_game_state()
                if play_button.is_pressed(mouse_pos, mouse_pressed):
                    intro = False
                    self.new_game = True
                    self.prologue_on = True
                    return self.new_game, self.prologue_on

                if exit_button.is_pressed(mouse_pos, mouse_pressed):
                    intro = False
                    self.running = False
                
                stretched_image = pygame.transform.scale(self.intro_background,(800,1000))
                self.screen.blit(stretched_image, (0, 0))
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
                if save_game.is_pressed(mouse_pos, mouse_pressed):
                    self.save_game_state()
                    print("Game saved.")
                if exit_button.is_pressed(mouse_pos, mouse_pressed):
                    menu = False
                    self.running = False
                    return self.running
                
                stretched_image = pygame.transform.scale(self.intro_background,(800,1000))
                self.screen.blit(stretched_image, (0, 0))
                self.screen.blit(title, title_rect)
                self.screen.blit(continue_button.image, continue_button.rect)
                self.screen.blit(save_game.image, save_game.rect)
                self.screen.blit(exit_button.image, exit_button.rect)
                
                pygame.display.update()
    def death_screen(self):
        self.death = True
        title = self.font.render("You died", True, 'Black')
        title_rect = title.get_rect(center=(WIDTH/2, HEIGHT/4))
        return_main_menu = Button(WIDTH/2 - 100, HEIGHT/2 - 150, 200, 50, (255, 255, 255), (0, 0, 0), "Main Menu", 36)
        exit_button = Button(WIDTH/2 - 100, HEIGHT/2 + 50, 200, 50, (255, 255, 255), (0, 0, 0), "Exit", 36)
        while self.death:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.death = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if return_main_menu.is_pressed(mouse_pos, mouse_pressed):
                self.death = False
                self.reset_game_state()
                self.intro_screen()
                return
            if exit_button.is_pressed(mouse_pos, mouse_pressed):
                self.death = False
                self.running = False
            
            stretched_image = pygame.transform.scale(self.intro_background,(800,1000))
            self.screen.blit(stretched_image, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(return_main_menu.image, return_main_menu.rect)
            self.screen.blit(exit_button.image, exit_button.rect)
            
            pygame.display.update()
    def reset_game_state(self):
        self.player = Player(0,0)
        self.inventory = Inventory()
        self.show_inventory = False
        self.show_quests = False
        self.npc = None
        self.map = 'map1.tmx'
        self.switch_map(self.map,'spawn_player')
    
    def npc_interaction_screen(self):
        self.npc_interaction = True
        title = self.font.render("Voici quelques quêtes pour toi.", True, 'White')
        title_rect = title.get_rect(center=(WIDTH/2, HEIGHT/6))
        quest_1 = Button(WIDTH/2 - 200, HEIGHT/2 - 150, 300, 50, (0, 0, 0,128), (255, 255, 128,64), "Tuer 10 ennemis!", 24)
        quest_2 = Button(WIDTH/2 - 200, HEIGHT/2 - 50, 300, 50, (0, 0, 0,128), (255, 255, 128,64), "Trouver 5 dents", 24)
        quest_3 = Button(WIDTH/2 - 200, HEIGHT/2 + 50, 300, 50, (0,0,0,128), (255, 255, 128,64), "Trouver 5 coeurs", 24)
        quest_4 = Button(WIDTH/2 - 200, HEIGHT/2 + 50, 300, 50, (0,0,0,128), (255, 255, 128,64), "Trouver 5 dents", 24)
        exit_button = Button(WIDTH/2 - 200, HEIGHT/2 + 150, 300, 50, (0,0,0,128), (255, 255, 128,64), "continuer l'aventure", 24)
        while self.npc_interaction:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.npc_interaction = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if quest_1.is_pressed(mouse_pos, mouse_pressed):
                self.npc_interaction = False
                self.npc.interact(self.player,NPC_DIALOGUE_10_MONSTER_QUEST)
                self.in_dialogue = True
                self.questmanager.add_quest(self.secondary_quest1)
                self.quest1active = True
            
            if quest_2.is_pressed(mouse_pos, mouse_pressed):
                self.npc.interact(self.player,NPC_DIALOGUE_HEART_MISSION)
                self.in_dialogue = True
                self.questmanager.add_quest(self.secondary_quest2)
                return
            
            if quest_3.is_pressed(mouse_pos, mouse_pressed):
                self.npc.interact(self.player,NPC_DIALOGUE_HIDDEN_OBJECT)
                self.in_dialogue = True
                self.questmanager.add_quest(self.secondary_quest3)
                return
            
            if quest_4.is_pressed(mouse_pos, mouse_pressed):
                self.npc.interact(self.player,NPC_DIALOGUE_HIDDEN_OBJECT)
                self.in_dialogue = True
                self.questmanager.add_quest(self.secondary_quest3)
                return
            
            if exit_button.is_pressed(mouse_pos, mouse_pressed):
                return
            
            stretched_image = pygame.transform.scale(self.quest_background,(800,800))
            self.screen.blit(stretched_image, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(quest_1.image, quest_1.rect)
            self.screen.blit(quest_2.image,quest_2.rect)
            self.screen.blit(quest_3.image, quest_3.rect)
            self.screen.blit(exit_button.image,exit_button.rect)
            
            pygame.display.update()