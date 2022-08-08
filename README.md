# Path Finding Visualizer  

https://user-images.githubusercontent.com/83274722/183077296-ea9ba290-4d29-4420-ae93-ea23cd5e45a1.mp4


An interactive Python application that visualizes different pathfinding, as well as maze generation computer algorithms for the user.  
This is a personal project for the purposes of learning and improving, made using the pygame module.

## Features
Graphical user interface, with the ability to place the starting/target position as well as walls on the grid.  
3 configurable screen resolutions:
- small grid: 1280x720 (80 columns by 45 rows)  
- medium grid: 1400x840 (100 columns by 60 rows)  
- large grid: 1500x900 (150 columns by 90 rows)  
  
  
### Currently supports the following path finding algorithms  
- Breadth first search
- Depth first search
- A* search (Manhattan distance heuristic, FIFO tie-breaker)
- Greedy best first search (Manhattan distance heuristic, FIFO tie-breaker)
- Bi-directional BFS
- Bi-directional DFS
  
  
### Currently supports the following maze generation algorithms  
- Recursive division  
- Randomized DFS  
- Aldous Border (HIGHLY not recommended.. The random nature of this algorithm means it can take a VERY long time until it generates a maze. It does however produce uniform spanning trees.)  
  
  
### Other
- Function for random wall placement  