import pygame  # Bibliothèque pour créer des jeux vidéo en utilisant Python
import textwrap  # Bibliothèque pour manipuler le texte, notamment pour le retour à la ligne
from item import *  # Importation des classes ou fonctions définies dans le fichier item.py
from entity import *  # Importation des classes ou fonctions définies dans le fichier entity.py

class Inventory:
    def __init__(self):
        self.items = []  # Initialise une liste vide pour stocker les items de l'inventaire
        self.item_rects = []
        self.hover_item = None
        self.player = Player(0, 0)


        #Test pour voir si les objets sont bien ajoutés à l'inventaire
        self.items.append(appel)
        self.items.append(military)

    def add_item(self, item):
        self.items.append(item)  # Ajoute un item à l'inventaire

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)  # Retire l'item de l'inventaire s'il est présent
        else:
            print(f"{item} n'est pas dans l'inventaire.")  # Message si l'item n'est pas trouvé

    def handle_click(self, mouse_pos):
        for rect, item in self.item_rects:
            if rect.collidepoint(mouse_pos):
               self.use_item(item)
    
    def use_item(self, item):
         self.remove_item(item)



    def show_inventory(self, screen, font, WIDTH):
        self.item_rects.clear()
        small_font = pygame.font.Font(None, 20)  # Définit une police plus petite pour les items de l'inventaire
        
        # Crée une surface pour l'inventaire
        inventory_surface = pygame.Surface((300, 400), pygame.SRCALPHA)
        inventory_surface.fill((50, 50, 50, 128))  # Remplit la surface avec une couleur de fond semi-transparente
        y_offset = 20  # Initialisation de l'offset vertical pour l'affichage des items

        #affichage du titre 
        title = font.render("Inventaire", True, (255, 255, 255))  # Blanc
        title_rect = title.get_rect(center=(WIDTH / 2, 20))
        screen.blit(title, title_rect)

        # Affiche chaque item dans l'inventaire
        for item in self.items:
            # Divise le texte de l'item en plusieurs lignes si nécessaire pour s'adapter à la largeur de 35 caractères
            item_text_lines = textwrap.wrap(f"{item.nom}: {item.info}", width=35)
            for line in item_text_lines:
                color = (255,255,255) if item != self.hover_item else (255,0,0)
                item_text = small_font.render(line, True, color)  # Rend chaque ligne de texte en blanc
                text_rect = item_text.get_rect(topleft=(20, y_offset))
                inflated_rect = text_rect.inflate(10,10)

                # crée une surface pour chaque item
                item_surface = pygame.Surface((inflated_rect.width, inflated_rect.height))
                item_surface.fill((0,0,0))
                pygame.draw.rect(item_surface, (255,255,255), item_surface.get_rect(), 2)
                item_surface.blit(item_text, (5,5))
                #pygame.draw.rect(inventory_surface, (0,0,0), text_rect.inflate(10,10), 2)
                inventory_surface.blit(item_surface, (10, y_offset))
                self.item_rects.append((pygame.Rect((WIDTH - 310 + 20, 10 + y_offset), item_surface.get_size()), item))
                y_offset += inflated_rect.height + 10
            
        # Affiche la surface de l'inventaire sur l'écran principal
        screen.blit(inventory_surface, (WIDTH - 310, 10))  # Positionne l'inventaire dans le coin supérieur droit
    def item(self):
        list_items = self.items
        return list_items #pour pouvoir sauvegarder l'inventaire
