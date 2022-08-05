import pygame, sys
from level import Level
from queue import PriorityQueue

class AStarSearch(Level):
    def __init__(self, clock):
        super().__init__(clock)
    
    def run_algorithm(self):
        self.came_from = {}
        open_set = PriorityQueue()
        g_score = {cell: float('inf') for row in self.grid for cell in row}
        f_score = {cell: float('inf') for row in self.grid for cell in row}
        g_score[self.start_node] = 0
        f_score[self.start_node] = self.h(self.start_node.get_pos(), self.target_node.get_pos())
        count = 0
        open_set.put((f_score[self.start_node], count, self.start_node))
        open_set_members = {self.start_node}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(1)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return False

            curr = open_set.get()[2]
            open_set_members.remove(curr)
            if curr is self.target_node:
                return True
            curr.visit()

            neighbors_group = pygame.sprite.Group()
            for neighbor in list(curr.neighbors.values()):
                tmp_g_score = g_score[curr] + 1
                if tmp_g_score < g_score[neighbor]:
                    self.came_from[neighbor] = curr
                    g_score[neighbor] = tmp_g_score
                    f_score[neighbor] = tmp_g_score + self.h(neighbor.get_pos(), self.target_node.get_pos())
                    if neighbor not in open_set_members:
                        count += 1
                        open_set_members.add(neighbor)
                        open_set.put((f_score[neighbor],count,neighbor))
                        neighbor.queue()
                neighbors_group.add(neighbor)

            neighbors_group.update(self)
            neighbors_group.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(300)

        return False