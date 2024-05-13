import pygame


#information a propos de chaque type (icone, valeur, taille d'empillement, etc)
class Itemtype:
    def __init__(self,name, icon, stack_size=1):
        self.name=name
        self.icon_name = icon
        self.icon = pygame.image.load()
    

#contenir la quantité d'un objet 

class Itemslot:
    def __init__(self):
        self.type = None
        self.amout = 0

#contient les slots
class Inventory:
    def __init__ (self, capacity):
        self.capacity = capacity
        self.token_slots=0
        self.slots = []
        #variable muette
        for _ in range(self.capacity):
            self.slots.append(Itemslot())
        self.listener=None
        pass

    def notify (self):
        pass
    
    def add (self, item_type, amount = 1):
        if item_type.stack_size>1:
            

    def remove (self, item_type, amount = 1):
        in_invent = 0
        for slot in self.slots:
            if slot.type == item_type:
                if slot.amount < amount:
                    in_invent +=slot.amount
                    slot.amount = 0
                    slot.type = None
                    self.notify()
                    continue
                elif slot.amount == amount:
                    in_invent += amount
                    slot.amount = 0
                    slot.type = None
                    self.notify()
                    return in_invent
                else:
                    in_invent += amount #?
                    slot.amount -= amount
                    self.notify()
                    return in_invent
        return in_invent
    
# verifier si l'objet demandé est suffisant par rapport à une quantité specifique 
    def has (self, item_type, amount = 1):
        in_invent = 0 
        for slot in self.slots:
            if slot.type == item_type:
                in_invent += slot.amount
                if in_invent>=amount:
                    return True
        return False
    
    def __str__ (self):
        pass

    def full_space(self):
        pass
    
    def weight (self):
        pass

    def value (self):
        pass

    
#item ramassable 
class Droppeditem:
    pass