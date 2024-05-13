from inventory import Inventory

class Item:
    def __init__ (self, nom, info):
        self.nom = nom
        self.info = info  
      
#toutes les classes suivantes héritent de la classe item#
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

# Création de l'inventaire
inventory = Inventory()

# Création des objets
bandage = Healer ("bandage", "bout de tissus")
paladin = Armor ("paladin", "vielle armure antique")
baies = Healer ("baies", "fruit qui apporte la vie")

# Ajout des objets à l'inventaire
inventory.add(bandage)
inventory.add(paladin)

# Affichage de l'inventaire
inventory.afficher()

