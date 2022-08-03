import pygame, sys
from level import Level
from collections import deque

class BreadthFirstSearch(Level):
    def __init__(self, clock):
        super().__init__(clock)
    
    def run_algorithm(self):
        self.came_from = {}
        q = deque()
        q.append(self.start_node)
        while q:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(1)

            curr = q.popleft()
            if curr is self.target_node:
                return True
            curr.visit()

            neighbors_group = pygame.sprite.Group()
            for neighbor in list(curr.neighbors.values()):
                if not neighbor.visited and not neighbor.queued:
                    neighbor.queue()
                    self.came_from[neighbor] = curr
                    q.append(neighbor)
                neighbors_group.add(neighbor)

            neighbors_group.update(self)
            neighbors_group.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(400)

        return False
