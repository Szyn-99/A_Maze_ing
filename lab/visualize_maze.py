import numpy as m
import matplotlib.pyplot as plt
import sys
import random

seed = 42
m.random.seed(seed)
# Increase recursion depth for deep mazes
sys.setrecursionlimit(2000)

def maze_creator(width: int, height: int) -> list:
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1
    
    # Initialize with 0 (Walls)
    maze = m.zeros((height, width), dtype=float)
    
    # Set unvisited cells to 0.5
    for i in range(1, height, 2):
        for j in range(1, width, 2):
            maze[i][j] = 0.5
            
    return maze

def recursive_backtracker(maze, x, y) -> None:
    # Mark current cell as Visited (1.0)
    maze[y, x] = 1.0
    
    directions = ["north", "south", "west", "east"]
    # Shuffle directions to ensure random exploration without getting stuck in a while true loop
    m.random.shuffle(directions)
    
    for move in directions:
        if move == "north" and y > 1 and maze[y-2, x] == 0.5:
            maze[y-1, x] = 1.0 # Carve wall
            recursive_backtracker(maze, x, y-2)
        elif move == "south" and y < maze.shape[0] - 2 and maze[y+2, x] == 0.5:
            maze[y+1, x] = 1.0 # Carve wall
            recursive_backtracker(maze, x, y+2)
        elif move == "west" and x > 1 and maze[y, x-2] == 0.5:
            maze[y, x-1] = 1.0 # Carve wall
            recursive_backtracker(maze, x-2, y)
        elif move == "east" and x < maze.shape[1] - 2 and maze[y, x+2] == 0.5:
            maze[y, x+1] = 1.0 # Carve wall
            recursive_backtracker(maze, x+2, y)

def generate_maze(width: int, height: int) -> list:
    maze = maze_creator(width, height)
    # Start at 1,1
    recursive_backtracker(maze, 1, 1)
    return maze
def imperfect_maze(maze, imperfection_rate, height, width) -> None:
    removeable_walls = []
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if maze[y][x] == 0:
                if (maze[y+1, x] == 1 and maze[y-1, x] == 1) or (maze[y, x+1] == 1 and maze[y, x-1] == 1):
                    removeable_walls += [(x, y)]
    random.shuffle(removeable_walls)
    for x, y in removeable_walls[:imperfection_rate]:
        maze[y,x] = 1
    return maze

if __name__ == "__main__":
    # Generate a maze
    width, height = 50, 50
    maze = generate_maze(width, height)
    print(maze)
    maze = imperfect_maze(maze, 4, height, width)
    # Visualization
    plt.figure(figsize=(10, 10))
    # Display the maze: Walls (0) will be purple/dark, Path (1) will be yellow/light
    plt.imshow(maze) 
    plt.title(f"Maze {width}x{height}")
    plt.axis('off')
    
    output_file = 'maze_visualization.png'
    plt.savefig(output_file)
    print(f"Maze visualization saved to {output_file}")
