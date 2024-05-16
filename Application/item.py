import pygame
from settings import *

class Item:
    def __init__ (self, nom, info, scale, color):
        self.nom = nom
        self.info = info
        self.scale = scale
        self.color = color

    def draw_item(self, surface, position):
        pygame.draw.rect(surface, self.color, (position[0], position[1], self.scale[0], self.scale[1]))
      
#toutes les classes suivantes héritent de la classe item
class Healer (Item):
    def __init__(self, nom, info, scale, color, heal):
        super().__init__(nom, info, scale, color)
        self.heal = heal
    """reprend tout les objets pour le soin
    si le max n'est pas déja atteint"""
    def healing (self):
        pass

class Power (Item):
    """reprend les amélioration qui auront pour effet 
    changer la qualité de la balle tirée (vitesse, damage, taille)"""
    def __init__(self, nom, info, scale, color, bullet_speed, bullet_damage, bullet_size):
        super().__init__(nom, info, scale, color)
        self.bullet_speed = bullet_speed
        self.bullet_damage = bullet_damage
        self.bullet_size = bullet_size        
    def damage (self):
        pass

class Armor (Item):
    """reprend les armures qui augmente la barre de vie principale"""
    def __init__(self, nom, info, scale, color, shield):
        super().__init__(nom, info, scale, color)
        self.shield = shield
    def protect():
        pass


appel = Healer('pomme', APPLE_INFO, APPLE_SCALE, APPEL_COLOR, APPLE_HEAL)
berry = Healer("baie", BERRY_INFO, BERRY_SCALE, BERRY_COLOR, BERRY_HEAL)
military= Armor("militaire", MILITARY_INFO, MILITARY_SCALE, MILITARY_COLOR, MILITARY_SHIELD )
police = Armor("police", PISTOL_INFO, PISTOL_SCALE, PISTOL_COLOR, MILITARY_SHIELD)
uzi = Power("uzi", UZI_INFO, UZI_SCALE, UZI_COLOR, UZI_SPEED, UZI_DAMAGE, UZI_SCALE)
bazooka = Power("bazooka", BAZOOKA_INFO, BAZOOKA_SCALE, BAZOOKA_COLOR, BAZOOKA_SPEED, BAZOOKA_DAMAGE, BAZOOKA_SCALE)
pistol = Power("pistol", PISTOL_INFO, PISTOL_SCALE, PISTOL_COLOR, PISTOL_SPEED, PISTOL_DAMAGE, PISTOL_SCALE)


list_items = [appel, berry, military, police, uzi, bazooka, pistol]