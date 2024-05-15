import pygame
import math
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):  # Modifier la signature de la méthode __init__
        super().__init__()
        self.position = [x, y]  # Convertir en liste
        self.angle = angle
        self.speed = BULLET_SPEED
        self.lifetime = BULLET_LIFETIME
        self.damage = BULLET_DAMAGE
        self.image = pygame.Surface((BULLET_SCALE, BULLET_SCALE))
        self.image.fill((255, 255, 255))  # Couleur de la balle (blanc)
        self.rect = self.image.get_rect(center=self.position)  # Créer un rect à partir de l'image

    def update(self):
        self.position[0] += math.cos(self.angle) * self.speed
        self.position[1] += math.sin(self.angle) * self.speed
        self.rect.center = self.position  # Mettre à jour la position du rect

    #  Ajouter une méthode pour vérifier les collisions avec monstres ou autres (A TERMINER)
    def check_collision(self, x, y):
        distance = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        return distance < 10