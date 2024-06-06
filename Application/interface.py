import pygame
import sys
from settings import *
from game import *
from save_system import SaveSystem
class Button: 
    def __init__(self, x, y, width, height, foreground,background,content,fontsize):
        self.font = pygame.font.Font('freesansbold.ttf', fontsize)
        self.content = content
        
        self.x = x
        self.y = y 
        
        self.width = width
        self.height = height
        
        self.foreground = foreground
        self.background = background
        
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.background)
        self.rect = self.image.get_rect()
        
        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.foreground)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)


    
    def is_pressed(self,pos,pressed):
        if self.rect.collidepoint(pos) and pressed[0]: #[0] car premier bouton de la liste
            return True
        return False


class DialogueBox:
    def __init__(self, text, font_size=24, width=600, height=200, x=100, y=100, bg_color=(255, 255, 255, 255), text_color=(255, 255, 255)):
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
        # Create a surface for the dialogue box
        dialog_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Draw a semi-transparent background rectangle
        pygame.draw.rect(dialog_surface, self.bg_color, dialog_surface.get_rect(), border_radius=10)
        
        # Blit the dialogue box surface onto the screen
        screen.blit(dialog_surface, (self.x, self.y))
        
        # Render and blit the text onto the dialogue box
        lines = self.wrap_text(self.text, self.font, self.width)
        y_offset = self.y + 20  # Starting position for text
        for line in lines:
            text_surface = self.font.render(line, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.x + self.width // 2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += self.font_size + 5  # Adjust vertical spacing


    def wrap_text(self, text, font, max_width):
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
class Interface:
    def __init__(self,player,prologue_on,new_game):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.intro_background = pygame.image.load("Application/background.png")
        self.new_game = False
        self.prologue_on = False
        self.epilogue_on = False
        self.save_load = SaveSystem('.json','Application/save_data/')
        self.player = player

        self.prologue_on = prologue_on
        self.new_game = new_game
    def menu_screen(self):
        menu = True
        title = self.font.render("Menu", True, 'Black')
        title_rect = title.get_rect(center=(WIDTH/2, HEIGHT/4))
        continue_button = Button(WIDTH/2 - 100, HEIGHT/2 - 150, 200, 50, (255, 255, 255), (0, 0, 0), "Continue", 36)
        save_game = Button(WIDTH/2 - 100, HEIGHT/2 -50 , 200, 50, (255, 255, 255), (0, 0, 0), "Save game", 36)
        exit_button = Button(WIDTH/2 - 100, HEIGHT/2 + 50, 200, 50, (255, 255, 255), (0, 0, 0), "Exit", 36)
        

        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if continue_button.is_pressed(mouse_pos, mouse_pressed):
                menu = False
            if save_game.is_pressed(mouse_pos, mouse_pressed):
                self.game_state.save_game_state()
            if exit_button.is_pressed(mouse_pos, mouse_pressed):
                menu = False
                self.running = False
                return self.running
            
            stretched_image = pygame.transform.scale(self.intro_background,(800,1000))
            self.screen.blit(stretched_image, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(continue_button.image, continue_button.rect)
            self.screen.blit(save_game.image, save_game.rect)
            self.screen.blit(exit_button.image, exit_button.rect)
            
            pygame.display.update()
    def prologue(self):
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
            
            
            self.screen.fill((0,0,0))
            prologue_box = DialogueBox("Il était une fois, dans un monde lointain, un jeune aventurier qui partit à la recherche de trésors cachés. Il se nommait Arthur et était connu pour sa bravoure et sa témérité. Un jour, alors qu'il explorait une grotte mystérieuse, il découvrit une carte ancienne indiquant l'emplacement d'un trésor légendaire. Arthur décida de partir à la recherche de ce trésor, mais il ne savait pas encore qu'il allait devoir affronter de nombreux dangers et énigmes pour parvenir à ses fins.", 22, 700, 150, 50, HEIGHT - 250, (255, 255, 128,128), (0, 0, 0))
            prologue_box.draw(self.screen)
            #  def __init__(self, text, font_size=24, width=600, height=200, x=100, y=100, bg_color=(255, 255, 255), text_color=(0, 0, 0)):
            press_enter_box = DialogueBox("Appuyez sur Entrée pour continuer...", 22, 300, 50, WIDTH/2 - 150, HEIGHT - 50, (255, 255, 255), (0, 0, 0))
            press_enter_box.draw(self.screen)
            pygame.display.update()
        
