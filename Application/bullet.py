import pygame
import math
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, speed, lifetime, damage, scale, color):
        super().__init__()
        self.position = [x, y]  # Convertir la position en liste
        self.angle = angle
        self.speed = speed
        self.lifetime = lifetime
        self.damage = damage
        self.image = pygame.Surface((scale, scale))
        self.image.fill(color)  
        self.rect = self.image.get_rect(center=self.position)
        
    def update(self):
        self.position[0] += math.cos(self.angle) * self.speed
        self.position[1] += math.sin(self.angle) * self.speed
        self.rect.center = self.position  

    #  Ajouter une méthode pour vérifier les collisions avec monstres ou autres (A TERMINER)
    def check_collision(self, x, y):
        distance = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        return distance < 10
  
    
class BasicBullet(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle, BULLET_SPEED, BULLET_LIFETIME, BULLET_DAMAGE, BULLET_SCALE, BULLET_COLOR)    
    
class SuperBullet(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle, SUPER_BULLET_SPEED, SUPER_BULLET_LIFETIME, SUPER_BULLET_DAMAGE, SUPER_BULLET_SCALE, SUPER_BULLET_COLOR)

class SniperBullet(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle, SNIPER_BULLET_SPEED, SNIPER_BULLET_LIFETIME, SNIPER_BULLET_DAMAGE, SNIPER_BULLET_SCALE, SNIPER_BULLET_COLOR)

class BossBullet(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle, GOLEM_SHOOT_SPEED, GOLEM_SHOOT_LIFETIME, GOLEM_SHOOT_DAMAGE, GOLEM_SHOOT_SCALE, GOLEM_SHOOT_COLOR)