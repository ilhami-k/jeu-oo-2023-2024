import pygame
import math
from settings import *
from bullet import Bullet
from game import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__() 
        self.position = [x, y]
        self.old_position = self.position.copy()   
        self.sprite_sheet = pygame.image.load(image_path)
        self.image = self.get_image(48, 0)
        self.image.set_colorkey((0, 0, 0))  
        self.rect = self.image.get_rect()

        self.health = PLAYER_HEALTH

    def get_image(self, x, y):
        image = pygame.Surface((16, 32))
        image.blit(self.sprite_sheet, (0, 0), (x, y, 16, 32))
        return image

    def save_location(self):
        self.old_position = self.position.copy()

    def move_back(self): 
        self.position = self.old_position.copy()
        self.rect.topleft = self.position
        
    def move(self, x, y):
        if x != 0 and y != 0:
            x *= math.sqrt(2) / 2
            y *= math.sqrt(2) / 2
        self.position[0] += x
        self.position[1] += y

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()  # Supprimer la spirte de l'ennemi du groupe

    def update(self, player):
        self.rect.topleft = self.position

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "Application/Player.png")
        self.speed = PLAYER_SPEED  
        self.shoot_cooldown = 0 

    def shoot(self, target_x, target_y, bullet_group):
        angle = math.atan2(target_y - self.position[1], target_x - self.position[0])
        bullet_group.add(Bullet(self.position[0], self.position[1], angle))

    def cooldown_tick(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "Application/Enemy1.png")
        # self.image = self.get_image(0, 0)  # Ajustez les paramètres ici si nécessaire
        self.speed = ENEMY_SPEED
        self.health = ENEMY_HEALTH
        self.attack_cooldown = 0

    def update(self, player):
        # Calculer la direction vers le joueur
        direction_x = player.position[0] - self.position[0]
        direction_y = player.position[1] - self.position[1]
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        # Déplacer l'ennemi dans la direction du joueur
        self.move(direction_x * self.speed, direction_y * self.speed)

        # Vérifier les collisions avec le joueur
        if self.rect.colliderect(player.rect):
            self.attack(player)

        # Gérer le temps entre les attaques
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # Mettre à jour la position du rectangle de collision
        self.rect.topleft = self.position

    def attack(self, player):
        # Vérifier si l'ennemi peut attaquer
        if self.attack_cooldown == 0:
            # Infliger des dégâts au joueur
            player.take_damage()
            # Réinitialiser le cooldown d'attaque
            self.attack_cooldown = ATTACK_COOLDOWN

class PNJ(Entity):
    pass  # Ajoutez ici les méthodes et attributs spécifiques à la classe PNJ
