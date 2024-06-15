import pygame
import textwrap 
from item import *  
from entity import *  

class Inventory:
    """
    Représente l'inventaire du joueur dans le jeu.

    Attributs :
        items (list): Liste des objets actuellement dans l'inventaire.
        item_rects (list): Liste des rectangles d'affichage pour chaque objet dans l'interface.
        player (Player): Le joueur associé à cet inventaire.

    Méthodes :
        __init__():
            Initialise un inventaire vide et ajoute des exemples d'objets pour test.

        add_item(item):
            Ajoute un item à l'inventaire.

        remove_item(item):
            Retire un item de l'inventaire s'il existe.

        handle_click(mouse_pos):
            Gère les clics de souris sur les objets de l'inventaire, renvoyant l'objet cliqué.

        use_item(item, player):
            Utilise un item sur le joueur, activant ses effets spécifiques.

        show_inventory(screen, font, WIDTH):
            Affiche l'inventaire à l'écran avec les noms des objets formatés.

        save_inventory():
            Sérialise l'inventaire pour sauvegarde.

        load_inventory(items_data):
            Désérialise et charge les objets depuis des données sauvegardées.
    """
    def __init__(self):
        """
        Initialise un inventaire vide et ajoute des exemples d'objets pour test.
        """
        self.items = []  # Liste des items dans l'inventaire
        self.item_rects = []  # Liste des rectangles d'affichage des items
        self.player = Player(0,0)  # Le joueur associé à l'inventaire
        # Ajout d'exemples d'items pour test
        self.items.append(apple)
        self.items.append(berry)

    def add_item(self, item):
        """
        Ajoute un item à l'inventaire.

        Args:
            item (Item): L'objet à ajouter.
        """
        self.items.append(item)

    def remove_item(self, item):
        """
        Retire un item de l'inventaire s'il existe.

        Args:
            item (Item): L'objet à retirer.
        """
        if item in self.items:
            self.items.remove(item)
    
    def handle_click(self, mouse_pos):
        """
        Gère les clics de souris sur les objets de l'inventaire.

        Args:
            mouse_pos (tuple): Coordonnées (x, y) du clic de souris.

        Returns:
            Item or None: L'item cliqué ou None s'il n'y a aucun item cliqué.
        """
        if not self.items:
            print("Inventaire vide")
            return None
        for rect, item in self.item_rects:
            if rect.collidepoint(mouse_pos):
                print(f"J'ai cliqué sur {item.nom}")
                return item
        return None
            
    def use_item(self, item, player):
        """
        Utilise un item sur le joueur, activant ses effets spécifiques.

        Args:
            item (Item): L'objet à utiliser.
            player (Player): Le joueur sur lequel appliquer l'effet de l'item.
        """
        if isinstance(item, Healer):
            item.healing(player)
        elif isinstance(item, Booster):
            item.boost(player)
              
    def show_inventory(self, screen, font, WIDTH):
        """
        Affiche l'inventaire à l'écran avec les noms des objets formatés.

        Args:
            screen (pygame.Surface): Surface de la fenêtre du jeu où dessiner.
            font (pygame.font.Font): Police utilisée pour le rendu du texte.
            WIDTH (int): Largeur de la fenêtre du jeu.
        """
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

        self.item_rects.clear()  # Efface la liste des rectangles d'items avant de dessiner

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
        """
        Sérialise l'inventaire pour sauvegarde.

        Returns:
            list: Liste des données sérialisées des objets.
        """
        return [item.serialize() for item in self.items]

    def load_inventory(self, items_data):
        """
        Désérialise et charge les objets depuis des données sauvegardées.

        Args:
            items_data (list): Liste des données sérialisées des objets.
        """
        self.items = []
        for item_data in items_data:
            item_type = item_data.pop('type')
            if item_type == 'Healer':
                item = Healer.deserialize(item_data)
            elif item_type == 'Booster':
                item = Booster.deserialize(item_data)
            self.items.append(item)
