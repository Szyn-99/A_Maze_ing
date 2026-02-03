import numpy as np
import matplotlib.pyplot as plt
import sys
import random

sys.setrecursionlimit(10000)
random.seed(42)
def maze_creator(height: int, width: int) -> np.ndarray:
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1

    maze = np.ones((height, width), dtype=int)
    return maze

def recursive_backtracker(maze, x, y, height, width) -> None:
    maze[y, x] = 0

    directions = ["north", "south", "west", "east"]
    random.shuffle(directions)
    for move in directions:
        if move == "north" and y > 1 and maze[y-2, x] == 1:
            maze[y-1, x] = 0
            recursive_backtracker(maze, x, y-2, height, width)
        elif move == "south" and y < height - 2 and maze[y+2, x] == 1:
            maze[y+1, x] = 0
            recursive_backtracker(maze, x, y+2, height, width)
        elif move == "west" and x > 1 and maze[y, x-2] == 1:
            maze[y, x-1] = 0
            recursive_backtracker(maze, x-2, y, height, width)
        elif move == "east" and x < width - 2 and maze[y, x+2] == 1:
            maze[y, x+1] = 0
            recursive_backtracker(maze, x+2, y, height, width)

def generate_maze(height: int, width: int) -> np.ndarray:
    maze = maze_creator(height, width)
    recursive_backtracker(maze, 19, 19, height, width)
    return maze


def imperfect_maze(maze, height, width, imperfection_rate) :
    removeable_walls = []
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if(maze[y,x] == 1):
                if (maze[y+1, x] == 0 and maze[y-1, x] == 0) or (maze[y, x+1] == 0 and maze[y, x-1] == 0):
                    removeable_walls.append((y,x))
    random.shuffle(removeable_walls)
    for y, x in removeable_walls[:imperfection_rate]:
        maze[y, x] = 0
    return maze


if __name__ == "__main__":

    h, w = 21, 21 
    maze = generate_maze(h, w)
    maze = imperfect_maze(maze, h, w, 8)
    plt.figure(figsize=(10, 10))

    plt.imshow(maze, cmap='binary') 
    
    plt.title(f"Maze {maze.shape[1]}x{maze.shape[0]}")
    plt.axis('off') 
    
    output_file = 'maze_py_py.png'
    plt.savefig(output_file)
    print(f"Maze visualization saved to {output_file}")
