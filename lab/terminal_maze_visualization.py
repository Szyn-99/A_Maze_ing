import numpy as n
import sys
import random
import time
import os

sys.setrecursionlimit(10000)
random.seed(42)

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def print_maze(maze, height, width, title="Generating Maze", clear=True):
    """Print the maze to terminal using ASCII characters"""
    if clear:
        clear_screen()
    print(f"\n{title}\n")
    
    for y in range(height):
        line = ""
        for x in range(width):
            if maze[y, x] == 1:
                line += "██"  # Wall
            else:
                line += "  "  # Path
        print(line)
    print(f"\nSize: {width}x{height}")
    sys.stdout.flush()

def print_maze_inline(maze, height, width, x_pos, y_pos, title=""):
    """Print maze with current position highlighted without clearing screen"""
    # Move cursor to top
    print("\033[H", end="")
    
    if title:
        print(f"\n{title}\n")
    
    for y in range(height):
        line = ""
        for x in range(width):
            # Highlight current position being carved
            if x == x_pos and y == y_pos:
                line += "\033[92m●●\033[0m"  # Green dot for current position
            elif maze[y, x] == 1:
                line += "██"  # Wall
            else:
                line += "  "  # Path
        print(line)
    print(f"\nSize: {width}x{height}")
    sys.stdout.flush()

def grid_creator(height: int, width: int) -> n.ndarray:
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1
    maze = n.ones((height, width), dtype=int)
    return maze

def recursive_backtracker(maze, x, y, height, width, live=True, delay=0.1, step_counter=[0]) -> None:
    maze[y, x] = 0
    
    # Update visualization if live mode is on
    if live:
        step_counter[0] += 1
        # Update display to show current carving position
        print_maze_inline(maze, height, width, x, y, f"Generating Maze - Step {step_counter[0]} - Carving at ({x},{y})")
        time.sleep(delay)

    directions = ["north", "south", "west", "east"]
    random.shuffle(directions)
    for move in directions:
        if move == "north" and y > 1 and maze[y-2, x] == 1:
            maze[y-1, x] = 0
            recursive_backtracker(maze, x, y-2, height, width, live, delay, step_counter)
        elif move == "south" and y < height - 2 and maze[y+2, x] == 1:
            maze[y+1, x] = 0
            recursive_backtracker(maze, x, y+2, height, width, live, delay, step_counter)
        elif move == "west" and x > 1 and maze[y, x-2] == 1:
            maze[y, x-1] = 0
            recursive_backtracker(maze, x-2, y, height, width, live, delay, step_counter)
        elif move == "east" and x < width - 2 and maze[y, x+2] == 1:
            maze[y, x+1] = 0
            recursive_backtracker(maze, x+2, y, height, width, live, delay, step_counter)

def generate_maze(height: int, width: int, live=True, delay=0.01) -> n.ndarray:
    maze = grid_creator(height, width)
    
    if live:
        clear_screen()
        print_maze(maze, height, width, "Starting Maze Generation...", clear=False)
        time.sleep(0.5)
    
    step_counter = [0]
    recursive_backtracker(maze, 1, 1, height, width, live, delay, step_counter)
    
    if live:
        # Final display
        print("\n" + "=" * 60)
        print(f"Maze Generation Complete! Total steps: {step_counter[0]}")
        print("=" * 60)
    
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
    # Use smaller size for terminal visualization (terminal has limited space)
    h, w = 21, 21  # Odd numbers work best
    
    print("=" * 60)
    print("TERMINAL MAZE GENERATOR")
    print("=" * 60)
    print("\nControls:")
    print("  - live=True:  See real-time generation")
    print("  - live=False: Generate instantly")
    print("  - delay: Controls animation speed (0.001 to 0.1)")
    print("\nLegend:")
    print("  ██ = Wall")
    print("     = Path")
    print("  ●● = Current carving position (green)")
    print("\nStarting in 2 seconds...")
    time.sleep(2)
    
    # Generate maze with live visualization
    maze = generate_maze(h, w, live=True, delay=0.02)
    
    print("\n\nAdding imperfections...")
    time.sleep(1)
    maze = imperfect_maze(maze, h, w, 10)
    
    clear_screen()
    print_maze(maze, h, w, "Final Maze with Imperfections", clear=False)
    
    print("\n" + "=" * 60)
    print("Maze generation complete!")
    print("=" * 60)
    
    # Save to file (optional)
    try:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 10))
        plt.imshow(maze, cmap='binary') 
        plt.title(f"Maze {maze.shape[1]}x{maze.shape[0]}")
        plt.axis('off') 
        output_file = 'terminal_maze.png'
        plt.savefig(output_file)
        print(f"\nMaze also saved to: {output_file}")
    except:
        print("\nMatplotlib not available for saving image file")
