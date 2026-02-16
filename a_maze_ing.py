import numpy as n
import sys
import random
from typing import Any, List, Dict, Union, Optional

class A_Maze_Ing:
    def __init__(self):
        self.tokens = self.Maze_Config_Analyzer.parsing_config_data()
        self.width = self.tokens["WIDTH"]
        self.height = self.tokens["HEIGHT"]
        self.entry = self.tokens["ENTRY"]
        self.exit = self.tokens["EXIT"]
        self.output_file = self.tokens["OUTPUT_FILE"]
        self.seed = self.tokens["SEED"]
        self.perfect = self.tokens["PERFECT"]
        self.flawed = self.tokens["FLAWED"]
        self.maze = self.Recursive_Backtracker(self)

    class Maze_Config_Analyzer:
        @staticmethod
        def parsing_config_data() -> dict[str, Union[str, int, None]]:
            try:
                if len(sys.argv) > 2:
                    raise ValueError("Too many arguments provided. Only the configuration file path is required.")
                elif len(sys.argv) < 2:
                    raise ValueError("No configuration file provided. Please provide the path to the configuration file.")
                config_file = sys.argv[1]
                with open(config_file, "r") as f:
                    config_lines = [line.strip() for line in f]
                tokens = {
                    "WIDTH": 0,
                    "HEIGHT": 0,
                    "EXIT": {"x": 0, "y": 0},
                    "ENTRY": {"x": 0, "y": 0},
                    "OUTPUT_FILE": None,
                    "PERFECT": 0,
                    "FLAWED": None,
                    "SEED": None,
                }

                counts = {key: 0 for key in tokens}

                for line in config_lines:
                    if line is None or line == "" or line[0] == "#" or "=" not in line:
                        continue

                    key, value = map(str.strip, line.split("=", 1))
                    if key not in tokens or value == "":
                        continue

                    counts[key] += 1

                    match key:
                        case "WIDTH" | "HEIGHT":
                            try:
                                tokens[key] = int(value)
                                if tokens[key] <= 0:
                                    raise ValueError(f"{key} must be positive")
                            except ValueError as e:
                                raise ValueError(f"Invalid {key}: '{value}' is not a valid integer")

                        case "OUTPUT_FILE":
                            if len(value.split()) > 1 or value == "":
                                raise ValueError(f"Invalid file name: {value}")
                            tokens[key] = value

                        case "PERFECT":
                            if value not in ("True" ,"False"):
                                raise ValueError ("Acceptable 'PERFECT' format is 'True' or 'False'.")
                            tokens[key] = True if value == "True" else False

                        case "EXIT" | "ENTRY":
                            x, y = map(int, value.split(","))
                            tokens[key] = {"x": x, "y": y}

                        case "FLAWED" | "SEED":
                            try:
                                tokens[key] = int(value)
                            except ValueError:
                                tokens[key] = None

                for key, value_count in counts.items():
                    if value_count > 1:
                        raise ValueError(f"Duplicate token detected: {key}")
                    elif value_count <= 0:
                        if key == "FLAWED" or key == "SEED":
                            raise ValueError(f"Missing optional keys: {key}, use 'None' to discard")
                        else:
                            raise ValueError(f"Missing required keys: {key}")
                
                for key in tokens:
                    match key:
                        case  "WIDTH" | "HEIGHT":
                            if tokens[key] <= 0:
                                raise ValueError(f"Impossible maze dimensions: ({key} = {tokens[key]})")
                        case  "EXIT" | "ENTRY":
                            if tokens[key]["x"] < 0 or tokens[key]["y"] < 0:
                                raise ValueError(f"Unlogical maze {key}: ({tokens[key]['x'], tokens[key]['y']})")
                            if tokens["WIDTH"] <= tokens[key]["x"] or tokens["HEIGHT"] <= tokens[key]["y"]:
                                raise ValueError(f"Invalid maze {key}: ({tokens[key]['x'], tokens[key]['y']})")
                            if tokens["ENTRY"]["x"] == tokens["EXIT"]["x"] and tokens["ENTRY"]["y"] == tokens["EXIT"]["y"]:
                                raise ValueError(f"'ENTRY' and 'EXIT' cannot share the same coordinates")
                        
                return tokens
            except Exception as e:
                print(f"Config Error: {e}")
                sys.exit(1)

    class Recursive_Backtracker:
        def __init__(self, maze):
            self.maze = maze 
        def pattern_42(self):
            return {(0,0), (2,0), (0,1), (2,1), (0,2), (1,2), (2,2), (2,3), (2,4), (4,0), (5,0), (6,0), (6,1), (4,2), (5,2), (6,2), (4,3), (4,4), (5,4), (6,4)}
        def shape_patter_42(self, maze):
            pattern = self.pattern_42()
            pattern_height = max(y for _, y in pattern) + 1
            pattern_width = max(x for x, _ in pattern) + 1
            half_grid_h = (maze.shape[0] - 1) // 2
            half_grid_w = (maze.shape[1] - 1) // 2
            
            entry_tuple = (self.maze.entry["x"], self.maze.entry["y"])
            exit_tuple = (self.maze.exit["x"], self.maze.exit["y"])
            for y in range (1, half_grid_h - pattern_height):
                for x in range (1, half_grid_w - pattern_width):
                    possible_cells = {(x + pattern_x, y + pattern_y) for pattern_x, pattern_y in pattern}
                    if entry_tuple not in possible_cells and exit_tuple not in possible_cells:
                        return x, y
            raise ValueError(f"Cannot shape the pattern, Maze is too small ({self.maze.height}, {self.maze.width})")
            
            
        def grid_creator(self, height: int, width: int) -> n.ndarray:
            maze = n.full((height, width), 0xF,dtype=n.uint8)
            return maze
        
        @staticmethod
        def iterative_recursion_backtracker( maze, height, width, enx, eny, compass):
            random.shuffle(compass)
            stack_simulation = [(enx, eny, compass.copy())]
            visited_cells = {(enx, eny)}
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
        def maze_entry(self) -> n.ndarray:
            maze = self.grid_creator(self.maze.height, self.maze.width)
            compass = ["North", "South", "West", "East"]
            maze = self.iterative_recursion_backtracker(maze, self.maze.height, self.maze.width, self.maze.entry["x"], self.maze.entry["y"], compass)
            return maze
                    
        def imperfect_maze(self, maze, height, width, flawed):
            removeable_walls = []
            for y in range(1, height - 1):
                for x in range(1, width - 1):
                    if(maze[y,x] == 1):
                        if (maze[y+1, x] == 0 and maze[y-1, x] == 0) or (maze[y, x+1] == 0 and maze[y, x-1] == 0):
                            removeable_walls.append((y,x))
            random.shuffle(removeable_walls)
            for y, x in removeable_walls[:flawed]:
                maze[y, x] = 0
            return maze

        def BFS(self, maze, enx: int, eny: int, exx: int, exy: int) -> str:
            directions = {0: (0, -1, 'N'), 1: (1, 0, 'E'), 2: (0, 1, 'S'), 3: (-1, 0, 'W')} 
            queue = [(enx, eny, "")]
            visited = {(enx, eny)}
            height, width = maze.shape
            while queue:
                x, y, path = queue.pop(0)
                
                if (x, y) == (exx, exy):
                    return path
                
                for direction, (dx, dy, compass) in directions.items():

                    if not bool(self.maze[y, x] & (0x1 << direction)):
                        nx, ny = x + dx, y + dy
                        
                        if (0 < nx < width and 
                            0 < ny < height and
                            (nx, ny) not in visited):

                            visited.add((nx, ny))
                            queue.append((nx, ny, path + compass))
            
            return ""
                    

    
    @staticmethod
    def maze_hexadecimal(maze, output_file, height, width, entry_p, exit_p):
        with open(output_file, "w") as f:
            for y in range(height):  
                row_cells = []
                for x in range(width):  
                    cell_hex = maze[y, x]
                    row_cells.append(hex(cell_hex)[2:].upper())
                print("".join(row_cells), file=f)
            enx, eny = entry_p["x"], entry_p["y"]
            exx, exy = exit_p["x"], exit_p["y"]
            print(f"\n{enx},{eny}", file=f, end="\n")
            print(f"{exx},{exy}", file=f, end="\n")
            
    def combine(self):
        if self.seed is not None:
            random.seed(self.seed)
        
        generated_maze = self.maze.maze_entry()
        
        if not self.perfect and self.flawed is not None and self.flawed > 0:
            generated_maze = self.maze.imperfect_maze(generated_maze, self.height, self.width, self.flawed)
                
        if self.output_file:
            self.maze_hexadecimal(generated_maze, self.output_file, self.height, self.width, self.entry, self.exit)
            print(f"\nMaze saved to {self.output_file}")
        finder = self.BFSPathfinder(generated_maze)
        path = finder.find_path(0, 0, 19, 14)
        print(f"Path: {path}")
        print(f"Length: {len(path)} steps")
        

        
    def print_arguments(self):
        print(f"Height: {self.height}")
        print(f"Width: {self.width}")
        print(f"Entry Point: {self.entry}")
        print(f"Exit Point: {self.exit}")
        print(f"Output File: {self.output_file}")
        print(f"Seed: {self.seed}")
        print(f"Perfect: {self.perfect}")
        print(f"Flawed: {self.flawed}")
        
            
if __name__ == "__main__":
    maze = A_Maze_Ing()
    maze.combine()
