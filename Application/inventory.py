import pygame  # Bibliothèque pour créer des jeux vidéo en utilisant Python
import textwrap  # Bibliothèque pour manipuler le texte, notamment pour le retour à la ligne
from item import *  # Importation des classes ou fonctions définies dans le fichier item.py

class Inventory:
    def __init__(self):
        self.items = []  # Initialise une liste vide pour stocker les items de l'inventaire
        
        # Test pour voir si les objets sont bien ajoutés à l'inventaire
        # self.items.append(appel)
        # self.items.append(berry)

    def add_item(self, item):
        self.items.append(item)  # Ajoute un item à l'inventaire

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)  # Retire l'item de l'inventaire s'il est présent
        else:
            print(f"{item} n'est pas dans l'inventaire.")  # Message si l'item n'est pas trouvé


    def show_inventory(self, screen, font, WIDTH):
        small_font = pygame.font.Font(None, 24)  # Définit une police plus petite pour les items de l'inventaire
        
        # Crée une surface pour l'inventaire
        inventory_surface = pygame.Surface((300, 400), pygame.SRCALPHA)
        inventory_surface.fill((50, 50, 50, 128))  # Remplit la surface avec une couleur de fond semi-transparente
        y_offset = 20  # Initialisation de l'offset vertical pour l'affichage des items

        # Affichage du titre "Inventory" au centre du haut de l'inventaire
        title = font.render("Inventory", True, (255, 255, 255))  # Rend le texte en blanc
        title_rect = title.get_rect(center=(WIDTH / 2, 50))
        screen.blit(title, title_rect)

                #affichage du titre 
                title = font.render("Inventaire", True, (255, 255, 255))  # Blanc
                title_rect = title.get_rect(center=(WIDTH / 2, 50))
                screen.blit(title, title_rect)

                #gestion de l'affichage du texte des items
                item_font = pygame.font.Font(None, 20)

                # Affichez chaque item dans l'inventaire
                for item in self.items:
                    item_text = item_font.render(f"{item.nom}: {item.info}", True, (255, 255, 255))
                    inventory_surface.blit(item_text, (20, y_offset))
                    y_offset += 40
                
                

        # Affiche chaque item dans l'inventaire
        for item in self.items:
            # Divise le texte de l'item en plusieurs lignes si nécessaire pour s'adapter à la largeur de 35 caractères
            item_text_lines = textwrap.wrap(f"{item.nom}: {item.info}", width=35)
            for line in item_text_lines:
                item_text = small_font.render(line, True, (255, 255, 255))  # Rend chaque ligne de texte en blanc
                inventory_surface.blit(item_text, (20, y_offset))  # Affiche la ligne de texte sur la surface de l'inventaire
                y_offset += 20  # Ajoute un espace vertical entre les lignes
            
        # Affiche la surface de l'inventaire sur l'écran principal
        screen.blit(inventory_surface, (WIDTH - 310, 10))  # Positionne l'inventaire dans le coin supérieur droit
