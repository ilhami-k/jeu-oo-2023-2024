import pygame
from settings import *
from game import *
from save_system import SaveSystem
import textwrap
class Button: 
    def __init__(self, x, y, width, height, foreground=(255,255,255,255), background=(0,0,0,256), content=None, fontsize=36):
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
class Npc_Dialogues:
    def __init__(self, messages, font_size, width, height, x, y, bg_color, text_color):
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
        if self.index < len(self.messages) - 1:
            self.index += 1
            print(f"Advancing to message index: {self.index}")
            return True
        print("No more messages to advance to")
        return False

    def reset(self):
        self.index = 0

class Interface:
    def __init__(self,player,prologue_on,new_game):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.intro_background = pygame.image.load("../Application/images/background.png")
        self.new_game = False
        self.prologue_on = False
        self.epilogue_on = False
        self.save_load = SaveSystem('.json','Application/save_data/')
        self.player = player
        self.end_background = pygame.image.load("../Application/images/background.png")
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
            prologue_box = DialogueBox("Dans un monde semblable au nôtre, la petite ville de Greenfield vivait paisiblement, entourée de forêts et de collines. Les habitants menaient une vie simple et tranquille, jusqu'au jour où des monstres apparurent soudainement. Sortis de nulle part, ces créatures terrifiantes commencèrent à envahir les rues, semant la panique et la destruction.Les autorités, dépassées, ne pouvaient contenir le chaos. Au cœur de cette invasion se trouvait un mystérieux golem, source de tous les maux. Votre mission est claire : réunir les forces nécessaires, affronter les monstres, et détruire le golem pour restaurer la paix à Greenfield.", 24, 700, 300, 50, HEIGHT - 350, (255, 255, 128,128), (0, 0, 0))
            prologue_box.draw(self.screen)
            #  def __init__(self, text, font_size=24, width=600, height=200, x=100, y=100, bg_color=(255, 255, 255), text_color=(0, 0, 0)):
            press_enter_box = DialogueBox("Appuyez sur Entrée pour continuer...", 22, 300, 50, WIDTH/2 - 150, HEIGHT - 50, (255, 255, 255), (0, 0, 0))
            press_enter_box.draw(self.screen)
            pygame.display.update()
    def ending_screen (self):
        self.ending = True
        title = self.font.render("Vous avez terminé le jeu", True, 'White')
        title_rect = title.get_rect(center=(WIDTH/2, HEIGHT/4))
        exit_button = Button(WIDTH/2 - 100, HEIGHT/2 - 100 , 200, 50, (255, 255, 255), (0, 0, 0), "Exit", 36)
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
            
            stretched_image = pygame.transform.scale(self.intro_background,(800,1000))
            self.screen.blit(stretched_image, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(exit_button.image, exit_button.rect)
            prologue_box = DialogueBox("Alors que le golem s'effondre dans un fracas assourdissant, un silence envahit Greenfield. Les monstres disparaissent et les habitants émergent de leurs refuges, incrédules mais soulagés. Les nuages sombres se dissipent, révélant un ciel clair.Le héros, fatigué mais victorieux, se tient au centre de la place, entouré de visages reconnaissants. Les applaudissements éclatent, remplissant l'air d'une joie nouvelle. La paix est enfin restaurée à Greenfield, grâce à son courage.", 24, 700, 300, 50, HEIGHT - 350, (255, 255, 128,128), (255, 255, 255))
            prologue_box.draw(self.screen)   
            pygame.display.update()
