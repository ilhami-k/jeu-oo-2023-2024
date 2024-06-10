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


class Booster(Item):
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
            'type':'Booster',
            'shield':self.shield
        })
        return data
    def deserialize(data):
        return Booster(data['nom'], data['info'], data['scale'], data['color'], data['shield'])

apple = Healer('pomme', APPLE_INFO, APPLE_SCALE, APPLE_COLOR, APPLE_HEAL)
berry = Healer("baie", BERRY_INFO, BERRY_SCALE, BERRY_COLOR, BERRY_HEAL)
military = Booster("militaire", MILITARY_INFO, MILITARY_SCALE, MILITARY_COLOR, MILITARY_SHIELD)
police = Booster("police", POLICE_INFO, POLICE_SCALE, POLICE_COLOR, POLICE_SHIELD)
tooth = Item( 0, 0, "dent", TOOTH_INFO, TOOTH_SCALE, TOOTH_COLOR)
heart = Item(0, 0, "coeur", HEART_INFO, HEART_SCALE, HEART_COLOR)
peluche = Item(0, 0, "peluche", PELUCHE_INFO, PELUCHE_SCALE, PELUCHE_COLOR)