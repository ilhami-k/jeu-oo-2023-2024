import pygame
import math
from settings import *
from bullet import Bullet

class Entite(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites, image_path):
        super().__init__() 
        self.position = [x, y]
        self.old_position = self.position.copy()  
        self.all_sprites = all_sprites  
        self.sprite_sheet = pygame.image.load(image_path)
        self.image = self.get_image(48, 0)
        self.image.set_colorkey((0, 0, 0))  
        self.rect = self.image.get_rect()

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

    def update(self):
        self.rect.topleft = self.position

class Player(Entite):
    def __init__(self, x, y, all_sprites):
        super().__init__(x, y, all_sprites, "Application/Player.png")
        self.speed = PLAYER_SPEED  
        self.shoot_cooldown = 0 

    def shoot(self, target_x, target_y, bullet_group):
        window_center_x = WIDTH // 2
        window_center_y = HEIGHT // 2
        angle = math.atan2(target_y - window_center_y, target_x - window_center_x)
        bullet_group.add(Bullet(window_center_x, window_center_y, angle))

    def cooldown_tick(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

class Enemy(Entite):
    def __init__(self, x, y, all_sprites):
        super().__init__(x, y, all_sprites, "Application/Enemy1.png")
        # self.image = self.get_image(0, 0)  # Ajustez les paramètres ici si nécessaire
        self.speed = ENEMY_SPEED

    # Ajoutez ici les autres méthodes spécifiques à la classe Enemy

class PNJ(Entite):
    pass  # Ajoutez ici les méthodes et attributs spécifiques à la classe PNJ
