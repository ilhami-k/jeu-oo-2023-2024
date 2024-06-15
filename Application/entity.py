import pygame
import math
from settings import *
from bullet import *
from game import *
from interface import *

class Entity(pygame.sprite.Sprite):
    """
    Classe de base représentant une entité dans le jeu.

    Attributs:
        position: Liste [x, y] représentant les coordonnées de l'entité sur l'écran.
        old_position: Anciennes coordonnées de l'entité avant le dernier déplacement.
        sprite_sheet: Surface contenant la feuille de sprites de l'entité.
        image: Image actuellement affichée de l'entité.
        rect: Rectangle de collision de l'entité pour la détection de collisions.
        speed: Vitesse de déplacement de l'entité.
        health: Points de vie actuels de l'entité.
        attack_cooldown: Délai de recharge entre les attaques de l'entité.
        damage: Dommages infligés par l'entité lors d'une attaque.

    Méthodes:
        get_image(x, y): Récupère une portion spécifique de l'image de l'entité.
        save_location(): Sauvegarde la position actuelle de l'entité.
        move_back(): Rétablit la position précédente de l'entité.
        move(x, y): Déplace l'entité selon les coordonnées spécifiées.
        take_damage(damage): Réduit les points de vie de l'entité en fonction des dégâts reçus.
        update(player): Met à jour la position de l'entité et gère les actions en fonction du joueur.
    """
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
            self.kill()  

    def update(self, player):
        self.rect.topleft = self.position

