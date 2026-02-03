import numpy as n

# Test the maze generation logic
def grid_creator(height: int, width: int) -> n.ndarray:
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1
    maze = n.ones((height, width), dtype=int)
    return maze

# Create a small 7x7 maze
maze = grid_creator(7, 7)
print("Initial maze (all walls = 1):")
print(maze)
print("\nShape:", maze.shape)

# Simulate one step of carving
maze[1, 1] = 0  # Carve starting position
maze[1, 2] = 0  # Carve wall between
maze[1, 3] = 0  # Carve next cell

print("\nAfter carving path from (1,1) to (1,3):")
print(maze)

print("\nVisual representation:")
for y in range(7):
    line = ""
    for x in range(7):
        if maze[y, x] == 1:
            line += "██"  # Wall
        else:
            line += "  "  # Path
    print(f"Row {y}: '{line}'")
