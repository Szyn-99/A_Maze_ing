import numpy as n
import random
from typing import Any, List, Dict, Union, Optional
from config_validator import Maze_config_analyzer as ConfigAnalyzer
from backtracker import MazeGenerationParts as MazeGenParts
class A_Maze_Ing:
    def __init__(self, height, width, entry, exit_, perfect, output_file, seed):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit_
        self.output_file = output_file
        self.seed = seed
        self.perfect = perfect
        self.generated_maze = None
        self.path = None

    def get_entry(self):
        return self.entry
    def get_exit(self):
        return self.exit
    def get_maze(self):
        return self.generated_maze
    def bring_maze(self):
        compass = ["North", "East", "South", "West"]
        maze = n.full((self.height, self.width), 0xF,dtype=n.uint8)
        self.generated_maze = MazeGenParts.iterative_backtracker(maze, self.height, self.width, self.entry, compass, self.exit, self.seed)
        if self.perfect == False:
            self.generated_maze = MazeGenParts.imperfect_maze(generated_maze, self.height, self.width, self.entry, self.exit, self.seed)
        return self.generated_maze

    def get_grid(self):
        grid = n.full((self.height, self.width), 0xF,dtype=n.uint8)
        return grid

    def get_path(self, generated_maze):
        self.path = MazeGenParts.bfs(generated_maze, self.entry, self.exit)
        return self.path

    def maze_hexadecimal(self):
        with open(self.output_file, "w") as f:
            for y in range(self.height):  
                row_cells = []
                for x in range(self.width):  
                    cell_hex = self.generated_maze[y, x]
                    row_cells.append(hex(cell_hex)[2:].upper())
                print("".join(row_cells), file=f)
            enx, eny = self.entry
            exx, exy = self.exit
            print(f"\n{enx},{eny}", file=f, end="\n")
            print(f"{exx},{exy}", file=f, end="\n")
            print(f"{self.path}", file=f, end="\n")

if __name__ == "__main__":
    parsed_config = ConfigAnalyzer.parse_and_validate()
    entry = tuple(parsed_config["ENTRY"].values())
    exit_ = tuple(parsed_config["EXIT"].values())
    width = parsed_config["WIDTH"]
    height = parsed_config["HEIGHT"]
    output_file = parsed_config["OUTPUT_FILE"]
    perfect = parsed_config["PERFECT"]
    seed = parsed_config["SEED"]
    if seed:
        random.seed(seed)
    maze = A_Maze_Ing(height, width, entry, exit_, perfect, output_file, seed)
    generated_maze = maze.bring_maze()
    print(generated_maze)
    grid = maze.get_grid()
    print(grid)
    path = maze.get_path(generated_maze)
    print(path)
    entry_p = maze.get_entry()
    print(entry_p)
    exit_p = maze.get_exit()
    print(exit_p)
    maze.maze_hexadecimal()
    
    
    
