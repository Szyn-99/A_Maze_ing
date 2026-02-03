import numpy as m
import enum as en


def maze_creator(width: int, height: int) -> list:
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1
    #(rows, columns) {matrix indexing} ==> row = heigth, column = width
    maze = m.ones((height, width),dtype=float) 
    for i in range(height):
        for j in range (width):
            if  i % 2 == 0 or j % 2 == 0:
                maze[i][j] = 0
            if i % 2 != 0 or j % 2 != 0 or i == width - 1 or j == height - 1:
                maze[i][j] = 0.5
    return maze
def recursive_backtracker(maze, x, y) -> None:
    maze[y, x] = 0.5
    
    if maze[y-2, x] == 0.5 and maze[y+2, x] == 0.5 and maze[y, x-2] == 0.5 and maze[y, x+2] == 0.5:
        return
    else:
        directions = tuple("north", "south", "west", "east")
        while True:
            move = m.random.choice(directions)
            if move == "north" and maze[y-2, x] == 0.5:
                maze[y-1, x] = 0.5
                recursive_backtracker(maze, x, y-2)
            elif move == "south" and maze[y+2, x] == 0.5:
                maze[y+1, x] = 0.5
                recursive_backtracker(maze, x, y+2)
            elif move == "west" and maze[y, x-2] == 0.5:
                maze[y, x-1] = 0.5
                recursive_backtracker(maze, x-2, y)
            elif move == "east" and maze[y, x+2] == 0.5:
                maze[y, x+1] = 0.5
                recursive_backtracker(maze, x+2, y)
            break

def generate_maze(width: int, height: int) -> list:
    maze = maze_creator(width, height)
    recursive_backtracker(maze, 1, 1)
    return maze
maze = generate_maze(7, 5)
for row in maze:
    print(row)