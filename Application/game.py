import pygame
import pygame.transform
import pytmx
import pyscroll
from player import Player
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # Initialisation de la fenêtre de jeu
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Projet OO")  # Définir le titre de la fenêtre

        # Chargement des données de la carte à partir d'un fichier TMX
        tmx_data = pytmx.util_pygame.load_pygame("Application/map.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)

        # Création d'un rendu de carte avec mise en mémoire tampon pour des performances optimales
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 2  # Zoom sur la carte

        # Création d'un groupe de calques pour les sprites
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)

        # Création du joueur et ajout au groupe de calques
        player_spawn = tmx_data.get_object_by_name("spawn_player")
        self.player = Player(player_spawn.x, player_spawn.y, self.group)  # Passer la référence au groupe ici
        self.group.add(self.player)

        self.all_bullets = pygame.sprite.Group() # Groupe pour les balles tirées par le joueur

        # Détection des collisions avec les objets de type "colliDeco" sur la carte
        self.collision = []
        for obj in tmx_data.objects:
            if obj.type == "colliDeco":
                self.collision.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        #Font pour le texte: 
        self.font = pygame.font.Font('freesansbold.ttf', 36)
        self.intro_background = pygame.image.load("Application/background.png")
        self.running = True # Variable GLOBALE pour contrôler l'exécution du jeu

    def update(self):
        # Mise à jour du groupe de calques
        self.group.update()

        # Vérification des collisions entre le joueur et les objets de collision
        for collision_rect in self.collision:
            if self.player.rect.colliderect(collision_rect):
                self.player.move_back()

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
        title_rect = title.get_rect(center=(WIDTH/2, HEIGHT/2))
        play_button = Button(WIDTH/2 - 50, HEIGHT/2 - 250, 100, 50, (255, 255, 255), (0, 0, 0), "Play", 36)
        exit_button = Button(WIDTH/2 - 50, HEIGHT/2 - 50, 100, 50, (255, 255, 255), (0, 0, 0), "Exit", 36)
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            if exit_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
                self.running = False
            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(exit_button.image, exit_button.rect)
            
            
            pygame.display.update()
    def run(self):
        clock = pygame.time.Clock()
        
        # Affichage de l'écran d'introduction
        self.intro_screen()

        while self.running:
            # Enregistrement de la position précédente du joueur
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
    
            # Mise à jour de l'affichage de l'écran
            pygame.display.flip()

            # Mise à jour des balles tirées par le joueur
            for bullet in self.all_bullets:
                bullet.update()
                if bullet.lifetime <= 0:
                    self.all_bullets.remove(bullet)
                else:
                    bullet.lifetime -= 1

            # Gestion des événements du jeu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            clock.tick(FPS)

        # Fermeture de la fenêtre pygame
        pygame.quit()