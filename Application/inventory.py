import pygame  # Bibliothèque pour créer des jeux vidéo en utilisant Python
import textwrap  # Bibliothèque pour manipuler le texte, notamment pour le retour à la ligne
from item import *  # Importation des classes ou fonctions définies dans le fichier item.py
from entity import *  # Importation des classes ou fonctions définies dans le fichier entity.py

class Inventory:
    def __init__(self):
        self.items = []  # Initialise une liste vide pour stocker les items de l'inventaire
        self.item_rects = []

        self.player = Player(0,0)
        #Test pour voir si les objets sont bien ajoutés à l'inventaire
        
        self.items.append(police)
        self.items.append(apple)
        


    def add_item(self, item):
        self.items.append(item)  # Ajoute un item à l'inventaire

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
    
    def handle_click(self, mouse_pos):
        for rect, item in self.item_rects:
            if rect.collidepoint(mouse_pos):
                print(f"j'ai cliqué sur {item.nom}")
                self.use_item(item, self.player)
                self.remove_item(item)
                
                    
   
    def use_item(self, item, player):
        if isinstance(item, Healer) and item.nom in ["Pomme", "Baie"]:
            item.healing(player)
        elif isinstance(item, Booster) and item.nom in ["Police", "Militaire"]:
            item.boost(player)
   
          
    def show_inventory(self, screen, font, WIDTH):
        small_font = pygame.font.Font(None, 24) 
        
        
        inventory_surface = pygame.Surface((300, 400), pygame.SRCALPHA)
        inventory_surface.fill((50, 50, 50, 128)) 
        
        
        title = font.render("Inventaire", True, (255, 255, 255))  
        title_rect = title.get_rect(topleft=(550, 20))
        screen.blit(title, title_rect)
        
       
        if not self.items:
            empty_text = small_font.render("Inventaire vide ", True, (255, 255, 255))
            inventory_surface.blit(empty_text, (10, 10))
            screen.blit(inventory_surface, (WIDTH - 310, 80))
            return

        
        rows = 8
        cols = (len(self.items) + rows - 1) // rows  
        cell_width = 300 // cols  
        cell_height = 400 // rows  

        self.item_rects.clear()  # Clear the item rectangles list before drawing new ones

        for i, item in enumerate(self.items):
            row = i % rows
            col = i // rows
            
            
            item_text_lines = textwrap.wrap(f"{item.nom}", width=20)

            y_offset = row * cell_height + 10  
            x_offset = col * cell_width + 10  
            
            for line in item_text_lines:
                item_text = small_font.render(line, True, (255, 255, 255))
                text_rect = item_text.get_rect(topleft=(x_offset + 5, y_offset))

                inventory_surface.blit(item_text, text_rect)
                y_offset += text_rect.height + 5  

            
            row_rect = pygame.Rect(x_offset, row * cell_height, 300, cell_height)
            pygame.draw.rect(inventory_surface, (255, 255, 255), row_rect, 2)
            self.item_rects.append((row_rect.move(WIDTH - 310, 80), item))
        
        screen.blit(inventory_surface, (WIDTH - 310, 80))
            
    

    
    def save_inventory(self):
        return [item.serialize() for item in self.items]

    def load_inventory(self, items_data):
        self.items = []
        for item_data in items_data:
            item_type = item_data.pop('type')
            if item_type == 'Healer':
                item = Healer.deserialize(item_data)
            elif item_type == 'Booster':
                item = Booster.deserialize(item_data)
            self.items.append(item)

