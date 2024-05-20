import pygame
from settings import *


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, nom, info, size, color):
        super().__init__()
        self.position = [x, y]
        self.nom = nom
        self.info = info
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Toutes les classes suivantes héritent de la classe Item
class Healer(Item):
    def __init__(self, nom, info, size, color, heal):
        super().__init__(0, 0, nom, info, size, color)  # Note: Position temporaire (0, 0)
        self.heal = heal

    def healing(self):
        # Reprend tout les objets pour le soin
        # Si le maximum n'est pas déjà atteint
        pass

    def draw_item(self, surface, position):
        surface.blit(self.image, position)

class Power(Item):
    """Reprend les améliorations qui auront pour effet 
    de changer la qualité de la balle tirée (vitesse, dégâts, taille)"""
    def __init__(self, nom, info, size, color, bullet_speed, bullet_damage, bullet_size):
        super().__init__(0, 0, nom, info, size, color)  # Note: Position temporaire (0, 0)
        self.bullet_speed = bullet_speed
        self.bullet_damage = bullet_damage
        self.bullet_size = bullet_size
        
    def damage(self):
        pass     

class Armor(Item):
    """Reprend les armures qui augmentent la barre de vie principale"""
    def __init__(self, nom, info, size, color, shield):
        super().__init__(0, 0, nom, info, size, color)  # Note: Position temporaire (0, 0)
        self.shield = shield

    def protect(self):
        pass


appel = Healer('pomme', APPLE_INFO, APPLE_SCALE, APPLE_COLOR, APPLE_HEAL)
berry = Healer("baie", BERRY_INFO, BERRY_SCALE, BERRY_COLOR, BERRY_HEAL)
military = Armor("militaire", MILITARY_INFO, MILITARY_SCALE, MILITARY_COLOR, MILITARY_SHIELD)
police = Armor("police", PISTOL_INFO, PISTOL_SCALE, PISTOL_COLOR, POLICE_SHIELD)
uzi = Power("uzi", UZI_INFO, UZI_SCALE, UZI_COLOR, UZI_SPEED, UZI_DAMAGE, UZI_SCALE)
bazooka = Power("bazooka", BAZOOKA_INFO, BAZOOKA_SCALE, BAZOOKA_COLOR, BAZOOKA_SPEED, BAZOOKA_DAMAGE, BAZOOKA_SCALE)
pistol = Power("pistol", PISTOL_INFO, PISTOL_SCALE, PISTOL_COLOR, PISTOL_SPEED, PISTOL_DAMAGE, PISTOL_SCALE)
tooth = Item( 0, 0, "dent", TOOTH_INFO, TOOTH_SCALE, TOOTH_COLOR)
