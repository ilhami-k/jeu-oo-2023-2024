import pygame
from settings import *
from entity import *


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, nom, info, scale, color):
        super().__init__()
        self.position = [x, y]
        self.nom = nom
        self.info = info
        self.image = pygame.Surface((scale, scale))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=self.position)

    def serialize(self):
        color = self.image.get_at((0, 0))
        return {
            'type': 'Item',
            'x': self.position[0],
            'y': self.position[1],
            'nom': self.nom,
            'info': self.info,
            'scale': self.image.get_width(),
            'color': [color.r, color.g, color.b, color.a]
        }

    def deserialize(data):
        color = pygame.Color(*data['color'])
        return Item(data['x'], data['y'], data['nom'], data['info'], data['scale'], color)
    
class Healer(Item):
    def __init__(self, nom, info, scale, color, heal):
        super().__init__(0, 0, nom, info, scale, color)  # Note: Position temporaire (0, 0)
        self.heal = heal
    def serialize(self):
        data = super().serialize()
        data.update({'type':'Healer', 'heal': self.heal})
        return data


    def deserialize(data):
        color = pygame.Color(*data['color'])
        return Healer(data['nom'], data['info'], data['scale'], color, data['heal'])
    def healing(self, player):
        if isinstance(player, Player):           
            player.health = min (player.health + self.heal, player.max_health) 


class Weapon(Item):
    """Reprend les améliorations qui auront pour effet 
    de changer la qualité de la balle tirée (vitesse, dégâts, taille)"""
    def __init__(self, nom, info, scale, color, bullet_speed, bullet_damage, bullet_scale):
        super().__init__(0, 0, nom, info, scale, color)  # Note: Position temporaire (0, 0)
        self.bullet_speed = bullet_speed
        self.bullet_damage = bullet_damage
        self.bullet_scale = bullet_scale
        

    def serialize(self):
        data = super().serialize()
        data.update({
            'type': 'Weapon',
            'bullet_speed': self.bullet_speed,
            'bullet_damage': self.bullet_damage,
            'bullet_scale': self.bullet_scale
        })
        return data


    def deserialize(data):
        color = pygame.Color(*data['color'])
        return Weapon(data['nom'], data['info'], data['scale'], color, data['bullet_speed'], data['bullet_damage'], data['bullet_scale'])
class Armor(Item):
    """Reprend les armures qui augmentent la barre de vie principale"""
    def __init__(self, nom, info, scale, color, shield):
        super().__init__(0, 0, nom, info, scale, color)  # Note: Position temporaire (0, 0)
        self.shield = shield

    def protect(self, player):
        if isinstance(player, Player):
            player.max_health += self.shield
            player.health += self.shield

    def serialize(self):
        data = super().serialize()
        data.update({
            'type':'Armor',
            'shield':self.shield
        })
        return data
    def deserialize(data):
        return Armor(data['nom'], data['info'], data['scale'], data['color'], data['shield'])

appel = Healer('pomme', APPLE_INFO, APPLE_SCALE, APPLE_COLOR, APPLE_HEAL)
berry = Healer("baie", BERRY_INFO, BERRY_SCALE, BERRY_COLOR, BERRY_HEAL)
military = Armor("militaire", MILITARY_INFO, MILITARY_SCALE, MILITARY_COLOR, MILITARY_SHIELD)
police = Armor("police", POLICE_INFO, POLICE_SCALE, POLICE_COLOR, POLICE_SHIELD)
uzi = Weapon("uzi", UZI_INFO, UZI_SCALE, UZI_COLOR, UZI_SPEED, UZI_DAMAGE, UZI_SCALE)
bazooka = Weapon("bazooka", BAZOOKA_INFO, BAZOOKA_SCALE, BAZOOKA_COLOR, BAZOOKA_SPEED, BAZOOKA_DAMAGE, BAZOOKA_SCALE)
pistol = Weapon("pistol", PISTOL_INFO, PISTOL_SCALE, PISTOL_COLOR, PISTOL_SPEED, PISTOL_DAMAGE, PISTOL_SCALE)
tooth = Item( 0, 0, "dent", TOOTH_INFO, TOOTH_SCALE, TOOTH_COLOR)
heart = Item(0, 0, "coeur", HEART_INFO, HEART_SCALE, HEART_COLOR)
peluche = Item(0, 0, "peluche", PELUCHE_INFO, PELUCHE_SCALE, PELUCHE_COLOR)