class Player(Entity):
    """
    Classe représentant le joueur dans le jeu.

    Hérite de la classe Entity.

    Attributs hérités de Entity :
        - position: Liste [x, y] représentant les coordonnées du joueur sur l'écran.
        - old_position: Anciennes coordonnées du joueur avant le dernier déplacement.
        - sprite_sheet: Surface contenant la feuille de sprites du joueur.
        - image: Image actuellement affichée du joueur.
        - rect: Rectangle de collision du joueur pour la détection de collisions.
        - speed: Vitesse de déplacement du joueur.
        - health: Points de vie actuels du joueur.
        - attack_cooldown: Délai de recharge entre les attaques du joueur.
        - damage: Dommages infligés par le joueur lors d'une attaque.

    Attributs propres :
        - max_health: Points de vie maximum du joueur.
        - selected_bullet_type_index: Index du type de projectile actuellement sélectionné.
        - bullet_types: Liste des types de projectiles disponibles pour le joueur.

    Méthodes :
        - add_bullet(bullet): Ajoute un type de projectile à la liste des types disponibles.
        - select_bullet_type(index): Sélectionne le type de projectile selon l'index fourni.
        - shoot(target_x, target_y, bullet_group): Tire un projectile vers une cible donnée.
        - cooldown_tick(): Diminue le délai de recharge entre les attaques.
        - show_bullets(screen, font, WIDTH): Affiche les types de projectiles disponibles à l'écran.
        - update_healthbar(screen): Met à jour la barre de vie du joueur à l'écran.
    """
    def __init__(self, x, y):
        super().__init__(x, y, "Application/images/Player.png", 'Player', PLAYER_SPEED, PLAYER_HEALTH, ATTACK_COOLDOWN, PLAYER_SHOOT_DAMAGE)
        self.max_health = PLAYER_MAX_HEALTH
        self.selected_bullet_type_index = 0
        self.bullet_types = [BasicBullet]

    def add_bullet(self, bullet):
        self.bullet_types.append(bullet)
    
    def select_bullet_type(self, index):
        if 0 <= index < len(self.bullet_types):
            self.selected_bullet_type_index = index

    def shoot(self, target_x, target_y, bullet_group):
        angle = math.atan2(target_y - self.position[1], target_x - self.position[0])
        center_x = self.position[0] + self.rect.width / 2
        center_y = self.position[1] + self.rect.height / 2
        bullet_type = self.bullet_types[self.selected_bullet_type_index]
        bullet_group.add(bullet_type(center_x, center_y, angle))

    def cooldown_tick(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
    
    def show_bullets(self, screen, font, WIDTH):
        small_font = pygame.font.Font(None, 18)   
        Bullet_surface = pygame.Surface((200, 150), pygame.SRCALPHA)
        Bullet_surface.fill((50, 50, 50, 0)) 
        y_offset = 1  

        for index, bullet in enumerate (self.bullet_types):
            
            bullet_text_lines = textwrap.wrap(f"Appuyez sur {index + 1} pour équiper {bullet.__name__}", width=30)
            for line in bullet_text_lines:
                bullet_text = small_font.render(line, True, (0, 0, 0))  
                Bullet_surface.blit(bullet_text, (20, y_offset)) 
                y_offset += 20 

        screen.blit(Bullet_surface, (550, 550))

    def update_healthbar (self, screen):   
        bar_color = (85,209,70)
        bar_fond_color = (255,95,65)
        bar_position = [15, 15, self.health, 10]
        bar_fond_position = [15, 15, self.max_health, 10]
        pygame.draw.rect(screen, bar_fond_color, bar_fond_position)
        pygame.draw.rect(screen, bar_color, bar_position)
    
class Enemy(Entity):
    """
    Classe représentant un ennemi dans le jeu.

    Hérite de la classe Entity.

    Attributs hérités de Entity :
        - position: Liste [x, y] représentant les coordonnées de l'ennemi sur l'écran.
        - old_position: Anciennes coordonnées de l'ennemi avant le dernier déplacement.
        - sprite_sheet: Surface contenant la feuille de sprites de l'ennemi.
        - image: Image actuellement affichée de l'ennemi.
        - rect: Rectangle de collision de l'ennemi pour la détection de collisions.
        - speed: Vitesse de déplacement de l'ennemi.
        - health: Points de vie actuels de l'ennemi.
        - attack_cooldown: Délai de recharge entre les attaques de l'ennemi.
        - damage: Dommages infligés par l'ennemi lors d'une attaque.

    Méthodes :
        - update(player): Met à jour la position de l'ennemi en se dirigeant vers le joueur.
        - attack(player, damage): Attaque le joueur si le délai de recharge est écoulé.

    Remarque : Les méthodes spécifiques à chaque type d'ennemi (comme `rage` pour le Golem ou `shoot_all_directions` pour le Golem) sont définies dans leurs sous-classes respectives.
    """
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
    """
    Classe représentant un Golem dans le jeu.

    Hérite de la classe Enemy.

    Attributs propres :
        - initial_attack_cooldown: Délai initial de recharge entre les attaques du Golem.
        - rage_sprite_sheet: Feuille de sprite utilisée lorsque le Golem est en rage.
        - is_raging: Indique si le Golem est en état de rage.

    Méthodes :
        - __init__(self, x, y): Initialise un Golem avec des attributs spécifiques.
        - get_image(self, x, y, sprite_sheet=None): Récupère l'image du Golem en fonction des coordonnées et de la feuille de sprite.
        - rage(self): Active l'état de rage du Golem s'il est en dessous de la moitié de ses points de vie.
        - shoot_all_directions(self, bullet_group): Fait tirer le Golem dans toutes les directions en ajoutant des projectiles au groupe de projectiles.
    """
    def __init__(self, x, y):
        super().__init__(x, y, "Application/images/Golem.png", 'Golem', GOLEM_SPEED, GOLEM_HEALTH, GOLEM_ATTACK_COOLDOWN, GOLEM_DAMAGE)
        self.initial_attack_cooldown = GOLEM_ATTACK_COOLDOWN
        self.image = self.get_image(0, 0)
        self.image.set_colorkey((0, 0, 0))
        self.rage_sprite_sheet = pygame.image.load("Application/images/GolemRage.png").convert_alpha()  # Charger la feuille de sprite de rage
        self.is_raging = False

    def get_image(self, x, y, sprite_sheet=None):
        if sprite_sheet is None:
            sprite_sheet = self.sprite_sheet
        image = pygame.Surface((67, 69), pygame.SRCALPHA)
        image.blit(sprite_sheet, (0, 0), (x, y, 67, 69))
        return image

    def rage(self):
        if self.health <= GOLEM_HEALTH / 2 and not self.is_raging:
            self.speed = GOLEM_SPEED * 2
            self.damage = GOLEM_DAMAGE * 4
            self.image = self.get_image(0, 0, self.rage_sprite_sheet)
            self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect(topleft=self.rect.topleft)  # Ajuster le rectangle de collision
            self.is_raging = True  # Éviter de changer l'image plusieurs fois

    def shoot_all_directions(self, bullet_group):
        for angle in range(0, 360, 45):  # Tirer dans 8 directions (0, 45, 90, ..., 315 degrés)
            rad_angle = math.radians(angle)
            boss_center_x = self.position[0] + self.rect.width / 2
            boss_center_y = self.position[1] + self.rect.height / 2
            bullet_group.add(BossBullet(boss_center_x, boss_center_y, rad_angle))

class Npc(Entity):
    """
    Classe représentant un personnage non-joueur (NPC) dans le jeu.

    Hérite de la classe Entity.

    Attributs hérités de Entity :
        - position: Liste [x, y] représentant les coordonnées du NPC sur l'écran.
        - old_position: Anciennes coordonnées du NPC avant le dernier déplacement.
        - sprite_sheet: Surface contenant la feuille de sprites du NPC.
        - image: Image actuellement affichée du NPC.
        - rect: Rectangle de collision du NPC pour la détection de collisions.
        - speed: Vitesse de déplacement du NPC.
        - health: Points de vie actuels du NPC.
        - attack_cooldown: Délai de recharge entre les attaques du NPC.
        - damage: Dommages infligés par le NPC lors d'une attaque.

    Attributs propres :
        - interaction_range: Distance maximale à laquelle le joueur peut interagir avec le NPC.
        - dialogue_box: Boîte de dialogue utilisée pour interagir avec le NPC.

    Méthodes :
        - interact(player, dialogue): Initie une interaction avec le joueur en affichant une boîte de dialogue.
        - in_interaction_range(player): Vérifie si le joueur est à portée d'interaction avec le NPC.
        - draw_dialogue_box(screen): Affiche la boîte de dialogue du NPC à l'écran.
        - close_dialogue_box(): Ferme la boîte de dialogue du NPC.
        - advance_dialogue(): Avance à la prochaine étape du dialogue avec le NPC.
    """
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



