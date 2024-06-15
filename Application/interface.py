import pygame
from settings import *
from game import *
from save_system import SaveSystem
import textwrap
class Button:
    def __init__(self, x, y, width, height, foreground=(255, 255, 255, 255), background=(0, 0, 0, 256), content=None, fontsize=36):
        """
        Initialise un bouton avec les paramètres spécifiés.

        Args:
            x (int): La position x du coin supérieur gauche du bouton.
            y (int): La position y du coin supérieur gauche du bouton.
            width (int): La largeur du bouton.
            height (int): La hauteur du bouton.
            foreground (tuple): La couleur du texte (R, G, B, A). Par défaut est blanc opaque (255, 255, 255, 255).
            background (tuple): La couleur de fond du bouton (R, G, B, A). Par défaut est noir transparent (0, 0, 0, 256).
            content (str): Le texte à afficher sur le bouton. Par défaut est None.
            fontsize (int): La taille de la police du texte. Par défaut est 36.
        """
        self.font = pygame.font.Font('freesansbold.ttf', fontsize)
        self.content = content
        
        self.x = x
        self.y = y 
        self.background = background
        self.width = width
        self.height = height
        
        self.foreground = foreground
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect() 
        self.rect.x = self.x
        self.rect.y = self.y
        self.image.fill(self.background)
        self.text_surface = self.font.render(self.content, True, self.foreground)
        self.text_rect = self.text_surface.get_rect(center=(self.width/2, self.height/2))

        self.image.blit(self.text_surface, self.text_rect)
    
    def is_pressed(self, pos, pressed):
        """Regarde si le clic gauche est appuyé (c'est index 0 sur la liste des commandes)"""
        if self.rect.collidepoint(pos) and pressed[0]:
            return True
        return False


