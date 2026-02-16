from collections import deque

class BFSPathfinder:    
    def __init__(self, maze: np.ndarray):
        self.maze = maze
        self.height, self.width = maze.shape
        
        self.DIRECTIONS = {
            0: (0, -1, 'N'),
            1: (1, 0, 'E'),
            2: (0, 1, 'S'),
            3: (-1, 0, 'W'),
        }
    
    def find_path(self, start_x: int, start_y: int,
                  end_x: int, end_y: int) -> str:        
        queue = deque([(start_x, start_y, "")])
        visited = {(start_x, start_y)}
        
        while queue:
            x, y, path = queue.popleft()
            
            if (x, y) == (end_x, end_y):
                return path
            
            for direction, (dx, dy, letter) in self.DIRECTIONS.items():
                has_wall = bool(self.maze[y, x] & (1 << direction))
                
                if not has_wall:
                    nx, ny = x + dx, y + dy
                    
                    if (0 <= nx < self.width and 
                        0 <= ny < self.height and
                        (nx, ny) not in visited):
                        
                        visited.add((nx, ny))
                        queue.append((nx, ny, path + letter))
        
        return ""


finder = BFSPathfinder(maze)
path = finder.find_path(0, 0, 19, 14)
print(f"Path: {path}")
print(f"Length: {len(path)} steps")