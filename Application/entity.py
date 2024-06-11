import pygame
import math
from settings import *
from bullet import *
from game import *
from interface import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, name, speed, health, attack_cooldown=0, damage=0):
        super().__init__()
        self.name = name 
        self.position = [x, y]
        self.old_position = self.position.copy()   
        self.sprite_sheet = pygame.image.load(image_path)
        self.image = self.get_image(48, 0)
        self.image.set_colorkey((0, 0, 0))  
        self.rect = self.image.get_rect()
        self.speed = speed
        self.health = health
        self.attack_cooldown = attack_cooldown
        self.damage = damage

    def get_image(self, x, y):
        image = pygame.Surface((16, 24))  # Réduire la hauteur de 8 pixels de l'image
        image.blit(self.sprite_sheet, (0, -8), (x, y, 16, 32))  # Déplacer le contenu de l'image de 8 pixels vers le bas pour ne pas perdre la réduction réaluisée juste avant
        return image

    def save_location(self):
        self.old_position = self.position.copy()

    def move_back(self): 
        self.position = self.old_position.copy()
        self.rect.topleft = self.position
        
    def move(self, x, y):
        # Réduire la vitesse de déplacement en diagonale (A vérifier si ca fonctionne bien)
        if x != 0 and y != 0:
            x *= math.sqrt(2) / 2
            y *= math.sqrt(2) / 2 
        self.position[0] += x
        self.position[1] += y

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()  # Supprimer la spirte de l'ennemi du groupe

    def update(self, player):
        self.rect.topleft = self.position

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "Application/images/Player.png", 'Player', PLAYER_SPEED, PLAYER_HEALTH, ATTACK_COOLDOWN, PLAYER_SHOOT_DAMAGE)
        self.max_health = PLAYER_MAX_HEALTH
        self.bullet_type = BasicBullet
        

    def shoot(self, target_x, target_y, bullet_group):
        angle = math.atan2(target_y - self.position[1], target_x - self.position[0])
        center_x = self.position[0] + self.rect.width / 2
        center_y = self.position[1] + self.rect.height / 2
        bullet_group.add(self.bullet_type(center_x, center_y, angle))

    def cooldown_tick(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
  
    
    #gestion de l'apparence de la barre de vie du joueur 
    def update_healthbar (self, screen):
        #couleur de la barre de vie 
        bar_color = (85,209,70)
        #couleur de fond de barre
        bar_fond_color = (255,95,65)
        #position de la barre 
        bar_position = [15, 15, self.health, 10]
        #position de l'arriere plan de la barre 
        bar_fond_position = [15, 15, self.max_health, 10]

        #affichage de l'arriere plan
        pygame.draw.rect(screen, bar_fond_color, bar_fond_position)
        #afficher la barre de vie 
        pygame.draw.rect(screen, bar_color, bar_position)
    
class Enemy(Entity):
    def update(self, player):
        # Calculer la direction vers le joueur
        direction_x = player.position[0] - self.position[0]
        direction_y = player.position[1] - self.position[1]
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        # Déplacer l'ennemi dans la direction du joueur
        self.move(direction_x * self.speed, direction_y * self.speed)

        # Vérifier les collisions avec le joueur
        # if self.rect.colliderect(player.rect):
        #     self.attack(player, self.damage)

        # Gérer le temps entre les attaques
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # Mettre à jour la position du rectangle de collision
        self.rect.topleft = self.position

    def attack(self, player, damage):
        # Vérifier si l'ennemi peut attaquer
        if self.attack_cooldown == 0:
            # Infliger des dégâts au joueur
            player.take_damage(damage)
            # Réinitialiser le cooldown d'attaque
            self.attack_cooldown = self.initial_attack_cooldown

class Zombie(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "Application/images/Zombie.png", 'Zombie', ZOMBIE_SPEED, ZOMBIE_HEALTH, ZOMBIE_ATTACK_COOLDOWN, ZOMBIE_DAMAGE)
        self.initial_attack_cooldown = ZOMBIE_ATTACK_COOLDOWN

class Skeleton(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "Application/images/Skeleton.png", 'Skeleton', SKELETON_SPEED, SKELETON_HEALTH, SKELETON_ATTACK_COOLDOWN, SKELETON_DAMAGE)
        self.initial_attack_cooldown = SKELETON_ATTACK_COOLDOWN

class Nohead(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "Application/images/Nohead.png", 'Nohead', NOHEAD_SPEED, NOHEAD_HEALTH, NOHEAD_ATTACK_COOLDOWN, NOHEAD_DAMAGE)
        self.initial_attack_cooldown = NOHEAD_ATTACK_COOLDOWN

class Golem(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "Application/images/Golem.png", 'Golem', GOLEM_SPEED, GOLEM_HEALTH, GOLEM_ATTACK_COOLDOWN, GOLEM_DAMAGE)
        self.initial_attack_cooldown = GOLEM_ATTACK_COOLDOWN
        self.image = self.get_image(0, 0)
        self.image.set_colorkey((0, 0, 0))

    def get_image(self, x, y):
        image = pygame.Surface((67, 69))
        image.blit(self.sprite_sheet, (0, 0), (x, y, 67, 69))
        return image
    
    def rage(self):
        if self.health <= GOLEM_HEALTH / 2:
            self.speed = GOLEM_SPEED * 2
            self.damage = GOLEM_DAMAGE * 4

    def shoot_all_directions(self, bullet_group):
        for angle in range(0, 360, 45):  # Tirer dans 8 directions (0, 45, 90, ..., 315 degrés)
            rad_angle = math.radians(angle)
            boss_center_x = self.position[0] + self.rect.width / 2
            boss_center_y = self.position[1] + self.rect.height / 2
            bullet_group.add(BossBullet(boss_center_x,boss_center_y, rad_angle))

class Npc(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "Application/images/NPC.png", 'npc', NPC_SPEED, NPC_HEALTH, NPC_ATTACK_COOLDOWN)
        self.interaction_range = 50
        self.dialogue_box = None
        

    def interact(self, player,dialogue):
        self.dialogue = dialogue
        if self.in_interaction_range(player):
            self.dialogue_box = Npc_Dialogues(self.dialogue, 22, 700, 150, 50, HEIGHT - 250, (255, 255, 128, 128), (0, 0, 0))
            return True
        return False

    def in_interaction_range(self, player):
        distance = math.sqrt((self.position[0] - player.position[0]) ** 2 + (self.position[1] - player.position[1]) ** 2)
        return distance <= self.interaction_range

    def draw_dialogue_box(self, screen):
    
        if self.dialogue_box:
            self.dialogue_box.draw(screen)

    def close_dialogue_box(self):
        self.dialogue_box = None

    def advance_dialogue(self):
        if self.dialogue_box:
            if not self.dialogue_box.next_message():
                self.close_dialogue_box()

                print("Dialogue closed")
                return False
        return True