class DialogueBox:
    def __init__(self, text, font_size=24, width=600, height=200, x=100, y=100, bg_color=(255, 255, 255, 255), text_color=(255, 255, 255)):
        """
        Initialise une boîte de dialogue avec les paramètres spécifiés.

        Args:
            text (str): Le texte à afficher dans la boîte de dialogue.
            font_size (int): La taille de la police du texte. Par défaut est 24.
            width (int): La largeur de la boîte de dialogue. Par défaut est 600.
            height (int): La hauteur de la boîte de dialogue. Par défaut est 200.
            x (int): La position x du coin supérieur gauche de la boîte de dialogue. Par défaut est 100.
            y (int): La position y du coin supérieur gauche de la boîte de dialogue. Par défaut est 100.
            bg_color (tuple): La couleur de fond de la boîte de dialogue (R, G, B, A). Par défaut est blanc opaque (255, 255, 255, 255).
            text_color (tuple): La couleur du texte (R, G, B). Par défaut est blanc (255, 255, 255).
        """
        self.text = text
        self.font_size = font_size
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.bg_color = bg_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, self.font_size)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        """
        Dessine la boîte de dialogue sur l'écran spécifié.
        Args:
            screen (pygame.Surface): La surface de l'écran où dessiner la boîte de dialogue.
        """
        dialog_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(dialog_surface, self.bg_color, dialog_surface.get_rect(), border_radius=10)
        screen.blit(dialog_surface, (self.x, self.y))
        
        lines = self.wrap_text(self.text, self.font, self.width)
        y_offset = self.y + 20
        for line in lines:
            text_surface = self.font.render(line, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.x + self.width // 2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += self.font_size + 5

    def wrap_text(self, text, font, max_width):
        """
        Enveloppe le texte pour qu'il s'adapte à la largeur maximale spécifiée.
        Args:
            text (str): Le texte à envelopper.
            font (pygame.font.Font): La police utilisée pour rendre le texte.
            max_width (int): La largeur maximale que le texte doit occuper.

        Returns:
            list: Une liste de lignes de texte qui tiennent dans la largeur spécifiée.
        """
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + ' ' + word if current_line != '' else word
            if font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines
class Npc_Dialogues:
    def __init__(self, messages, font_size, width, height, x, y, bg_color, text_color):
        """
        Initialise un système de dialogues pour un NPC (Personnage Non Joueur) avec les paramètres spécifiés.

        Args:
            messages (list): Liste de tuples contenant le nom du locuteur et le message (ex. [('npc', 'Bonjour!'), ('player', 'Salut!')]).
            font_size (int): La taille de la police du texte.
            width (int): La largeur de la boîte de dialogue.
            height (int): La hauteur de la boîte de dialogue.
            x (int): La position x du coin supérieur gauche de la boîte de dialogue.
            y (int): La position y du coin supérieur gauche de la boîte de dialogue.
            bg_color (tuple): La couleur de fond de la boîte de dialogue (R, G, B, A).
            text_color (tuple): La couleur du texte du NPC (R, G, B).
        """
        self.font = pygame.font.Font(None, font_size)
        self.messages = messages
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.bg_color = bg_color
        self.text_color = text_color
        self.index = 0

    def draw(self, screen):
        """
        Dessine la boîte de dialogue sur l'écran spécifié et affiche le message actuel.

        Args:
            screen (pygame.Surface): La surface de l'écran où dessiner la boîte de dialogue.
        """
        pygame.draw.rect(screen, self.bg_color, (self.x, self.y, self.width, self.height), border_radius=10)
        if self.index < len(self.messages):
            speaker, message = self.messages[self.index]
            color = self.text_color if speaker == 'npc' else (0, 0, 0)
            speaker_text = "Brançois Furniaux" if speaker == 'Brançois Furniaux' else "Billy"
            header_surface = self.font.render(speaker_text, True, (0, 0, 0))
            header_rect = header_surface.get_rect(center=(self.x + self.width // 2, self.y + 10))
            screen.blit(header_surface, header_rect)
            wrapped_lines = textwrap.wrap(message, width=int(self.width / 10))
            y_offset = 50
            for line in wrapped_lines:
                text_surface = self.font.render(line, True, color)
                text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + y_offset))
                screen.blit(text_surface, text_rect)
                y_offset += self.font.get_height() + 5

    def next_message(self):
        """
        Passe au message suivant dans la liste des messages.

        Returns:
            bool: Retourne True si le message a été avancé, sinon False.
        """
        if self.index < len(self.messages) - 1:
            self.index += 1
            print(f"Advancing to message index: {self.index}")
            return True
        print("No more messages to advance to")
        return False

    def reset(self):
        """
        Réinitialise l'index des messages à zéro.
        """
        self.index = 0


class Interface:
    def __init__(self, player, prologue_on, new_game):
        """
        Initialise l'interface du jeu avec les paramètres spécifiés.

        Args:
            player (Player): L'objet joueur représentant le joueur.
            prologue_on (bool): Indique si le prologue est actif.
            new_game (bool): Indique si une nouvelle partie est lancée.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.intro_background = pygame.image.load("../Application/images/background.png")
        self.new_game = new_game
        self.prologue_on = prologue_on
        self.epilogue_on = False
        self.save_load = SaveSystem('.json', '../Application/save_data/')
        self.player = player
        self.end_background = pygame.image.load("../Application/images/background.png")

    def prologue(self):
        """
        Affiche l'écran du prologue et gère les événements associés.
        
        Returns:
            bool: Retourne l'état de fonctionnement du jeu (True si le jeu continue, False sinon).
        """
        self.prologue_on = True
        self.death = False

        while self.prologue_on:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.prologue_on = False
                if event.type == pygame.QUIT:
                    self.prologue_on = False
                    self.running = False
                    return self.running
            
            self.screen.fill((0, 0, 0))
            prologue_box = DialogueBox(PROLOGUE_STORY , 24, 700, 300, 50, HEIGHT - 350, (255, 255, 128, 128), (0, 0, 0))
            prologue_box.draw(self.screen)
            press_enter_box = DialogueBox("Appuyez sur Entrée pour continuer...", 22, 300, 50, WIDTH / 2 - 150, HEIGHT - 50, (255, 255, 255), (0, 0, 0))
            press_enter_box.draw(self.screen)
            pygame.display.update()

    def ending_screen(self):
        """
        Affiche l'écran de fin et gère les événements associés.
        
        Returns:
            bool: Retourne l'état de fonctionnement du jeu (True si le jeu continue, False sinon).
        """
        self.ending = True
        title = self.font.render("Vous avez terminé le jeu", True, 'White')
        title_rect = title.get_rect(center=(WIDTH / 2, HEIGHT / 4))
        exit_button = Button(WIDTH / 2 - 100, HEIGHT / 2 - 100, 200, 50, (255, 255, 255), (0, 0, 0), "Exit", 36)
        while self.ending:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.ending = False
                    self.running = False
                    return self.running
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if exit_button.is_pressed(mouse_pos, mouse_pressed):
                self.ending = False
                self.running = False
                return self.running
            stretched_image = pygame.transform.scale(self.intro_background, (800, 1000))
            self.screen.blit(stretched_image, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(exit_button.image, exit_button.rect)
            ending_box = DialogueBox(ENDING_STORY,24, 700, 300, 50, HEIGHT - 350, (255, 255, 128, 128), (255, 255, 255))
            ending_box.draw(self.screen)
            pygame.display.update()
