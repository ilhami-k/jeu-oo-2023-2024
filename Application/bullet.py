import pygame
import math
from settings import *

class Bullet(pygame.sprite.Sprite):
    """
    Représente un projectile de balle dans le jeu.

    Attributs :
        position (list): Coordonnées actuelles de la balle [x, y].
        angle (float): Angle en radians représentant la direction du mouvement.
        speed (int): Vitesse de la balle.
        lifetime (int): Durée de vie restante de la balle en frames.
        damage (int): Dommages infligés par la balle lors de la collision.
        radius (int): Rayon de la balle pour la détection de collision.
        image (pygame.Surface): Surface représentant l'apparence visuelle de la balle.
        rect (pygame.Rect): Rectangle englobant l'image de la balle pour la détection de collision.

    Méthodes :
        __init__(self, x, y, angle, speed, lifetime, damage, radius, color):
            Initialise un nouvel objet Bullet avec les attributs spécifiés.
        
        update(self):
            Met à jour la position de la balle en fonction de son angle et de sa vitesse.
        
        check_collision(self, target):
            Vérifie la collision entre la balle et un sprite cible.

    """
    def __init__(self, x, y, angle, speed, lifetime, damage, radius, color):
        super().__init__()
        self.position = [x, y]  # Convertir la position en format liste
        self.angle = angle
        self.speed = speed
        self.lifetime = lifetime
        self.damage = damage
        self.radius = radius

        # Créer une surface pour la balle et dessiner un cercle dessus
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=self.position)
  
    def update(self):
        """
        Met à jour la position de la balle en fonction de son angle et de sa vitesse.
        """
        self.position[0] += math.cos(self.angle) * self.speed
        self.position[1] += math.sin(self.angle) * self.speed
        self.rect.center = self.position  
        
        # Diminue la durée de vie de la balle
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()  # Supprime la balle si elle atteint la fin de sa durée de vie

    def check_collision(self, target):
        """
        Vérifie la collision entre la balle et un sprite cible.

        Args:
            target (pygame.sprite.Sprite): Le sprite cible pour vérifier la collision.
        
        Returns:
            bool: True si une collision est détectée, False sinon.
        """
        if pygame.sprite.collide_circle(self, target):
            return True
        else:
            return False

class BasicBullet(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle, BULLET_SPEED, BULLET_LIFETIME, BULLET_DAMAGE, BULLET_RADIUS, BULLET_COLOR)

class SuperBullet(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle, SUPER_BULLET_SPEED, SUPER_BULLET_LIFETIME, SUPER_BULLET_DAMAGE, SUPER_BULLET_RADIUS, SUPER_BULLET_COLOR)

class SniperBullet(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle, SNIPER_BULLET_SPEED, SNIPER_BULLET_LIFETIME, SNIPER_BULLET_DAMAGE, SNIPER_BULLET_RADIUS, SNIPER_BULLET_COLOR)

class BossBullet(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle, GOLEM_SHOOT_SPEED, GOLEM_SHOOT_LIFETIME, GOLEM_SHOOT_DAMAGE, GOLEM_SHOOT_RADIUS, GOLEM_SHOOT_COLOR)
