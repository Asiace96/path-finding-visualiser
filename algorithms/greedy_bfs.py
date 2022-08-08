import pygame, sys
from level import Level
from queue import PriorityQueue

class GreedyBestFirstSearch(Level):
    def __init__(self, clock, num_cols):
        super().__init__(clock, num_cols)
    
    def run_algorithm(self):
        self.came_from = {}
        open_set = PriorityQueue()
        score = {cell: self.h(cell.get_pos(), self.target_node.get_pos()) for row in self.grid for cell in row}
        count = 0
        open_set.put((score[self.start_node], count, self.start_node))

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(1)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return False

            curr = open_set.get()[2]
            if curr is self.target_node:
                return True
            curr.visit()

            neighbors_group = pygame.sprite.Group()
            for neighbor in list(curr.neighbors.values()):
                if not neighbor.visited and not neighbor in self.came_from:
                    count += 1
                    open_set.put((score[neighbor],count,neighbor))
                    neighbor.queue()
                    self.came_from[neighbor] = curr
                neighbors_group.add(neighbor)


            neighbors_group.update(self)
            neighbors_group.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(200)

        return False