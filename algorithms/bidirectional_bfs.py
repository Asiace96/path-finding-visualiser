import pygame, sys
from level import Level
from collections import deque

class BiDirectionalBFS(Level):
    def __init__(self, clock):
        super().__init__(clock)
        self.came_from_start = None
        self.came_from_target = None
        self.intersection = None
    
    def draw_path(self):
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

    def run_algorithm(self):
        self.came_from_start = {}
        self.came_from_target = {}
        visited_start = []
        visited_target = []
        q_start = deque()
        q_target = deque()
        q_start.append(self.start_node)
        q_target.append(self.target_node)
        while q_start and q_target:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(1)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return False

            curr_1 = q_start.popleft()
            curr_2 = q_target.popleft()
            curr_1.visit()
            curr_2.visit_v2()
            visited_start.append(curr_1)
            visited_target.append(curr_2)

            if len(list(set(visited_start) & set(visited_target))) == 1:
                self.intersection = list(set(visited_start) & set(visited_target))[0]
                return True

            neighbors_group = pygame.sprite.Group()
            for neighbor in list(curr_1.neighbors.values()):
                if not neighbor.visited and not neighbor in self.came_from_start:
                    neighbor.queue()
                    self.came_from_start[neighbor] = curr_1
                    q_start.append(neighbor)
                neighbors_group.add(neighbor)

            for neighbor in list(curr_2.neighbors.values()):
                if not neighbor.visited and not neighbor in self.came_from_target:
                    neighbor.queue_v2()
                    self.came_from_target[neighbor] = curr_2
                    q_target.append(neighbor)
                neighbors_group.add(neighbor)

            neighbors_group.update(self)
            neighbors_group.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(300)

        return False