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
