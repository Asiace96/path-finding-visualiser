import pygame, sys, random, tkinter
from cell import Cell
from settings import *
from tkinter import messagebox

class Level:
    def __init__(self, clock):
        self.screen = pygame.display.get_surface()
        self.clock = clock
        self.rows = ROWS
        self.cols = COLS
        self.cell_size = CELL_SIZE

        self.cell_group = pygame.sprite.Group()
        self.grid = self.create_grid()
        self.came_from = None
        self.start_node = None
        self.target_node = None

        self.running = True


    def create_grid(self):
        grid = []
        for i in range(self.rows):
            grid.append([])
            for j in range(self.cols):
                grid[i].append(Cell(i, j, self.cell_size, self.rows, self.cols, [self.cell_group]))
        return grid

    def update_neighbors(self):
        for row in self.grid:
            for cell in row:
                cell.update_neighbors(self.grid)
    
    def clear_grid(self):
        self.start_node = None
        self.target_node = None
        for row in self.grid:
            for cell in row:
                cell.reset()
    
    def random_barriers(self):
        for row in self.grid:
            for cell in row:
                if not random.randint(0,2) and not cell.start_node and not cell.target_node:
                    cell.make_barrier()
    
    def get_clicked_node_pos(self):
        x,y = pygame.mouse.get_pos()
        row = y // CELL_SIZE
        col = x // CELL_SIZE
        return row,col   

    def h(self, p1, p2):
        x1,y1 = p1
        x2,y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    def draw_path(self):
        current = self.target_node
        while current in self.came_from:
            current = self.came_from[current]
            if current is self.start_node:
                break
            current.make_path()
    
    def run(self):
        self.screen.fill('black')
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit(1)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_c:
                        self.clear_grid()
                    if event.key == pygame.K_r:
                        self.random_barriers()
                    if event.key == pygame.K_RETURN:
                        self.update_neighbors()
                        if self.start_node is None or self.target_node is None:
                            tkinter.Tk().withdraw()
                            messagebox.showinfo('Alert','Need to place start node / target node')
                            break
                        path_found = self.run_algorithm()
                        if path_found:
                            self.draw_path()
                        else:
                            tkinter.Tk().withdraw()
                            messagebox.showinfo('Alert','No path found')

            self.cell_group.update(self)
            self.cell_group.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

    def run_algorithm():
        pass