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
    def __init__(self,name,description,goal,reward,manager,inventory,current = 0):
        self.name = name
        self.description = description
        self.goal = goal
        self.reward = reward
        self.manager = manager
        self.inventory = inventory
        self.current = current
        self.completed = False

    def updateProgress(self):
        if not self.completed: #Si objectif pas complété
            self.current += 1
            self.checkCompletion(self.inventory)
        
    def checkCompletion(self,inventory):
          if self.current >= self.goal: #and not self.completed
                self.completed = True #Objectif complété
                print(self.reward.nom)
                inventory.add_item(self.reward) #Ajoute la récompense à l'inventaire
                self.manager.deleteQuest(self)  # Supprime la quête du gestionnaire
                self.current = 0

class QuestManager:
    def __init__(self):
        self.quests = [] #Liste quêtes
      
    
    def addQuest(self,quest):
        self.quests.append(quest)
    
    def deleteQuest(self,quest):
        if quest in self.quests:
            self.quests.remove(quest)

    def show_quests(self,screen,font,WIDTH):
        small_font = pygame.font.Font(None,24) #Définit une police plus petite pour les quetes
        quest_surface_x = 10

        #Créé une surface pour l'affichage
        quests_surface = pygame.Surface((300,400), pygame.SRCALPHA) 
        quests_surface.fill((50, 50, 50, 128))  # Remplit la surface avec une couleur de fond semi-transparente
        y_offset = 1 # Initialisation de l'offset vertical pour l'affichage
        #affichage du titre 
        title = font.render("Quêtes", True, (255, 255, 255))  # Blanc 
        title_rect = title.get_rect(center=(WIDTH / 2, 150))
        screen.blit(title, title_rect) 

        for quest in self.quests:
            # Divise le texte des quetes en plusieurs lignes si nécessaire pour s'adapter à la largeur de 35 caractères
            item_text_lines = textwrap.wrap(f"{quest.name}: {quest.description} {quest.current}/{quest.goal}", width=35)
            for line in item_text_lines:
                quests_text = small_font.render(line, True, (255, 255, 255))  # Rend chaque ligne de texte en blanc
                quests_surface.blit(quests_text, (20, y_offset))  # Affiche la ligne de texte sur la surface
                y_offset += 20  # Ajoute un espace vertical entre les lignes
            
    
       # Affiche la surface de l'inventaire sur l'écran principal
        screen.blit(quests_surface, (WIDTH - 310, 10))  # Positionne l'inventaire dans le coin supérieur droit
