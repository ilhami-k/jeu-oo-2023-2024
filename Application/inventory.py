import pygame
from item import *

class Inventory:
    def __init__(self):
        self.items = []
        
        # Test pour voir si les objets sont bien ajoutés à l'inventaire
        # self.items.append(appel)
        # self.items.append(berry)

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
        else:
            print(f"{item} n'est pas dans l'inventaire.")
   
    
    def show_inventory(self, screen, font, WIDTH):
                #affichage de la surface
                inventory_surface = pygame.Surface((300, 400), pygame.SRCALPHA)  # Créez une surface pour l'inventaire
                inventory_surface.fill((50, 50, 50, 128))  # Remplissez la surface avec une couleur de fond
                y_offset = 20

                #affichage du titre 
                title = font.render("Inventory", True, (255, 255, 255))  # Blanc
                title_rect = title.get_rect(center=(WIDTH / 2, 50))
                screen.blit(title, title_rect)

                # Affichez chaque item dans l'inventaire
                for item in self.items:
                    item_text = font.render(f"{item.nom}: {item.info}", True, (255, 255, 255))
                    inventory_surface.blit(item_text, (20, y_offset))
                    y_offset += 40

                # Blittez l'inventaire sur l'écran principal
                screen.blit(inventory_surface, (WIDTH - 310, 10))  # Positionnez