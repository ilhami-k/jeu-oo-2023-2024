import pygame 
class Item:
    def __init__ (self, nom, info, color, size):
        self.nom = nom
        self.info = info
        self.color = color
        self.size = size

    def draw_item(self, surface, position):
        pygame.draw.rect(surface, self.color, (position[0], position[1], self.size[0], self.size[1]))
      
#toutes les classes suivantes héritent de la classe item
class Healer (Item):
    """reprend tout les objets pour le soin
    si le max n'est pas déja atteint"""
    def heal (self):
        pass

class Power (Item):
    """reprend les amélioration qui auront pour effet 
    changer la qualité de la balle tirée (vitesse, damage, taille)"""
    def damage (self):
        pass

class Armor (Item):
    """reprend les armures qui créent une deuxieme barre de vie"""
    def protect():
        pass


pomme = Healer("pomme", "fruit qui apporte de la vie", (255, 0, 0), (20, 20))
baie = Healer("baie", "fruit qui remonte un peu la vie", (0, 255, 0), (15, 15))
militaire = Armor("militaire", "armure de grade militaire", (0, 0, 255), (40, 40))
police = Armor("police", "armure de police", (255, 255, 0), (40, 40))
uzi = Power("uzi", "arme automatique à courte portée", (255, 0, 255), (30, 15))
bazooka = Power("bazooka", "arme explosive à longue portée", (0, 255, 255), (40, 20))
pistol = Power("pistol", "arme de poing standard", (255, 0, 0), (25, 15))


list_items = [pomme, baie, militaire, police, uzi, bazooka, pistol]