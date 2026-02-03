import numpy as n
import matplotlib.pyplot as plt
import sys
import random
sys.setrecursionlimit(50000)  # Increased for larger mazes
random.seed(42)

def grid_creator(height: int, width: int) -> n.ndarray:
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1
    maze = n.ones((height, width), dtype=int)
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

def generate_maze(height: int, width: int, entry_x, entry_y) -> n.ndarray:
    maze = grid_creator(height, width)
    actual_height, actual_width = maze.shape  # Get actual dimensions after making odd
    
    # Store original entry coordinates
    original_entry_x, original_entry_y = entry_x, entry_y
    
    # Make entry coordinates odd and within bounds
    entry_x = entry_x if entry_x % 2 != 0 else entry_x + 1
    entry_y = entry_y if entry_y % 2 != 0 else entry_y + 1
    entry_x = min(entry_x, actual_width - 2)
    entry_y = min(entry_y, actual_height - 2)
    
    # Generate the maze starting from the adjusted entry point
    recursive_backtracker(maze, int(entry_x), int(entry_y), actual_height, actual_width)
    
    # Mark the original entry point as a path (in case it was even)
    maze[original_entry_y, original_entry_x] = 0
    
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

    h, w = 200, 200
    maze = generate_maze(h, w, 19, 14)
    # maze = imperfect_maze(maze, h, w, 1000)
    plt.figure(figsize=(10, 10))

    plt.imshow(maze, cmap='binary') 
    
    plt.title(f"Maze {maze.shape[1]}x{maze.shape[0]}")
    plt.axis('off') 
    
    output_file = 'maze_py_py.png'
    plt.savefig(output_file)
    print(f"Maze visualization saved to {output_file}")
