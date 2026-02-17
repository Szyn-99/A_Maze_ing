import numpy as n
import sys
import random
from typing import Any, List, Dict, Union, Optional

class A_Maze_Ing:
    def __init__(self):
        self.tokens = self.Maze_config_analyzer.parsing_config_data()
        self.width = self.tokens["WIDTH"]
        self.height = self.tokens["HEIGHT"]
        self.entry = self.tokens["ENTRY"]
        self.exit = self.tokens["EXIT"]
        self.output_file = self.tokens["OUTPUT_FILE"]
        self.seed = self.tokens["SEED"]
        self.perfect = self.tokens["PERFECT"]
        self.flawed = self.tokens["FLAWED"]
        self.maze = self.MazeGenerationParts(self)

    class Maze_config_analyzer:
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
                            try:
                                x, y = map(int, value.split(","))
                                tokens[key] = {"x": x, "y": y}
                            except ValueError:
                                raise ValueError(f"Invalid/Missing {key} value")

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

    class MazeGenerationParts:
        def __init__(self, maze):
            self.maze = maze

        @staticmethod
        def iterative_backtracker(maze, height, width, enx, eny, compass):
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
        @staticmethod
        def bfs(maze, enx: int, eny: int, exx: int, exy: int) -> str:
            directions = {0: (0, -1, 'N'), 1: (1, 0, 'E'), 2: (0, 1, 'S'), 3: (-1, 0, 'W')} 
            queue = [(enx, eny, "")]
            visited = {(enx, eny)}
            height, width = maze.shape
            while queue:
                x, y, path = queue.pop(0)
                
                if (x, y) == (exx, exy):
                    return path
                
                for direction, (dx, dy, compass) in directions.items():

                    if not bool(maze[y, x] & (0x1 << direction)):
                        nx, ny = x + dx, y + dy
                        
                        if (0 <= nx < width and 
                            0 <= ny < height and
                            (nx, ny) not in visited):

                            visited.add((nx, ny))
                            queue.append((nx, ny, path + compass))

            return "No path found"
        
    @staticmethod
    def maze_hexadecimal(maze, output_file, height, width, entry_p, exit_p, path):
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
            print(f"{path}", file=f, end="\n")


    def start(self):
        print(f"Height: {self.height}")
        print(f"Width: {self.width}")
        print(f"Entry Point: {self.entry}")
        print(f"Exit Point: {self.exit}")
        print(f"Output File: {self.output_file}")
        print(f"Seed: {self.seed}")
        print(f"Perfect: {self.perfect}")
        print(f"Flawed: {self.flawed}")
        if self.seed:
            random.seed(self.seed)
        compass = ["North", "East", "South", "West"]
        maze = n.full((self.height, self.width), 0xF,dtype=n.uint8)
        generated_maze = self.MazeGenerationParts.iterative_backtracker(maze, self.height, self.width, self.entry['x'], self.entry['y'], compass)
        path = self.MazeGenerationParts.bfs(generated_maze, self.entry['x'], self.entry['y'], self.exit['x'], self.exit['y'])
        print(f"{path}")
        self.maze_hexadecimal(generated_maze, self.output_file, self.height, self.width, self.entry, self.exit, path)
        
            
if __name__ == "__main__":
    maze = A_Maze_Ing()
    maze.start()
