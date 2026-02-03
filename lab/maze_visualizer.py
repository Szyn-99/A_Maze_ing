import numpy as np
import sys
import time
import os

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def visualize_maze_animated(maze, delay=0.001, title="Maze Visualization"):
    """
    Animate the maze by revealing it row by row
    
    Args:
        maze: numpy array where 0=path, 1=wall
        delay: time delay between updates (seconds)
        title: title to display
    """
    height, width = maze.shape
    
    # Clear screen and show title
    clear_screen()
    print(f"\n{title}\n")
    print(f"Size: {width}x{height}")
    print("\nRevealing maze row by row...\n")
    time.sleep(1)
    
    # Animate row by row
    for y in range(height):
        line = ""
        for x in range(width):
            if maze[y, x] == 1:
                line += "\033[40m  \033[0m"  # Wall (black background)
            else:
                line += "\033[47m  \033[0m"  # Path (white background)
        
        # Add row indicator
        print(line + f"  \033[90m← Row {y+1}/{height}\033[0m")
        sys.stdout.flush()
        time.sleep(delay)
    
    print("\n\033[92m✓ Maze visualization complete!\033[0m")
    time.sleep(0.5)

def visualize_maze_build(maze, delay=0.001, title="Building Maze"):
    """
    Animate the maze being built cell by cell from top-left to bottom-right
    
    Args:
        maze: numpy array where 0=path, 1=wall
        delay: time delay between cell reveals (seconds)
        title: title to display
    """
    height, width = maze.shape
    display_maze = np.full((height, width), -1, dtype=int)  # -1 means not revealed yet
    
    cell_count = 0
    total_cells = height * width
    
    # Initial display
    clear_screen()
    print(f"\n{title}\n")
    print(f"Size: {width}x{height}")
    print(f"Progress: 0/{total_cells} cells (0%)")
    print("\nLegend: \033[90m░░\033[0m = Unrevealed  \033[40m  \033[0m = Wall  \033[47m  \033[0m = Path  \033[92m●●\033[0m = Current\n")
    
    for y in range(height):
        for x in range(width):
            # Reveal this cell
            display_maze[y, x] = maze[y, x]
            cell_count += 1
            
            # Only update display every few cells to reduce flickering
            if cell_count % 3 == 0 or cell_count == total_cells:
                # Use ANSI codes to move cursor and update without full clear
                print("\033[4;0H", end="")  # Move cursor to line 4
                print(f"Progress: {cell_count}/{total_cells} cells ({100*cell_count//total_cells}%)  ")
                print("\033[7;0H", end="")  # Move cursor to line 7 (after legend)
                
                for row_y in range(height):
                    line = ""
                    for row_x in range(width):
                        if display_maze[row_y, row_x] == -1:
                            line += "\033[90m░░\033[0m"  # Not revealed yet (gray)
                        elif display_maze[row_y, row_x] == 1:
                            line += "\033[40m  \033[0m"  # Wall (black background)
                        else:
                            line += "\033[47m  \033[0m"  # Path (white background)
                        
                        # Highlight current position
                        if row_y == y and row_x == x:
                            line = line[:-11] + "\033[42;92m●●\033[0m"  # Green background + green dot
                            
                    print(line + "\033[K")  # \033[K clears to end of line
                
                sys.stdout.flush()
                time.sleep(delay)
    
    # Final message
    print("\n\033[92m✓ Maze built! Total cells: {}\033[0m".format(total_cells))
    time.sleep(0.5)

def visualize_maze_static(maze, title="Final Maze"):
    """
    Display the maze without animation
    
    Args:
        maze: numpy array where 0=path, 1=wall
        title: title to display
    """
    height, width = maze.shape
    
    print(f"\n{title}\n")
    print(f"Size: {width}x{height}\n")
    
    for y in range(height):
        line = ""
        for x in range(width):
            if maze[y, x] == 1:
                line += "\033[40m  \033[0m"  # Wall (black background)
            else:
                line += "\033[47m  \033[0m"  # Path (white background)
        print(line)
    
    print()

def visualize_maze_with_markers(maze, entry=None, exit=None, path=None, title="Maze with Markers"):
    """
    Display maze with entry, exit, and optional solution path highlighted
    
    Args:
        maze: numpy array where 0=path, 1=wall
        entry: tuple (x, y) for entry point
        exit: tuple (x, y) for exit point
        path: list of (x, y) tuples for solution path
        title: title to display
    """
    height, width = maze.shape
    
    print(f"\n{title}\n")
    print(f"Size: {width}x{height}\n")
    print("Legend:")
    print("  \033[40m  \033[0m = Wall (Black)")
    print("  \033[47m  \033[0m = Path (White)")
    if entry:
        print("  \033[42m  \033[0m = Entry (Green)")
    if exit:
        print("  \033[41m  \033[0m = Exit (Red)")
    if path:
        print("  \033[43m  \033[0m = Solution Path (Yellow)")
    print()
    
    for y in range(height):
        line = ""
        for x in range(width):
            # Check if this is a special position
            if entry and (x, y) == entry:
                line += "\033[42m  \033[0m"  # Green entry (green background)
            elif exit and (x, y) == exit:
                line += "\033[41m  \033[0m"  # Red exit (red background)
            elif path and (x, y) in path:
                line += "\033[43m  \033[0m"  # Yellow path (yellow background)
            elif maze[y, x] == 1:
                line += "\033[40m  \033[0m"  # Wall (black background)
            else:
                line += "\033[47m  \033[0m"  # Path (white background)
        print(line)
    
    print()
    if entry:
        print(f"🟢 Entry: {entry}")
    if exit:
        print(f"🔴 Exit: {exit}")
    if path:
        print(f"📍 Path length: {len(path)} steps")
    print()


# Example usage and demo
if __name__ == "__main__":
    # Import the maze generator
    from amz_recursive_backtracker import generate_maze
    
    print("=" * 60)
    print("MAZE VISUALIZER DEMO")
    print("=" * 60)
    print("\nGenerating maze...")
    
    height, width = 31, 31
    maze = generate_maze(height, width, 8, 1)
    
    print("Maze generated successfully!")
    print("\nChoose visualization style:")
    print("  1. Cell-by-cell reveal (slower, detailed)")
    print("  2. Row-by-row reveal (faster)")
    print("  3. Static display with entry/exit")
    
    choice = input("\nEnter choice (1-3, or press Enter for default): ").strip()
    
    if choice == "2":
        print("\nStarting row-by-row visualization in 2 seconds...")
        time.sleep(2)
        visualize_maze_animated(maze, delay=0.1, title="Row-by-Row Maze Reveal")
    elif choice == "3":
        print("\nDisplaying static maze...")
        time.sleep(1)
        clear_screen()
    else:
        print("\nStarting cell-by-cell visualization in 2 seconds...")
        time.sleep(2)
        # Demo 1: Build animation (cell by cell) - SLOWER
        visualize_maze_build(maze, delay=0.1, title="Building Maze Cell-by-Cell")
    
    print("\nPress Enter to see maze with entry/exit markers...")
    input()
    
    # Demo 2: With entry/exit markers
    entry = (8, 1)
    exit_point = (width-2, height-2)
    visualize_maze_with_markers(maze, entry=entry, exit=exit_point, 
                                title="Maze with Entry/Exit Markers")
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)
    print("\nAvailable functions:")
    print("  - visualize_maze_build(maze, delay, title)")
    print("  - visualize_maze_animated(maze, delay, title)")
    print("  - visualize_maze_static(maze, title)")
    print("  - visualize_maze_with_markers(maze, entry, exit, path, title)")
    print()
