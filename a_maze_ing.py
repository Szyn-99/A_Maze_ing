import numpy as n
import sys
import random
sys.setrecursionlimit(50000)

class A_Maze_Ing:
    def __init__(self):
        tokens = self.Maze_Config_Analyzer.Combining_rules()
        self.width = tokens["WIDTH"]
        self.height = tokens["HEIGHT"]
        self.entry = tokens["ENTRY"]
        self.exit = tokens["EXIT"]
        self.output_file = tokens["OUTPUT_FILE"]
        self.seed = tokens["SEED"]
        self.perfect = tokens["PERFECT"]
        self.flawed = tokens["FLAWED"]
        self.maze = self.Recursive_Backtracker(self)

    class Maze_Config_Analyzer:
        @staticmethod
        def is_empty(output_file: str) -> bool:
            for i in output_file:
                if i != " ":
                    return False
            return True
        @staticmethod
        def validate_lines(config_lines: list[str]) -> dict[str, int | str | dict | None]:
            tokens = {
                "WIDTH": 0,
                "HEIGHT": 0,
                "EXIT": {"x": 0, "y": 0},
                "ENTRY": {"x": 0, "y": 0},
                "OUTPUT_FILE": None,
                "PERFECT": 0,
                "FLAWED": 0,
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
                        tokens[key] = int(value)

                    case "OUTPUT_FILE":
                        if len(value.split()) > 1:
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
                elif value_count <= 0 and key is not "SEED" or key is not "FLAWED":
                    raise ValueError(f"Missing required keys: {key}")
             
            for key in tokens:
                match key:
                    case  "WIDTH" | "HEIGHT":
                        if tokens[key] <= 0 or tokens[key] <= 0:
                            raise ValueError(f"Impossible maze dimensions: ({tokens[key]["x"], tokens[key]["y"]})")
                    case  "EXIT" | "ENTRY":
                        if tokens[key]["x"] < 0 or tokens[key]["y"] < 0:
                            raise ValueError(f"Unlogical maze {key}: ({tokens[key]["x"], tokens[key]["y"]})")
                        if tokens["WIDTH"] <= tokens[key]["x"] or tokens["HEIGHT"] <= tokens[key]["y"]:
                            raise ValueError(f"Invalid maze {key}: ({tokens[key]["x"], tokens[key]["y"]})")
                        if tokens["ENTRY"]["x"] == tokens["EXIT"]["x"] and tokens["ENTRY"]["y"] == tokens["EXIT"]["y"]:
                            raise ValueError(f"'ENTRY' and 'EXIT cannot share the same coordinates")
                    
            return tokens

        @staticmethod
        def Combining_rules(self) -> dict:
            try:
                if len(sys.argv) > 2:
                    raise ValueError("Too many arguments provided. Only the configuration file path is required.")
                elif len(sys.argv) < 2:
                    raise ValueError("No configuration file provided. Please provide the path to the configuration file.")
                config_file = sys.argv[1]
                with open(config_file, "r") as f:
                    config_lines = [line.strip() for line in f]
                tokens = self.Maze_Config_Analyzer.validate_lines(config_lines)
                return tokens
            except Exception as e:
                print("An Error Occured: ->", end=" ")
                print(f"Type: {e.__class__.__name__} Details: {e}")
                sys.exit(1)  
        def print_tokens(tokens: dict) -> None:
            for tok in tokens:
                print(f"{tok} -> {tokens[tok]}")
    def generate_maze(self):
        tokens = self.Maze_Config_Analyzer.Combining_rules()
        self.Maze_Config_Analyzer.print_tokens(tokens)
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
        
        def recursive_backtracker(self, maze, enx, eny, height, width, exx, exy, path_way):
            maze[eny, enx] = 0
            path = (enx, eny) == (exx, exy)
            directions = ["north", "south", "west", "east"]
            stack_simulation = []
            random.shuffle(directions)
            for move in directions:
                if move == "north" and eny > 1 and maze[eny-2, enx] == 1:
                    maze[eny-1, enx] = 0
                    if self.recursive_backtracker(maze, enx, eny-2, height, width, exx, exy, path_way)[0]:
                        path = True
                        maze[eny-1, enx] = 42
                        path_way.append("N")  # Went north during exploration
                elif move == "south" and eny < height - 2 and maze[eny+2, enx] == 1:
                    maze[eny+1, enx] = 0
                    if self.recursive_backtracker(maze, enx, eny+2, height, width, exx, exy, path_way)[0]:
                        path = True
                        maze[eny+1, enx] = 42
                        path_way.append("S")  # Went south during exploration
                elif move == "west" and enx > 1 and maze[eny, enx-2] == 1:
                    maze[eny, enx-1] = 0
                    if self.recursive_backtracker(maze, enx-2, eny, height, width, exx, exy, path_way)[0]:
                        path = True
                        maze[eny, enx-1] = 42
                        path_way.append("W")  # Went west during exploration
                elif move == "east" and enx < width - 2 and maze[eny, enx+2] == 1:
                    maze[eny, enx+1] = 0
                    if self.recursive_backtracker(maze, enx+2, eny, height, width, exx, exy, path_way)[0]:
                        path = True
                        maze[eny, enx+1] = 42
                        path_way.append("E")  # Went east during exploration
            if path:
                maze[eny, enx] = 42
            return path, path_way
        
        def generate_maze(self, height: int, width: int, entry_point: tuple, exit_point: tuple) -> n.ndarray:
    
            maze = self.grid_creator(height, width)
            
            entry_x , entry_y = entry_point
            exit_x , exit_y = exit_point
            
            if entry_x == 0 or entry_y == 0 or entry_x >= width - 1 or entry_y >= height - 1:
                raise ValueError(f"Invalid Entry ({entry_x}, {entry_y}): entry cannot be on the maze boundary.")
            if exit_x == 0 or exit_y == 0 or exit_x >= width - 1 or exit_y >= height - 1:
                raise ValueError(f"Invalid Exit ({exit_x}, {exit_y}): exit cannot be on the maze boundary.")

            valid_point = self.shape_patter_42(maze)
            if valid_point:
                pattern = self.pattern_42()
                x, y = valid_point
                for pattern_x, pattern_y in pattern:
                    valid_cell_x = (x + pattern_x) * 2 + 1
                    valid_cell_y = (y + pattern_y) * 2 + 1
                    maze[valid_cell_y, valid_cell_x] = 0xf
            path_way = []
            self.recursive_backtracker(maze, entry_x, entry_y, height, width, exit_x, exit_y, path_way)
            maze[entry_y, entry_x] = 0xE
            maze[exit_y, exit_x] = 0xE2

            return maze, path_way
        
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
        
        def maze_bringer(self):
            try:
                entry  = (self.maze.entry["x"], self.maze.entry["y"],)
                exit = (self.maze.exit["x"], self.maze.exit["y"],)
                perfect = True if 'True' in self.maze.perfect else False
                flawed = self.maze.flawed
                seed = self.maze.seed
                height = self.maze.height
                width = self.maze.width
                
                if flawed is None:
                    flawed = 0
                if seed is not None:
                    random.seed(seed)
                if width % 2 == 0:
                    width += 1
                if height % 2 == 0:
                    height += 1
                
                
                self.maze.width = width
                self.maze.height = height
                
                maze, path_way = self.generate_maze(height, width, entry, exit)
                if not perfect:
                    maze = self.imperfect_maze(maze, height, width, flawed)
                
                return maze, path_way
            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)

    @staticmethod
    def maze_printer(maze):
        
        RESET = "\033[0m"
        WALL  = "\033[40m  "           
        PATH  = "\033[48;5;254m  "    
        SYM   = "\033[48;5;250m░░"    
        START = "\033[48;5;129m  "    
        END   = "\033[48;5;196m  "
        
        mapping = {
            0: PATH,
            1: WALL,
            0xE: START,
            0xE2: END,
            42: SYM
        }
        for row in maze:
            for cell in row:
                print(mapping.get(cell, PATH), end="")
            print(RESET)
    @staticmethod
    def maze_hexadecimal(maze, output_file, height, width, entry_p, exit_p, path_way):
        path_from_entry_to_exit = list(reversed(path_way))
        
        with open(output_file, "w+") as f:
            for y in range(1, height-1 , 2):  
                row_cells = []
                for x in range(1, width-1, 2):  
                    cell_hex = 0
                    if maze[y-1][x] == 1: cell_hex += 1 #North
                    if maze[y+1][x] == 1: cell_hex += 4 #South
                    if maze[y][x+1] == 1: cell_hex += 2 #East
                    if maze[y][x-1] == 1: cell_hex += 8 #West
                    row_cells.append(hex(cell_hex)[2:].upper())
                print("".join(row_cells), file=f)
            enx, eny, = entry_p["x"], entry_p["y"]
            exx, exy, = exit_p["x"], exit_p["y"]
            print(f"\n{enx},{eny}", file=f, end="\n")
            print(f"{exx},{exy}", file=f, end="\n")
            for direction in path_from_entry_to_exit:
                print(direction, file=f, end="")
            print(file=f, end="\n")
            
    
        
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
    # maze.print_arguments()
    maze.generate_maze()
