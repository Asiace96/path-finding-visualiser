import pygame, sys, os
from settings import *
from algorithms import BreadthFirstSearch
from algorithms import DepthFirstSearch
from algorithms import AStarSearch
from algorithms import GreedyBestFirstSearch

class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, color, pos, groups, draw_in_center=False, font=None):
        super().__init__(groups)
        self.screen = pygame.display.get_surface()
        self.color = color
        self.font = pygame.font.Font(font, size)
        self.pos = pos
        self.draw_in_center = draw_in_center
        self.set(text)
    
    def set(self, text):
        self.image = self.font.render(str(text), True, self.color)
        if self.draw_in_center:
            self.rect = self.image.get_rect(center=self.pos)
        else:
            self.rect = self.image.get_rect(topleft=self.pos)


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, groups, font=None, font_size=0, text=''):
        super().__init__(groups)
        self.screen = pygame.display.get_surface()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.outline = pygame.Rect(x-2, y-2, width+4, height+4)
        self.color = color
        self.text = text
        self.font = pygame.font.Font(font, font_size)

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def draw_text(self, text_color):
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def update(self):
        button_color = self.color if self.is_hovered() else 'black'
        pygame.draw.rect(self.screen, 'black', self.outline, border_radius = 15)
        pygame.draw.rect(self.screen, button_color, self.rect, border_radius = 13)
        
        if not self.text == '':
            text_color = 'black' if self.is_hovered() else 'white'
            self.draw_text(text_color)


class Menu:
    def __init__(self, clock, main_image):
        self.screen = pygame.display.get_surface()
        self.main_image = main_image
        self.font_path = os.path.join('assets', 'Ubuntu-Bold.ttf')
        self.clock = clock
        self.running = True
        self.action = None
        self.state = None

        self.text_sprites = pygame.sprite.Group()
        self.button_sprites = pygame.sprite.Group()


    def run(self):
        while self.running:
            self.action = None
            self.screen.fill('grey70')
            self.screen.blit(self.main_image, (WIDTH//2,HEIGHT//3))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit(1)
                
                self.run_menu(event)


            self.text_sprites.draw(self.screen)
            self.button_sprites.update()
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def run_menu(self, event):
        pass



class MainMenu(Menu):
    def __init__(self, clock, main_image):
        super().__init__(clock, main_image)
        self.buttons = [
                        Button(50,70, 260,50, 'red', self.button_sprites, font_size=25, text='Controls'),
                        Button(50,HEIGHT*0.6, 260,50, 'green', self.button_sprites, font_size=25, text='Breadth First Search'),
                        Button(50,HEIGHT*0.7, 260,50, 'green', self.button_sprites, font_size=25, text='Depth First Search'),
                        Button(50,HEIGHT*0.8, 260,50, 'green', self.button_sprites, font_size=25, text='A* Search'),
                        Button(50,HEIGHT*0.9, 260,50, 'green', self.button_sprites, font_size=25, text='Greedy Best First Search')
                        ]
        self.texts = [
                      Text('Path Finding Visuaizer', 50, 'black', (WIDTH//3,HEIGHT//3), self.text_sprites, font=self.font_path),
                      Text('By Asaf Brandwain', 30, 'black', (WIDTH//3,HEIGHT//2), self.text_sprites, font=self.font_path)
                    ]

    def run_menu(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                pygame.quit()
                sys.exit(1)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.is_hovered():
                    self.action = button.text
            if self.action == 'Controls':
                self.state = ControlMenu(self.clock, self.main_image)
                self.state.run()
            if self.action == 'Breadth First Search':
                self.state = BreadthFirstSearch(self.clock)
                self.state.run()
            if self.action == 'Depth First Search':
                self.state = DepthFirstSearch(self.clock)
                self.state.run()
            if self.action == 'A* Search':
                self.state = AStarSearch(self.clock)
                self.state.run()
            if self.action == 'Greedy Best First Search':
                self.state = GreedyBestFirstSearch(self.clock)
                self.state.run()


class ControlMenu(Menu):
    def __init__(self, clock, main_image):
        super().__init__(clock, main_image)
        self.texts = [
                    Text('Controls:', 50, 'black', (WIDTH//2,100), self.text_sprites, draw_in_center=True),
                    Text('Esc - Go back', 36, 'black', (100,200), self.text_sprites, draw_in_center=False),
                    Text('R - Random barriers', 36, 'black', (100,300), self.text_sprites, draw_in_center=False),
                    Text('C - Clear grid', 36, 'black', (100,400), self.text_sprites, draw_in_center=False),
                    Text('Enter - Run algorithm', 36, 'black', (100,500), self.text_sprites, draw_in_center=False)
                    ]
    
    def run_menu(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False

        