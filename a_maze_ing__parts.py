import numpy as m
import enum as en
import numpy as m
import matplotlib.pyplot as plt
import sys
import random
sys.setrecursionlimit(10000)

def maze_creator(height: int, width: int) -> list:
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1
    #(rows, columns) {matrix indexing} ==> row = heigth, column = width
    maze = m.ones((height, width),dtype=int)
    return maze


def recursive_backtracker(maze, height: int, width: int, x, y) -> None:
    maze[y,x] = 0

    directions = ["north", "south", "west", "east"]
    random.shuffle(directions)
    for move in directions:
        if move == "north" and y > 1 and maze[y-2, x] == 1:
            maze[y-1, x] = 0
            recursive_backtracker(maze, height, width, x, y-2)
        elif move == "south" and y < height - 2 and maze[y+2, x] == 1:
            maze[y+1, x] = 0
            recursive_backtracker(maze, height, width, x, y+2)
        elif move == "west" and x > 1 and maze[y, x-2] == 1:
            maze[y, x-1] = 0
            recursive_backtracker(maze, height, width, x-2, y)
        elif move == "east" and x < width - 2 and maze[y, x+2] == 1:
            maze[y, x+1] = 0
            recursive_backtracker(maze, height, width, x+2, y)

def generate_maze(height: int, width: int) -> list:
    maze = maze_creator(height, width)
    # Start at 1,1
    recursive_backtracker(maze, height, width, 1, 1)
    return maze

if __name__ == "__main__":
    # Generate a maze
    height, width = 100, 100
    maze = generate_maze(height, width)
    print(maze)
    # maze = imperfect_maze(maze, 4, height, width)
    # Visualization
    plt.figure(figsize=(10, 10))
    # Display the maze: Walls (0) will be purple/dark, Path (1) will be yellow/light
    plt.imshow(maze) 
    plt.title(f"Maze {width}x{height}")
    plt.axis('off')
    
    output_file = 'maze_visualization.png'
    plt.savefig(output_file)
    print(f"Maze visualization saved to {output_file}")