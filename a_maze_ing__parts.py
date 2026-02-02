import numpy as m
def maze_creator(width: int, height: int) -> list:
    maze = m.ones((width, height),dtype=int)
    for i in range(width):
        for another_i in range (height):
            if i % 2 != 0 or another_i % 2 != 0:
                maze[i][another_i] = 0
    return maze
maze = maze_creator(7, 5)
for row in maze:
    print(row)

        
# class cell:
#     def __