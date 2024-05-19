#Mission principale:
#Tuer le boss qui pop dés que le jeu commence apres le prologue

#Quetes:
#quete1 où il faut tuer x ennemis

#quete2 où il faut ramasser x item sur des ennemis
class Objective:
    def __init__(self,description,goal, current = 0):
        self.description = description
        self.goal = goal
        self.current = current
        self.completed = False
    
    def updateProgress(self):
        if not self.completed: #Si objectif pas complété
            self.current += 1
            if self.current >= self.goal:
                self.completed = True #Objectif complété


class Quest:
    def __init__(self,name,description,goal):
        self.name = name
        self.description = description
        self.goal = goal
        self.completed = False

    def checkCompletion(self):
        pass

class QuestManager:
    def __init__(self):
        self.quests = [] #Liste quêtes
    
    def addQuest(self,quest):
        self.quests.append(quest)
    
    def active_quests(self):
        pass
    
    def completed_quests(self):
        pass

    def update(self):
        for quest in self.quests:
            quest.check_completion()
    
    def display_quests(self):
        print("Active Quests:")