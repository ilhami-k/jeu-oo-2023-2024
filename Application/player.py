import pygame
import math
from settings import *
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites):
        super().__init__()
        
        # Position initiale du joueur
        self.position = [x, y]
        # Création de la feuille de sprites du joueur
        self.sprite_sheet = pygame.image.load("Application/Player.png")
        # Création des images pour les différentes directions du joueur
        self.image = self.get_image(48, 0)
        self.image.set_colorkey((0, 0, 0))  # Définir la couleur de transparence
        self.rect = self.image.get_rect()

        self.old_position = self.position.copy()  # Pour sauvegarder la position précédente
        self.speed = PLAYER_SPEED  # Vitesse de déplacement du joueur
        
        # Délai de rechargement entre chaque tir
        self.shoot_cooldown = 0

    # Création de la méthode get_image pour obtenir une image à partir de la feuille de sprites
    def get_image(self, x, y):
        image = pygame.Surface((16, 32))
        image.blit(self.sprite_sheet, (0, 0), (x, y, 16, 32))
        return image

    def save_location(self):
        """Sauvegarde la position actuelle du joueur."""
        self.old_position = self.position.copy()

    def move_back(self):
        """Revenir à la position précédente en cas de collision."""
        self.position = self.old_position.copy()
        self.rect.topleft = self.position

    def move(self, x, y):
        """Déplacer le joueur."""
        # Si le joueur se déplace en diagonale, ajuster la vitesse
        if x != 0 and y != 0:
            x *= math.sqrt(2) / 2
            y *= math.sqrt(2) / 2

        self.position[0] += x
        self.position[1] += y

        # Mettre à jour les coordonnées du carré rouge
        self.rect.x = int(self.position[0])
        self.rect.y = int(self.position[1]) 
    
    def update(self):
        """Mettre à jour la position du joueur."""
        self.rect.topleft = self.position

    def shoot(self, target_x, target_y, bullet_group):
        """Tirer une balle vers la position cible."""
        # ATTENTION LES TIRS PARTENT DU CENTRE DE LA FENETRE ET PAS DU JOUEUR (Debogage sur le centre du player à faire si possible par la suite)
        window_center_x = WIDTH // 2
        window_center_y = HEIGHT // 2
        angle = math.atan2(target_y - window_center_y, target_x - window_center_x)
        # Utilise les coordonnées du centre de la fenêtre de jeu comme position initiale pour les balles
        bullet_group.add(Bullet(window_center_x, window_center_y, angle))

    def cooldown_tick(self):
        """Réduire le délai de rechargement."""
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def get_center(self):
        return self.x + self.width / 2, self.y + self.height / 2