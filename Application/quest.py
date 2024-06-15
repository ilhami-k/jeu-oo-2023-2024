import textwrap
import pygame
from item import *
from inventory import *
class Quest:
    """
    Représente une quête avec un objectif spécifique à atteindre.

    Attributs:
        name (str): Le nom de la quête.
        description (str): Une brève description de la quête.
        goal (int): La valeur cible à atteindre pour compléter la quête.
        reward_given (bool): Indique si la récompense pour la quête a été donnée.
        manager: Le gestionnaire responsable de la quête.
        current (int): La progression actuelle de la quête.
        completed (bool): Indique si la quête est terminée.
    """

    def __init__(self, name, description, goal, manager, current=0):
        self.name = name
        self.description = description
        self.goal = goal
        self.reward_given = False
        self.manager = manager
        self.current = current
        self.completed = False

    def updateProgress(self):
        """
        Met à jour la progression de la quête en incrémentant la valeur actuelle de 1.
        Vérifie si la quête est complétée après la mise à jour de la progression.
        """
        print('Mise à jour de la progression pour', self.name)
        if not self.completed:
            self.current += 1
            self.checkCompletion()
            print(self.current)
        
    def checkCompletion(self):
        """
        Vérifie si la progression actuelle atteint ou dépasse l'objectif.
        Marque la quête comme complétée et informe le gestionnaire de supprimer la quête si elle est complétée.
        """
        if self.current >= self.goal:
            self.completed = True
            if self.completed:
                print(f'La quête {self.name} est terminée')
            self.manager.deleteQuest(self)
            self.current = 0

    def to_dict(self):
        """
        Convertit les attributs de la quête en un dictionnaire.
        Retourne:
            dict: Une représentation sous forme de dictionnaire de la quête.
        """
        return {
            'name': self.name,
            'description': self.description,
            'goal': self.goal,
            'current': self.current,
            'completed': self.completed
        }
import pygame
import textwrap

class QuestManager:
    """
    Gère une liste de quêtes, permettant l'ajout, la suppression et l'affichage des quêtes.

    Attributs:
        quests (list): La liste des quêtes.
    """

    def __init__(self):
        self.quests = []

    def add_quest(self, quest):
        """
        Ajoute une quête à la liste des quêtes.

        Paramètres:
            quest (Quest): La quête à ajouter.
        """
        self.quests.append(quest)
    
    def deleteQuest(self, quest):
        """
        Supprime une quête de la liste des quêtes si elle y est présente.

        Paramètres:
            quest (Quest): La quête à supprimer.
        """
        if quest in self.quests:
            self.quests.remove(quest)

    def has_quest(self, quest_name):
        """
        Vérifie si une quête avec un nom spécifique est présente dans la liste des quêtes.

        Paramètres:
            quest_name (str): Le nom de la quête à vérifier.

        Retourne:
            bool: True si la quête est présente, sinon False.
        """
        for quest in self.quests:
            if quest.name == quest_name:
                return True
        return False

    def show_quests(self, screen, font, WIDTH):
        """
        Affiche la liste des quêtes à l'écran.

        Paramètres:
            screen: L'écran où afficher les quêtes.
            font: La police utilisée pour afficher le titre.
            WIDTH (int): La largeur de l'écran.
        """
        small_font = pygame.font.Font(None, 24)  # Définit une police plus petite pour les quêtes

        # Crée une surface pour l'affichage
        quests_surface = pygame.Surface((300, 400), pygame.SRCALPHA)
        quests_surface.fill((50, 50, 50, 128))  # Remplit la surface avec une couleur de fond semi-transparente
        y_offset = 1  # Initialisation de l'offset vertical pour l'affichage

        # Affichage du titre
        title = font.render("Quêtes", True, (255, 255, 255))  # Blanc
        title_rect = title.get_rect(topleft=(10, 30))
        screen.blit(title, title_rect)

        for quest in self.quests:
            # Divise le texte des quêtes en plusieurs lignes si nécessaire pour s'adapter à la largeur de 30 caractères
            item_text_lines = textwrap.wrap(f"{quest.name}: {quest.description} ({quest.current}/{quest.goal})", width=30)
            for line in item_text_lines:
                quests_text = small_font.render(line, True, (255, 255, 255))  # Rend chaque ligne de texte en blanc
                quests_surface.blit(quests_text, (20, y_offset))  # Affiche la ligne de texte sur la surface
                y_offset += 20

        screen.blit(quests_surface, (10, 80))

    def all_quests(self):
        """
        Renvoie une liste de dictionnaires représentant toutes les quêtes.

        Retourne:
            list: Une liste de dictionnaires contenant les données des quêtes.
        """
        quest_data = []
        for quest in self.quests:
            quest_data.append(quest.to_dict())
        return quest_data
