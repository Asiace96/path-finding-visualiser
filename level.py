import pygame, sys, random, tkinter
from collections import deque
from cell import Cell
from settings import FPS
from tkinter import messagebox

class Level:
    def __init__(self, clock, num_cols):
        self.screen = pygame.display.get_surface()
        self.clock = clock
        self.cols = num_cols
        self.cell_size = self.screen.get_width() // self.cols
        self.rows = self.screen.get_height() // self.cell_size

        self.cell_group = pygame.sprite.Group()
        self.grid = self.create_grid()
        self.came_from = None
        self.start_node = None
        self.target_node = None

        #for bidirectional
        self.bi_directional = False
        self.came_from_start = None
        self.came_from_target = None
        self.intersection = None

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
    
    def update_walls(self):
        for row in self.grid:
            for cell in row:
                cell.update_walls(self.grid)
    
    def update_neighbors_for_maze(self):
        for row in self.grid:
            for cell in row:
                cell.update_neighbors_for_maze(self.grid)
    
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
        row = y // self.cell_size
        col = x // self.cell_size
        return row,col   

    def h(self, p1, p2):
        x1,y1 = p1
        x2,y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    def draw_path(self):
        current = self.target_node
        group = pygame.sprite.Group()
        while current in self.came_from:
            current = self.came_from[current]
            if current is self.start_node:
                break
            current.make_path()
            group.add(current)
            group.update(self)
            group.draw(self.screen)
            pygame.display.update(current.rect)
            self.clock.tick(120)

    # for bidirectional
    def draw_path_v2(self):
        self.intersection.make_path()
        current_1 = self.intersection
        current_2 = self.intersection
        group = pygame.sprite.Group()
        while current_1 in self.came_from_start and current_2 in self.came_from_target:
            current_1 = self.came_from_start[current_1]
            current_2 = self.came_from_target[current_2]
            current_1.make_path()
            current_2.make_path()

            if current_1 is self.start_node:
                while current_2 in self.came_from_target:
                    current_2 = self.came_from_target[current_2]
                    if current_2 is self.target_node:
                        return
                    current_2.make_path()
                    group.add(current_2)
                    group.update(self)
                    group.draw(self.screen)
                    pygame.display.flip()
                    self.clock.tick(120)

            if current_2 is self.target_node:
                while current_1 in self.came_from_start:
                    current_1 = self.came_from_start[current_1]
                    if current_1 is self.start_node:
                        return
                    current_1.make_path()
                    group.add(current_1)
                    group.update(self)
                    group.draw(self.screen)
                    pygame.display.flip()
                    self.clock.tick(120)

            group.add(current_1, current_2, self.intersection)
            group.update(self)
            group.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(120)


    def wall_maze(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if i == 0 or i == self.rows - 1 or j == 0 or j == self.cols - 1:
                    self.grid[i][j].make_barrier()

    def random_wall(self, min_row, max_row, min_col, max_col):
        # walls only in even cells, holes only in odd cells
        row_idx = (random.randint(min_row+2, max_row-2)//2)*2
        col_idx = (random.randint(min_col+2, max_col-2)//2)*2

        if abs(min_row-max_row) < abs(min_col-max_col):
            for i in range(min_row, max_row+1):
                for j in range(min_col, max_col+1):
                    if j==col_idx:
                        self.grid[i][j].make_barrier()
            
            x = (random.randint(min_row+1,max_row-1)//2)*2 + 1
            hole = x if x!=max_row else max_row-1
            self.grid[hole][col_idx].reset()
            return col_idx

        else:
            for i in range(min_row, max_row+1):
                for j in range(min_col, max_col+1):
                    if i==row_idx:
                        self.grid[i][j].make_barrier()
            x = (random.randint(min_col+1,max_col-1)//2)*2 + 1
            hole = x if x!=max_col else max_col-1
            self.grid[row_idx][hole].reset()
            return row_idx

    def recursive_division(self, min_row, max_row, min_col, max_col):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(1)

        if max_row-min_row<=3 or max_col-min_col<=3:
            return
        
        idx = self.random_wall(min_row, max_row, min_col, max_col)

        self.cell_group.update(self)
        self.cell_group.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(FPS)

        if abs(min_row-max_row) < abs(min_col-max_col):
            self.recursive_division(min_row, max_row, min_col, idx)
            self.recursive_division(min_row, max_row, idx, max_col)
        else:
            self.recursive_division(min_row, idx, min_col, max_col)
            self.recursive_division(idx, max_row, min_col, max_col)

    def odd_walls(self):
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if c%2==1 or r%2==1:
                    cell.make_barrier()

    def randomized_dfs(self):
        visited = set()
        s = deque()
        sr,sc = random.randrange(0,self.rows,2), random.randrange(0,self.cols,2)
        curr = self.grid[sr][sc]
        visited.add(curr)
        s.append(curr)

        while s:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(1)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return False

            curr = s.pop()
            unvisited = {}
            for direction, neighbor in list(curr.maze_neighbors.items()):
                if neighbor not in visited:
                    unvisited[direction] = neighbor
            if unvisited:
                s.append(curr)
                direction, neighbor = random.choice(list(unvisited.items()))
                curr.walls[direction].reset()
                visited.add(neighbor)
                s.append(neighbor)

            self.cell_group.update(self)
            self.cell_group.draw(self.screen)
            pygame.draw.rect(self.screen,'green',curr.rect)
            pygame.display.flip()
            self.clock.tick(FPS)
                
    def aldous_border(self):
        visited = set()
        to_visit = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if i%2==0 and j%2==0:
                    to_visit+=1
        sr,sc = random.randrange(0,self.rows,2), random.randrange(0,self.cols,2)
        curr = self.grid[sr][sc]
        visited.add(curr)

        while len(visited) < to_visit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(1)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return False
            direction, neighbor = random.choice(list(curr.maze_neighbors.items()))
            if neighbor not in visited:
                curr.walls[direction].reset()
                visited.add(neighbor)
            curr = neighbor

            self.cell_group.update(self)
            self.cell_group.draw(self.screen)
            pygame.draw.rect(self.screen,'green',curr.rect)
            pygame.display.flip()
            self.clock.tick(FPS)


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
                        self.clear_grid()
                        self.random_barriers()

                    if event.key == pygame.K_q:
                        self.clear_grid()
                        self.wall_maze()
                        self.recursive_division(0,self.rows-1, 0,self.cols-1)

                    if event.key == pygame.K_w:
                        self.clear_grid()
                        self.odd_walls()
                        self.update_walls()
                        self.update_neighbors_for_maze()
                        self.randomized_dfs()

                    if event.key == pygame.K_e:
                        self.clear_grid()
                        self.odd_walls()
                        self.update_walls()
                        self.update_neighbors_for_maze()
                        self.aldous_border()
                        
                    if event.key == pygame.K_RETURN:
                        self.update_neighbors()
                        if self.start_node is None or self.target_node is None:
                            tkinter.Tk().withdraw()
                            messagebox.showinfo('Alert','Need to place start node / target node')
                            break
                        path_found = self.run_algorithm()
                        if path_found and self.bi_directional:
                            self.draw_path_v2()
                        elif path_found:
                            self.draw_path()
                        else:
                            tkinter.Tk().withdraw()
                            messagebox.showinfo('Alert','No path found')

            self.cell_group.update(self)
            self.cell_group.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

    # Does nothing - hook for child classes to be run and implemented by
    def run_algorithm():
        pass