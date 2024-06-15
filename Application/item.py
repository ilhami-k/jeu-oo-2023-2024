import pygame
from settings import *
from entity import Player

class Item(pygame.sprite.Sprite):
    """
    Classe de base représentant un item dans le jeu.

    Attributes:
        position (list): Les coordonnées x et y de l'item.
        nom (str): Le nom de l'item.
        info (str): Des informations supplémentaires sur l'item.
        image (pygame.Surface): La surface de l'image de l'item.
        rect (pygame.Rect): Le rectangle de collision de l'item.
        player (Player): Le joueur associé à l'item (par défaut initialisé à (0,0)).
    """

    def __init__(self, x, y, nom, info, scale, color):
        super().__init__()
        self.position = [x, y]
        self.nom = nom
        self.info = info
        self.image = pygame.Surface((scale, scale))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=self.position)
        self.player = Player(0, 0)  # Note: Player initialisé à (0,0)

    def serialize(self):
        """
        Convertit l'item en un dictionnaire pour la sérialisation.

        Returns:
            dict: Un dictionnaire contenant les attributs de l'item.
        """
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
        """
        Désérialise les données d'un dictionnaire pour créer un objet Item.

        Args:
            data (dict): Le dictionnaire contenant les données de l'item.

        Returns:
            Item: L'objet Item créé à partir des données.
        """
        color = pygame.Color(*data['color'])
        return Item(data['x'], data['y'], data['nom'], data['info'], data['scale'], color)


class Healer(Item):
    """
    Classe représentant un item de type Healer, qui peut guérir le joueur.

    Attributes:
        heal (int): La quantité de guérison que cet item fournit.
    """

    def __init__(self, nom, info, scale, color, heal):
        super().__init__(0, 0, nom, info, scale, color)  # Note: Position temporaire (0, 0)
        self.heal = heal

    def serialize(self):
        """
        Convertit l'item Healer en un dictionnaire pour la sérialisation.

        Returns:
            dict: Un dictionnaire contenant les attributs de l'item Healer.
        """
        data = super().serialize()
        data.update({'type': 'Healer', 'heal': self.heal})
        return data

    def deserialize(data):
        """
        Désérialise les données d'un dictionnaire pour créer un objet Healer.

        Args:
            data (dict): Le dictionnaire contenant les données de l'item Healer.

        Returns:
            Healer: L'objet Healer créé à partir des données.
        """
        color = pygame.Color(*data['color'])
        return Healer(data['nom'], data['info'], data['scale'], color, data['heal'])

    def healing(self, player):
        """
        Fonction qui guérit le joueur en augmentant sa santé actuelle jusqu'à sa santé maximale.

        Args:
            player (Player): Le joueur à guérir.
        """
        if isinstance(player, Player):
            print("Appel de la fonction healing")
            print(f"Vie actuelle du joueur: {player.health}/{player.max_health}")
            player.health = min(player.health + self.heal, player.max_health)
            print(f"Vie après heal: {player.health}/{player.max_health}")


class Booster(Item):
    """
    Classe représentant un item de type Booster, qui augmente la santé maximale du joueur.

    Attributes:
        shield (int): La quantité de santé maximale que cet item ajoute.
    """

    def __init__(self, nom, info, scale, color, shield):
        super().__init__(0, 0, nom, info, scale, color)  # Note: Position temporaire (0, 0)
        self.shield = shield

    def boost(self, player):
        """
        Fonction qui augmente la santé maximale du joueur.

        Args:
            player (Player): Le joueur à booster.
        """
        if isinstance(player, Player):
            print("Appel de la fonction boost")
            player.max_health += self.shield
            player.health += self.shield
            print(f"Vie totale augmentée : {self.player.max_health}")

    def serialize(self):
        """
        Convertit l'item Booster en un dictionnaire pour la sérialisation.

        Returns:
            dict: Un dictionnaire contenant les attributs de l'item Booster.
        """
        data = super().serialize()
        data.update({
            'type': 'Booster',
            'shield': self.shield
        })
        return data
    def deserialize(data):
        """
        Désérialise les données d'un dictionnaire pour créer un objet Booster.

        Args:
            data (dict): Le dictionnaire contenant les données de l'item Booster.

        Returns:
            Booster: L'objet Booster créé à partir des données.
        """
        return Booster(data['nom'], data['info'], data['scale'], data['color'], data['shield'])

# Exemples d'objets créés
apple = Healer("pomme", APPLE_INFO, APPLE_SCALE, APPLE_COLOR, APPLE_HEAL)
berry = Healer("baie", BERRY_INFO, BERRY_SCALE, BERRY_COLOR, BERRY_HEAL)
military = Booster("militaire", MILITARY_INFO, MILITARY_SCALE, MILITARY_COLOR, MILITARY_SHIELD)
police = Booster("police", POLICE_INFO, POLICE_SCALE, POLICE_COLOR, POLICE_SHIELD)
tooth = Item(0, 0, "dent", TOOTH_INFO, TOOTH_SCALE, TOOTH_COLOR)
heart = Item(0, 0, "coeur", HEART_INFO, HEART_SCALE, HEART_COLOR)
peluche = Item(0, 0, "peluche", PELUCHE_INFO, PELUCHE_SCALE, PELUCHE_COLOR)
