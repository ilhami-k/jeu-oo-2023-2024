import pygame
import math
from settings import *
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites):
        super().__init__()
        
        # Création de l'image du joueur (un carré rouge)
        self.sprite_sheet = pygame.image.load("Application/Player.png")
        self.image = self.get_image(48, 0)
        self.image.set_colorkey((0, 0, 0))  # Définir la couleur de transparence
        self.rect = self.image.get_rect()

        # Position initiale du joueur
        self.position = [x, y]
        self.old_position = self.position.copy()  # Pour sauvegarder la position précédente
        self.speed = PLAYER_SPEED  # Vitesse de déplacement du joueur
        
        # Délai de rechargement entre chaque tir
        self.shoot_cooldown = 0

        # Couleur du rectangle de collision
        self.rect_color = (0, 255, 0)  # Vert par exemple

    # Création de la méthode get_image pour obtenir une image à partir de la feuille de sprites
    def get_image(self, x, y):
        image = pygame.Surface((16, 32))
        image.blit(self.sprite_sheet, (0, 0), (x, y, 16, 32))
        return image

    def save_location(self):
        """Sauvegarde la position actuelle du joueur."""
        self.old_position = self.position.copy()

    def move_back(self):
        """Revenir à la position précédente en cas de collision."""
        self.position = self.old_position.copy()
        self.rect.topleft = self.position

    def move(self, x, y):
        """Déplacer le joueur."""
        # Si le joueur se déplace en diagonale, ajuster la vitesse
        if x != 0 and y != 0:
            x *= math.sqrt(2) / 2
            y *= math.sqrt(2) / 2

        self.position[0] += x
        self.position[1] += y

        # Mettre à jour les coordonnées du carré rouge
        self.rect.x = int(self.position[0])
        self.rect.y = int(self.position[1]) 
    
    def update(self):
        """Mettre à jour la position du joueur."""
        self.rect.topleft = self.position

    def shoot(self, target_x, target_y, bullet_group):
        """Tirer une balle vers la position cible."""
        angle = math.atan2(target_y - self.position[1], target_x - self.position[0])
        # Utilise les coordonnées du centre du joueur comme position initiale pour les balles
        bullet_group.add(Bullet(self.rect.centerx, self.rect.centery, angle))

    def cooldown_tick(self):
        """Réduire le délai de rechargement."""
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def draw_collision_rect(self, surface):
        """Dessine le rectangle de collision sur la surface donnée."""
        pygame.draw.rect(surface, self.rect_color, self.rect, 2)  # Dessine le rectangle avec une couleur et une épaisseur de ligne de 2 pixels
