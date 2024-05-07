import pygame
import math
from settings import *
from bullet import Bullet
from game import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites):
        super().__init__()
        
        # Création de l'image du joueur (un carré rouge)
        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 0, 0))
        self.image.set_colorkey((0, 0, 0))  # Rendre le fond transparent
        self.rect = self.image.get_rect()
        
        # Position initiale du joueur
        self.position = [x, y]
        self.old_position = self.position.copy()  # Pour sauvegarder la position précédente
        self.speed = PLAYER_SPEED  # Vitesse de déplacement du joueur
        
        # Délai de rechargement entre chaque tir
        self.shoot_cooldown = 0
        
        # Groupe de tous les sprites, nécessaire pour ajouter des balles
        self.all_sprites = all_sprites

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

    def update(self):
        """Mettre à jour la position du joueur."""
        self.rect.topleft = self.position

    def shoot(self, target_pos):
        """Tirer une balle vers la position cible."""
        if self.shoot_cooldown <= 0:
            # Création d'une balle et ajout au groupe de tous les sprites
            bullet = Bullet(self.rect.center, target_pos)
            self.all_sprites.add(bullet)
            # Réinitialisation du délai de rechargement
            self.shoot_cooldown = SHOOT_COOLDOWN
            return True  # Indiquer que le tir a été effectué avec succès
        return False  # Indiquer que le tir n'a pas été effectué

    def cooldown_tick(self):
        """Réduire le délai de rechargement."""
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
