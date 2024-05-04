import pygame
import math
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        super().__init__()
        
        # Création de la surface de la balle
        self.image = pygame.Surface((4, 4))
        self.image.fill((255, 255, 255))  # Couleur blanche
        self.rect = self.image.get_rect()
        self.rect.center = start_pos  # Position de départ de la balle

        # Calcul du vecteur de direction du projectile
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        # Éviter la division par zéro et normaliser le vecteur de direction
        if distance != 0:
            self.dx = dx / distance * BULLET_SPEED
            self.dy = dy / distance * BULLET_SPEED
        else:
            self.dx = 0
            self.dy = 0

    def update(self):
        # Déplacement de la balle en fonction du vecteur de direction
        self.rect.x += self.dx
        self.rect.y += self.dy
