*This project has been created as part of the 42 curriculum by iamessag, aymel-ha.*

# A-Maze-ing

## Description

**A-Maze-ing**, a terminal-based maze generation program written in Python. The goal of the project is to generate a perfect maze — one with no loops and exactly one path between any two cells — and render it interactively in the terminal using a dedicated graphic window or displayed on the terminal.

The maze is generated using an **iterative Depth-First Search (DFS)** algorithm, also known as Recursive Backtracking. The iterative approach was chosen over a recursive one to work around Python's default recursion limit, which becomes a problem for large mazes. The algorithm works by maintaining an explicit stack (simulating stack using list), visiting unvisited neighbors at random, and carving passages between cells until the entire grid has been explored.

---

## Instructions

### Requirements

- Python 3.x
- A Unix-like terminal with `curses` support (Linux / macOS)
- `make`

### Installation & Execution

Clone the repository and run:

```bash
make install
```

To run the program directly:

```bash
make run
```



This will generate a maze based on the configuration file and display it in the terminal.

To clean up generated files:

```bash
make clean
```

To check against flake8 and numpy
```bash
make lint
```


> **Note:** The terminal window must be large enough to display the maze. If the window is too small, the program will exit with an error.

---

## Resources

### Maze Generation

- Jamis Buck — Mazes for Programmers: Code Your Own Twisty Little Passages (Book) — explains a dozen maze generation algorithms (Binary Tree, Recursive Backtracker, Prim’s, Kruskal’s) with practical Ruby implementations.  It covers algorithm trade-offs, maze visualization, solving techniques like Dijkstra’s algorithm, and advanced topics such as mazes on hex grids, 3D surfaces

- [Maze Generation: Recursive Backtracking](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking) __ A blog explaining Recursive Backtracking (4 minutes read).
- [Maze Generation — Recursive Backtracking by Aryan Abed-Esfahani](https://aryanab.medium.com/maze-generation-recursive-backtracking-5981bc5cc766) __ Another blog explaining maze generation using recursive backtracking in simple terms (9 minutes read). 
- [Maze Generation Algorithm — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm) — A solid overview of common maze generation techniques including DFS, Prim's, and Kruskal's.


### Python curses

- [Python `curses` — Official Documentation](https://docs.python.org/3/library/curses.html) — The standard library reference for the `curses` module.
- [Tech With Tim (Python Curses Tutorial)](https://youtube.com/playlist?list=PLzMcBGfZo4-n2TONAOImWL4sgZsmyMBc8&si=f6FfFq_bGAo-iZpQ) — A beginner-friendly guide to use `curses` in Python, Simple and short.

### Python Recursion Limit

- [Python `sys.setrecursionlimit` — Official Docs](https://docs.python.org/3/library/sys.html#sys.setrecursionlimit) — Documents the recursion limit and why iterative solutions are often preferred for deep traversals.
- [Stack Overflow — Iterative DFS vs Recursive DFS](https://stackoverflow.com/questions/9999784/iterative-dfs-vs-recursive-dfs-and-different-results) — Discussion on converting recursive DFS to an iterative version using an explicit stack.

### AI Usage

AI tools (specifically Claude) were used during this project for the following purposes:

- **Debugging help:** Identifying and resolving issues related to `curses` display bugs, off-by-one errors in the grid, and stack handling in the iterative DFS implementation.
- **Understanding concepts:** Clarifying how the Recursive Backtracking / DFS maze generation algorithm works conceptually, and understanding why Python's recursion limit causes issues with deep recursive traversals on large grids.