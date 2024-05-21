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
    def __init__(self,name,description,goal,current = 0):
        self.name = name
        self.description = description
        self.goal = goal
        self.current = current
        self.completed = False

    def updateProgress(self):
        if not self.completed: #Si objectif pas complété
            self.current += 1
            self.checkCompletion(self.current) #envoie la valeur de self.current comme donnée à la méthode de la classe mère qui regarde si la quête est complétée.

    def checkCompletion(self,current):
          if current >= self.goal:
                self.completed = True #Objectif complété

class MainQuest(Quest):
    def __init__(self,name,description,goal):
        super().__init__(name,description,goal)
    
class SecondaryQuests(Quest):
    def __init__(self,name,description,goal):
        super().__init__(name,description,goal)

class QuestManager:
    def __init__(self):
        self.quests = [] #Liste quêtes
    
    def addQuest(self,quest):
        self.quests.append(quest)
    
    def active_quests(self):
        return [quest for quest in self.quests if not quest.completed] #compréhension de liste qui fait une liste qui comprendra les quêtes qui se trouvent dans la liste self.quests et qui ne sont pas completed 
    
    def completed_quests(self):
        return [quest for quest in self.quests if quest.completed] ##compréhension de liste qui fait une liste qui comprendra les quêtes qui se trouvent dans la liste self.quests et qui sont completed 
    
    def display_quests(self):
        print("Active Quests:")
        for quest in self.active_quests():
            print("- {}: {}".format(quest.name,quest.description))
        for quest in self.completed_quests():
            print("- {}: {} ({}/{})".format(quest.name,quest.description,quest.current,quest.goal))