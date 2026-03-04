import curses
import numpy as n
import locale
locale.setlocale(locale.LC_ALL, '')
class Render_Maze:
    def __init__(self, maze, entry, exit_,  actions=None):
        self.maze = maze
        self.entry = entry
        self.exit = exit_
        self.actions = actions
        # self.path = path
    
    def _get_intersection_char(self, up, right, down, left):
        connections = (up, right, down, left)
        
        # Double-line characters (thicker)
        mapping = {
            (1,1,1,1): "╬",  # ┼ becomes ╬
            (1,1,1,0): "╠",  # ├ becomes ╠
            (1,0,1,1): "╣",  # ┤ becomes ╣
            (0,1,1,1): "╦",  # ┬ becomes ╦
            (1,1,0,1): "╩",  # ┴ becomes ╩
            (1,0,1,0): "║",  # │ becomes ║
            (0,1,0,1): "═",  # ─ becomes ═
            (0,1,1,0): "╔",  # ┌ becomes ╔
            (0,0,1,1): "╗",  # ┐ becomes ╗
            (1,1,0,0): "╚",  # └ becomes ╚
            (1,0,0,1): "╝",  # ┘ becomes ╝
        }
        
        return mapping.get(connections, " ")
    # def _init_colors(self):
    #     curses.start_color()
    #     curses.use_default_colors()

    #     curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)  # walls
    #     curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)  # path
    #     curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_GREEN)  # entry
    #     curses.init_pair(4, curses.COLOR_RED, curses.COLOR_RED)      # exit

    def animate(self, actions):
        curses.wrapper(self._animate_main, actions)
        if not actions:
            return False
        return True

    def _animate_main(self, stdscr, actions):
        curses.curs_set(0)
        self._init_colors()
        
        height, width = self.maze.shape
        anim_maze = n.full((height, width), 0xF, dtype=n.uint8)
        
        delay = 50  # ms, adjust as needed
        current_head = None
        
        stdscr.nodelay(True)  # non-blocking getch
        
        for action in actions:
            # handle speed control
            key = stdscr.getch()
            if key == ord('+'):
                delay = max(10, delay - 10)
            elif key == ord('-'):
                delay = min(500, delay + 10)
            
            if action['type'] == 'pattern':
                x, y = action['cell']
                anim_maze[y, x] = 0xF  # stays fully walled
            
            elif action['type'] == 'visit':
                current_head = action['cell']
            
            elif action['type'] == 'carve':
                fx, fy = action['from_cell']
                tx, ty = action['to_cell']
                d = action['direction']
                
                # update the live maze bits
                wall_map = {
                    'N': (0, 2),  # bit to clear on from, bit to clear on to
                    'S': (2, 0),
                    'E': (1, 3),
                    'W': (3, 1),
                }
                from_bit, to_bit = wall_map[d]
                anim_maze[fy, fx] &= ~(1 << from_bit)
                anim_maze[ty, tx] &= ~(1 << to_bit)
                current_head = (tx, ty)
            
            elif action['type'] == 'backtrack':
                current_head = action['from_cell']
            
            self._draw_frame(stdscr, anim_maze, current_head, action['type'])
            curses.napms(delay)

    def _init_colors(self):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, -1)   # walls
        curses.init_pair(6, curses.COLOR_YELLOW, -1) 
        curses.init_pair(2, curses.COLOR_GREEN, -1)   # entry
        curses.init_pair(3, curses.COLOR_RED, -1)       # exit
        curses.init_pair(4, curses.COLOR_YELLOW, -1)                    # carving head
        curses.init_pair(5, curses.COLOR_YELLOW, -1)                  # backtrack head

    def _draw_frame(self, stdscr, anim_maze, head=None, action_type=None):
        stdscr.clear()
        height, width = anim_maze.shape

        display = [[" " for _ in range(3 * width + 1)] for _ in range(2 * height + 1)]

        for y in range(height):
            for x in range(width):
                cell = anim_maze[y, x]
                base_y = 2 * y
                base_x = 3 * x

                # cell content
                if (x, y) == self.entry:
                    display[base_y + 1][base_x + 1] = "E"
                    display[base_y + 1][base_x + 2] = " "
                elif (x, y) == self.exit:
                    display[base_y + 1][base_x + 1] = "X"
                    display[base_y + 1][base_x + 2] = " "
                else:
                    display[base_y + 1][base_x + 1] = ""
                    display[base_y + 1][base_x + 2] = ""

                # walls
                if cell & 1:
                    display[base_y][base_x + 1] = "═"
                    display[base_y][base_x + 2] = "═"
                if cell & 4:
                    display[base_y + 2][base_x + 1] = "═"
                    display[base_y + 2][base_x + 2] = "═"
                if cell & 8:
                    display[base_y + 1][base_x] = "║"
                if cell & 2:
                    display[base_y + 1][base_x + 3] = "║"

        # intersections
        for y in range(0, 2 * height + 1, 2):
            for x in range(0, 3 * width + 1, 3):
                up    = 1 if y > 0       and display[y-1][x] == "║" else 0
                down  = 1 if y < 2*height and display[y+1][x] == "║" else 0
                left  = 1 if x > 0       and display[y][x-1] == "═" else 0
                right = 1 if x < 3*width  and display[y][x+1] == "═" else 0
                display[y][x] = self._get_intersection_char(up, right, down, left)

        # render
        for y in range(len(display)):
            for x in range(len(display[y])):
                char = display[y][x]
                if char == " ":
                    continue

                cell_x = x // 3
                cell_y = y // 2
                is_head = head is not None and (cell_x, cell_y) == head

                if is_head and char not in self._get_intersection_chars():
                    color = curses.color_pair(5) if action_type == 'backtrack' else curses.color_pair(6)
                else:
                    color = curses.color_pair(1)
                if (cell_x, cell_y) == self.entry:
                    color = curses.color_pair(2)
                elif (cell_x, cell_y) == self.exit:
                    color = curses.color_pair(3)
                elif is_head and char not in self._get_intersection_chars():
                    # ▓ gives a "drilling" feel — it's inside the cell being carved
                    char = "▓"
                    color = curses.color_pair(4) if action_type == 'carve' else curses.color_pair(5)
                else:
                    color = curses.color_pair(1)

                try:
                    stdscr.addstr(y, x, char, color)
                except curses.error:
                    pass

        stdscr.refresh()

    def _get_intersection_chars(self):
        return set("╬╠╣╦╩║═╔╗╚╝")

    # refactor _draw to reuse _draw_frame
    def _draw(self, stdscr):
        curses.curs_set(0)
        stdscr.clear()
        self._draw_frame(stdscr, self.maze)

    def _main(self, stdscr):
        curses.curs_set(0)

        if not curses.has_colors():
            raise Exception("Terminal does not support colors")

        self._init_colors()
        self._draw(stdscr)

        stdscr.getch()

    def display(self):
        curses.wrapper(self._main)
