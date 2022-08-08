import pygame

class Cell(pygame.sprite.Sprite):
    def __init__(self, row, col, size, total_rows, total_cols, groups):
        super().__init__(groups)
        self.screen = pygame.display.get_surface()
        self.row = row
        self.col = col
        self.size = size
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.x = col * size
        self.y = row * size

        # cell state
        self.visited = False
        self.queued = False
        self.start_node = False
        self.target_node = False
        self.barrier = False
        self.neighbors = None
        self.walls = None
        self.maze_neighbors = None
        self.color = 'grey30'

        # for bidirectional
        self.visited_v2 = False

        # sprite settings
        self.image = pygame.Surface((size-1,size-1))
        self.rect = self.image.get_rect(topleft = (self.x,self.y))

    def get_pos(self):
        return self.row, self.col


    def reset(self):
        self.color = 'grey30'
        self.start_node = False
        self.target_node = False
        self.barrier = False
        self.visited = False
        self.queued = False
        self.visited_v2 = False

    def make_start(self):
        self.reset()
        self.start_node = True

    def make_target(self):
        self.reset()
        self.target_node = True
    
    def make_barrier(self):
        self.reset()
        self.color = 'black'
        self.barrier = True

    def queue(self):
        self.color = 'turquoise3'
        self.queued = True

    def visit(self):
        self.color = 'turquoise4'
        self.visited = True

    def queue_v2(self):
        self.color = 'aquamarine3'
        self.queued = True

    def visit_v2(self):
        self.color = 'aquamarine4'
        self.visited_v2 = True

    def make_path(self):
        self.color = 'midnightblue'

    def update_neighbors(self, grid):
        self.neighbors = {}
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].barrier:
            self.neighbors['down'] = grid[self.row + 1][self.col]

        if self.col > 0 and not grid[self.row][self.col - 1].barrier:
            self.neighbors['left'] = grid[self.row][self.col - 1]

        if self.row > 0 and not grid[self.row - 1][self.col].barrier:
            self.neighbors['up'] = grid[self.row - 1][self.col]

        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].barrier:
            self.neighbors['right'] = grid[self.row][self.col + 1]

    def update_walls(self, grid):
        self.walls = {}
        if self.row < self.total_rows - 1 and grid[self.row + 1][self.col].barrier: 
            self.walls['down'] = grid[self.row + 1][self.col]

        if self.col > 0 and grid[self.row][self.col - 1].barrier:
            self.walls['left'] = grid[self.row][self.col - 1]

        if self.row > 0 and grid[self.row - 1][self.col].barrier:
            self.walls['up'] = grid[self.row - 1][self.col]

        if self.col < self.total_cols - 1 and grid[self.row][self.col + 1].barrier:
            self.walls['right'] = grid[self.row][self.col + 1]
        
    def update_neighbors_for_maze(self, grid):
        # for maze, neighbors considered to be second but next cell eg distance of 2
        self.maze_neighbors = {}
        if self.row < self.total_rows - 2 and not grid[self.row + 2][self.col].barrier:
            self.maze_neighbors['down'] = grid[self.row + 2][self.col]

        if self.col > 1 and not grid[self.row][self.col - 2].barrier:
            self.maze_neighbors['left'] = grid[self.row][self.col - 2]

        if self.row > 1 and not grid[self.row - 2][self.col].barrier:
            self.maze_neighbors['up'] = grid[self.row - 2][self.col]

        if self.col < self.total_cols - 2 and not grid[self.row][self.col + 2].barrier:
            self.maze_neighbors['right'] = grid[self.row][self.col + 2]



    def left_clicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]
    def right_clicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[2]

    def update(self, level):
        if self.right_clicked():
            if self.start_node: 
                level.start_node = None
            elif self.target_node:
                level.target_node = None
            self.reset()

        elif self.left_clicked():
            if level.start_node is None and not self.target_node:
                self.make_start()
                level.start_node = self
            elif level.target_node is None and not self.start_node:
                self.make_target()
                level.target_node = self
            elif not self.start_node and not self.target_node:
                self.make_barrier()

        if self.start_node: self.color = 'red'
        if self.target_node: self.color = 'yellow'
        
        self.image.fill(self.color)
        #pygame.draw.rect(self.screen, self.color, self.rect, border_radius=5)
    
    def __lt__(self, other):
        return False