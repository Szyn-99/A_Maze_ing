import numpy as n
import random
from typing import Any, List, Dict, Union, Optional
from config_validator import Maze_config_analyzer as ConfigAnalyzer
from backtracker import MazeGenerationParts as MazeGenParts
from maze_renderer import Render_Maze


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
        self.generated_maze = MazeGenParts.iterative_backtracker(maze, self.height, self.width, self.entry, compass, self.exit, self.seed, True)
        if self.perfect == False:
            self.generated_maze = MazeGenParts.imperfect_maze(generated_maze, self.height, self.width, self.entry, self.exit, self.seed, True)
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


def main():
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

    compass = ["North", "East", "South", "West"]
    grid = n.full((height, width), 0xF, dtype=n.uint8)

    generated_maze, actions = MazeGenParts.iterative_backtracker(
        grid, height, width, entry, compass, exit_, seed, record=True
    )

    if not perfect:
        generated_maze = MazeGenParts.imperfect_maze(generated_maze, height, width)

    path = MazeGenParts.bfs(generated_maze, entry, exit_)

    renderer = Render_Maze(generated_maze, entry, exit_)
    renderer.animate(actions)
    renderer.display()



if __name__ == "__main__":
   main()

