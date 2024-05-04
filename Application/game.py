import pygame
import pygame.transform
import pytmx
import pyscroll
from player import Player
from settings import *

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

        # Détection des collisions avec les objets de type "colliDeco" sur la carte
        self.collision = []
        for obj in tmx_data.objects:
            if obj.type == "colliDeco":
                self.collision.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    def update(self):
        # Mise à jour du groupe de calques
        self.group.update()

        # Vérification des collisions entre le joueur et les objets de collision
        for collision_rect in self.collision:
            if self.player.rect.colliderect(collision_rect):
                self.player.move_back()

    def handle_input(self):
        # Gestion des entrées du joueur (mouvement et tir)
        pressed = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()

        # Gestion du mouvement du joueur
        if pressed[pygame.K_z]:
            self.player.move(0, -PLAYER_SPEED)
        if pressed[pygame.K_s]:
            self.player.move(0, PLAYER_SPEED)
        if pressed[pygame.K_q]:
            self.player.move(-PLAYER_SPEED, 0)
        if pressed[pygame.K_d]:
            self.player.move(PLAYER_SPEED, 0)
                
        # Gestion du tir du joueur (avec le bouton gauche de la souris)
        if mouse_pressed[0]:  # Bouton gauche de la souris
            if self.player.shoot(pygame.mouse.get_pos()):
                # Si le tir est réussi, réinitialiser le délai de tir
                self.player.shoot_cooldown = SHOOT_COOLDOWN

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            # Enregistrement de la position précédente du joueur
            self.player.save_location()
            
            # Gestion des entrées du joueur et des événements de jeu
            self.handle_input()
            
            # Réduction du délai de tir du joueur
            self.player.cooldown_tick()
            
            # Affichage des sprites et de la carte
            self.group.draw(self.screen)
            
            # Mise à jour des sprites et de la carte
            self.update()
            
            # Centrage de la caméra sur le joueur
            self.group.center(self.player.rect.center)
            
            # Mise à jour de l'affichage de l'écran
            pygame.display.flip()

            # Gestion des événements du jeu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(FPS)

        # Fermeture de la fenêtre pygame
        pygame.quit()
