import pygame, sys, os
from settings import *
from gui import MainMenu


class Game():
    def __init__(self):
        
    #----------------------- general setup ----------------------------#

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Path Finding Algorithm Visualizer')
        main_icon = pygame.image.load(os.path.join('assets', 'main_icon.png')).convert_alpha()
        icon = pygame.image.load(os.path.join('assets', 'icon.png')).convert_alpha()
        #title_font = os.path.join('assets', 'Ubuntu-Bold.ttf')
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()

    #----------------------- instantiate game state--------------------#

        self.menu = MainMenu(self.clock, main_icon)
    
    #---------------------- game loop ---------------------------------#

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(1)
            
            self.menu.run()

if __name__== '__main__':
    game = Game()
    game.run()