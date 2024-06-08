import textwrap
import pygame
from item import *
from inventory import *
#Mission principale:
#Tuer le boss qui pop dés que le jeu commence apres le prologue

#Quetes:
#quete1 où il faut tuer x ennemis

#quete2 où il faut ramasser x item sur des ennemis
#Mission principale:
#Tuer le boss qui pop dés que le jeu commence apres le prologue

#Quetes:
#quete1 où il faut tuer x ennemis

#quete2 où il faut ramasser x item sur des ennemis

#Mission principale affichée apres introduction
class Quest:
    def __init__(self,name,description,goal,manager,current = 0):
        self.name = name
        self.description = description
        self.goal = goal
        self.reward_given = False
        self.manager = manager
        self.current = current
        self.completed = False

    def updateProgress(self):
        print('updating progress for ',self.name)
        if not self.completed: #Si objectif pas complété
            self.current += 1
            self.checkCompletion()
            print(self.current)
        
    def checkCompletion(self):
          if self.current >= self.goal: #and not self.completed
                self.completed = True #Objectif complété
                if self.completed:
                    print(f'Quest {self.name} is completed')
                self.manager.deleteQuest(self)  # Supprime la quête du gestionnaire
                self.current = 0
    def to_dict (self):
        return {
            'name': self.name,
            'description': self.description,
            'goal': self.goal,
            'current': self.current,
            'completed': self.completed
        
        }

class QuestManager:
    def __init__(self):
        self.quests = [] #Liste quêtes
      
    
    def add_quest(self,quest):
        self.quests.append(quest)
    
    def deleteQuest(self,quest):
        if quest in self.quests:
            self.quests.remove(quest)

    def has_quest(self, quest_name):
        for quest in self.quests:
            if quest.name == quest_name:
                return True
        return False

    def show_quests(self, screen, font, WIDTH):
        small_font = pygame.font.Font(None, 24)  # Définit une police plus petite pour les quetes

        # Créé une surface pour l'affichage
        quests_surface = pygame.Surface((300, 400), pygame.SRCALPHA)
        quests_surface.fill((50, 50, 50, 128))  # Remplit la surface avec une couleur de fond semi-transparente
        y_offset = 1  # Initialisation de l'offset vertical pour l'affichage
        # affichage du titre
        title = font.render("Quêtes", True, (255, 255, 255))  # Blanc
        title_rect = title.get_rect(topleft=(10, 30))
        screen.blit(title, title_rect)

        for quest in self.quests:
            # Divise le texte des quetes en plusieurs lignes si nécessaire pour s'adapter à la largeur de 35 caractères
            item_text_lines = textwrap.wrap(f"{quest.name}: {quest.description} ({quest.current}/{quest.goal})", width=30)
            for line in item_text_lines:
                quests_text = small_font.render(line, True, (255, 255, 255))  # Rend chaque ligne de texte en blanc
                quests_surface.blit(quests_text, (20, y_offset))  # Affiche la ligne de texte sur la surface
                y_offset += 20

        screen.blit(quests_surface, (10, 80))

    def all_quests(self):
        quest_data = []
        for quest in self.quests:
            quest_data.append(quest.to_dict())
        return quest_data
