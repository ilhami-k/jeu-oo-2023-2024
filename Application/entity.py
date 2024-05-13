import pygame
import math
from settings import *
from bullet import Bullet
from game import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, name, speed, health, attack_cooldown=0):
        super().__init__()
        self.name = name 
        self.position = [x, y]
        self.old_position = self.position.copy()   
        self.sprite_sheet = pygame.image.load(image_path)
        self.image = self.get_image(48, 0)
        self.image.set_colorkey((0, 0, 0))  
        self.rect = self.image.get_rect()
        self.speed = speed
        self.health = health
        self.attack_cooldown = attack_cooldown

    def get_image(self, x, y):
        image = pygame.Surface((16, 24))  # Réduire la hauteur de 8 pixels de l'image
        image.blit(self.sprite_sheet, (0, -8), (x, y, 16, 32))  # Déplacer le contenu de l'image de 8 pixels vers le bas pour ne pas perdre la réduction réaluisée juste avant
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
        super().__init__(x, y, "Application/Player.png", 'Player', PLAYER_SPEED, PLAYER_HEALTH, ATTACK_COOLDOWN)

    def shoot(self, target_x, target_y, bullet_group):
        angle = math.atan2(target_y - self.position[1], target_x - self.position[0])
        bullet_group.add(Bullet(self.position[0], self.position[1], angle))

    def cooldown_tick(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

class Enemy(Entity):
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
            self.attack_cooldown = self.initial_attack_cooldown

class Zombie(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "Application/Zombie.png", 'Zombie', ZOMBIE_SPEED, ZOMBIE_HEALTH, ZOMBIE_ATTACK_COOLDOWN)
        self.initial_attack_cooldown = ZOMBIE_ATTACK_COOLDOWN

class Skeleton(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "Application/Skeleton.png", 'Skeleton', SKELETON_SPEED, SKELETON_HEALTH, SKELETON_ATTACK_COOLDOWN)
        self.initial_attack_cooldown = SKELETON_ATTACK_COOLDOWN

class Npc(Entity):
    pass  # Ajoutez ici les méthodes et attributs spécifiques à la classe PNJ
