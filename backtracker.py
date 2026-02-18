import random
from sys import exit
class MazeGenerationParts:
        def __init__(self, maze):
            self.maze = maze
        @staticmethod
        def pattern_42(height, width):
            base_pattern = {
                            (0,0) ,(0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (2, 4), 
                            (4, 0), (5, 0), (6, 0), (6, 1),  (4, 2), (5, 2), (6, 2), (4, 3),
                            (4,4), (5,4), (6,4)
                            }
            pattern_width = max(x for x, _ in base_pattern) + 1
            pattern_height = max(y for _, y in base_pattern) + 1
            if height <= pattern_height or width <= pattern_width:
                print(f"cannot place pattern on the maze {width}/{height}")
                exit(1)
            scale_x = width // pattern_width
            scale_y = height // pattern_height
            scale = max(1, min(scale_x, scale_y) // 25)
            pattern_height = pattern_height * scale
            pattern_width = pattern_width * scale
            middle_x = (width - pattern_width) // 2
            middle_y = (height - pattern_height) // 2
            scaled_pattern = set()
            for bx, by in base_pattern:
                for sx in range(scale):
                    for sy in range(scale):
                        x = bx * scale + sx + middle_x
                        y = by * scale + sy + middle_y
                        scaled_pattern.add((x, y))
            return scaled_pattern
        
        @staticmethod
        def iterative_backtracker(maze, height, width, entry, compass, exit_, seed):
            pattern_coords = MazeGenerationParts.pattern_42(height, width)
            enx, eny = entry
            random.shuffle(compass)
            stack_simulation = [(enx, eny, compass.copy())]
            visited_cells = {(enx, eny)}
            for cord in pattern_coords:
                if cord == entry or cord == exit_:
                    print(f"Entry/Exit spotted on pattern")
                    exit(1)
                visited_cells.add(cord)
                x, y = cord
                maze[y,x] = 0xF
            while stack_simulation:
                x, y, cell_compass = stack_simulation[-1]
                moved = False
                while cell_compass:
                    move = cell_compass.pop(0)
                    if move == "North" and y > 0 and (x, y-1) not in visited_cells:
                        maze[y, x] -= 1      
                        maze[y-1, x] -= 4    
                        visited_cells.add((x, y-1))
                        fresh_compass = compass.copy()
                        random.shuffle(fresh_compass)
                        stack_simulation.append((x, y-1, fresh_compass))
                        moved = True
                        break
                    if move == "South" and y < height - 1 and (x, y+1) not in visited_cells:
                        maze[y, x] -= 4   
                        maze[y+1, x] -= 1  
                        visited_cells.add((x, y+1))
                        fresh_compass = compass.copy()
                        random.shuffle(fresh_compass)
                        stack_simulation.append((x, y+1, fresh_compass))
                        moved = True
                        break
                    if move == "West" and x > 0 and (x-1, y) not in visited_cells:
                        maze[y, x] -= 8    
                        maze[y, x-1] -= 2    
                        visited_cells.add((x-1, y))
                        fresh_compass = compass.copy()
                        random.shuffle(fresh_compass)
                        stack_simulation.append((x-1, y, fresh_compass))
                        moved = True
                        break
                    if move == "East" and x < width - 1 and (x+1, y) not in visited_cells:
                        maze[y, x] -= 2 
                        maze[y, x+1] -= 8   
                        visited_cells.add((x+1, y))
                        fresh_compass = compass.copy()
                        random.shuffle(fresh_compass)
                        stack_simulation.append((x+1, y, fresh_compass))
                        moved = True
                        break
                if not moved:
                    stack_simulation.pop()
            return maze

        @staticmethod
        def bfs(maze, entry, exit_) -> str:
            directions = {0: (0, -1, 'N'), 1: (1, 0, 'E'), 2: (0, 1, 'S'), 3: (-1, 0, 'W')}
            enx, eny = entry
            exx, exy = exit_
            queue = [(enx, eny, "")]
            visited = {(enx, eny)}
            height, width = maze.shape
            while queue:
                x, y, path = queue.pop(0)
                

                for direction, (dx, dy, compass) in directions.items():
                    if (x, y) == (exx, exy):
                        return path + compass
                    if not bool(maze[y, x] & (0x1 << direction)):
                        nx, ny = x + dx, y + dy
                        
                        if (0 <= nx < width and 
                            0 <= ny < height and
                            (nx, ny) not in visited):

                            visited.add((nx, ny))
                            queue.append((nx, ny, path + compass))

            return "No path found"
        @staticmethod
        def imperfect_maze(maze, height, width):
            pattern_coords = MazeGenerationParts.pattern_42(height, width)
            directions = [(0, -1, 0, 2), (1, 0, 1, 3), (0, 1, 2, 0), (-1, 0, 3, 1)]
            removed_walls = set()

            total_walls = int((width * height) * 0.25)
            max_tries = width * height
            walls = 0
            tries = 0
            while tries < max_tries and walls < total_walls:
                tries += 1
                x , y = random.randint(0, width - 1), random.randint(0, height - 1)
                dx, dy , wall, neighbor_wall = random.choice(directions)
                nx = dx + x
                ny = dy + y
                if not (0 <= nx < width and 0 <= ny < height):
                    continue
                if (nx, ny) in pattern_coords or (x, y) in pattern_coords:
                    continue
                if bool(maze[y, x] & (1 << wall)):
                    maze[y,x] &= ~(1 << wall)
                    maze[ny,nx] &= ~(1 << neighbor_wall)
                    walls += 1
                    removed_walls.add((x, y))
            return maze