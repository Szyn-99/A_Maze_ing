import numpy as n
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import sys
import random

sys.setrecursionlimit(10000)
random.seed(42)

def grid_creator(height: int, width: int) -> n.ndarray:
    # Force dimensions to be odd to ensure a solid outer wall border
    h = height if height % 2 != 0 else height + 1
    w = width if width % 2 != 0 else width + 1
    return n.ones((h, w), dtype=int)

def recursive_backtracker(maze, x, y, exx, exy) -> bool:
    maze[y, x] = 0 # Mark as visited (path)
    
    # Base Case: Did we find the exit?
    found = (x == exx and y == exy)

    directions = ["north", "south", "west", "east"]
    random.shuffle(directions)
    h, w = maze.shape

    for move in directions:
        # Step by 2 to jump over the wall to the next cell
        if move == "north":   nx, ny, wx, wy = x, y-2, x, y-1
        elif move == "south": nx, ny, wx, wy = x, y+2, x, y+1
        elif move == "west":  nx, ny, wx, wy = x-2, y, x-1, y
        elif move == "east":  nx, ny, wx, wy = x+2, y, x+1, y
        else: continue

        # Check if the neighbor is within the inner grid and is unvisited (1)
        if 0 < nx < w-1 and 0 < ny < h-1 and maze[ny, nx] == 1:
            maze[wy, wx] = 0 # Carve the wall between
            if recursive_backtracker(maze, nx, ny, exx, exy):
                found = True
                maze[wy, wx] = 42 # Mark the wall as the solution path
    
    if found:
        maze[y, x] = 42 # Mark the cell as the solution path
    return found

def generate_maze(height: int, width: int, entry: tuple, exit_pt: tuple) -> n.ndarray:
    maze = grid_creator(height, width)
    h, w = maze.shape
    
    # Snap the algorithm's internal start/end to the nearest odd "Cells"
    # This prevents the "corrupted" floating wall look.
    alg_sx, alg_sy = (entry[0]//2*2+1, entry[1]//2*2+1)
    alg_ex, alg_ey = (exit_pt[0]//2*2+1, exit_pt[1]//2*2+1)
    
    # Ensure they stay inside the 1-pixel border
    alg_sx, alg_sy = max(1, min(alg_sx, w-2)), max(1, min(alg_sy, h-2))
    alg_ex, alg_ey = max(1, min(alg_ex, w-2)), max(1, min(alg_ey, h-2))

    # Run generator
    recursive_backtracker(maze, alg_sx, alg_sy, alg_ex, alg_ey)
    
    # BRIDGE: Connect your specific requested entry/exit to the path
    # This carves through the outer wall if your point was at (0, y) or (x, 0)
    for (px, py), (ax, ay) in [(entry, (alg_sx, alg_sy)), (exit_pt, (alg_ex, alg_ey))]:
        # Carve a straight line from requested point to algorithm cell
        x_range = range(min(px, ax), max(px, ax) + 1)
        y_range = range(min(py, ay), max(py, ay) + 1)
        for ix in x_range: maze[py, ix] = 42
        for iy in y_range: maze[iy, ax] = 42
            
    return maze

if __name__ == "__main__":
    # Settings
    h, w = 41, 81  # Height and Width
    start_pt = (1, 1)  # Entrance on the left wall
    end_pt = (w-1, h-2) # Exit on the right wall
    
    maze = generate_maze(h, w, start_pt, end_pt)

    # VISUALIZATION FIX:
    # Define a colormap: 0=Path (White), 1=Wall (Black), 42=Solution (Neon Green)
    # We use a dictionary to map values to colors correctly.
    cmap = ListedColormap(['white', 'black'])
    # To handle the 42 value easily, we can normalize or just use a logic check
    display_maze = n.copy(maze)
    
    plt.figure(figsize=(15, 7))
    # We use 'gist_ncar' or 'prism' for high contrast, 
    # but binary with a mask for the path is cleanest:
    plt.imshow(maze == 1, cmap='binary') # Walls as Black, Paths as White
    
    # Overlay the solution path in color
    path_mask = n.ma.masked_where(maze != 42, maze)
    plt.imshow(path_mask, cmap='hsv', alpha=1) # Path as bright color
    
    plt.title(f"Solved Maze {w}x{h} (Entry: {start_pt}, Exit: {end_pt})")
    plt.axis('off')
    plt.show()