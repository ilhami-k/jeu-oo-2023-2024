import pygame
import sys
from settings import *

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

