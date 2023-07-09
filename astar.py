import pygame
import heapq
import math

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Window dimensions
WIDTH = 500
HEIGHT = 500

# Grid dimensions
ROWS = 10
COLS = 10
GRID_SIZE = WIDTH // COLS

# Initialize Pygame
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding")

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.position = (row, col)
        self.neighbors = []
        self.g = 0
        self.h = 0
        self.f = 0
        self.is_obstacle = False
        self.is_start = False
        self.is_goal = False
        self.parent = None  
        
    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def __lt__(self, other):
        return self.f < other.f


def update_obstacle(grid, row, col):
    node = grid[row][col]
    node.is_obstacle = not node.is_obstacle

    # Run A* algorithm again
    start = (0, 0)
    goal = (ROWS - 1, COLS - 1)
    path = astar(grid, start, goal)
    return path

def distance(p1, p2):
    dx = abs(p1[0] - p2[0])
    dy = abs(p1[1] - p2[1])
    return math.sqrt(dx*dx + dy*dy)

def create_grid():
    grid = [[Node(row, col) for col in range(COLS)] for row in range(ROWS)]
    for row in range(ROWS):
        for col in range(COLS):
            node = grid[row][col]
            if row > 0:
                node.add_neighbor(grid[row - 1][col])  # Up
            if row < ROWS - 1:
                node.add_neighbor(grid[row + 1][col])  # Down
            if col > 0:
                node.add_neighbor(grid[row][col - 1])  # Left
            if col < COLS - 1:
                node.add_neighbor(grid[row][col + 1])  # Right
            if row > 0 and col > 0:
                node.add_neighbor(grid[row - 1][col - 1])  # Up-Left
            if row > 0 and col < COLS - 1:
                node.add_neighbor(grid[row - 1][col + 1])  # Up-Right
            if row < ROWS - 1 and col > 0:
                node.add_neighbor(grid[row + 1][col - 1])  # Down-Left
            if row < ROWS - 1 and col < COLS - 1:
                node.add_neighbor(grid[row + 1][col + 1])  # Down-Right
    return grid

def draw_grid(grid):
    # Set start and goal nodes
    grid[0][0].is_start = True
    grid[ROWS - 1][COLS - 1].is_goal = True
    
    for row in range(ROWS):
        for col in range(COLS):
            node = grid[row][col]
            color = WHITE
            if node.is_obstacle:
                color = BLACK
            elif node.is_start:
                color = GREEN
            elif node.is_goal:
                color = RED
            pygame.draw.rect(win, color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(win, BLUE, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

def draw_path(path):
    for i, (row, col) in enumerate(path):
        if i == 0:
            pygame.draw.rect(win, GREEN, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        elif i == len(path) - 1:
            pygame.draw.rect(win, RED, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        else:
            pygame.draw.rect(win, BLUE, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def astar(grid, start, goal):
    open_set = []
    closed_set = set()

    start_node = grid[start[0]][start[1]]
    goal_node = grid[goal[0]][goal[1]]

    heapq.heappush(open_set, (0, start_node))

    while open_set:
        current = heapq.heappop(open_set)[1]
        closed_set.add(current)

        if current == goal_node:
            path = []
            node = current
            while node:
                path.append(node.position)
                node = node.parent
            path.reverse()
            return path

        for neighbor in current.neighbors:
            if neighbor.is_obstacle or neighbor in closed_set:
                continue

            new_g = current.g + distance(current.position, neighbor.position)

            if new_g < neighbor.g or neighbor not in [i[1] for i in open_set]:
                neighbor.g = new_g
                neighbor.h = distance(neighbor.position, goal_node.position)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current

                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (neighbor.f, neighbor))

    return None


def main():
    grid = create_grid()
    start = (0, 0)
    goal = (ROWS - 1, COLS - 1)
    path = astar(grid, start, goal)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]: 
                    mouse_pos = pygame.mouse.get_pos()
                    col = mouse_pos[0] // GRID_SIZE
                    row = mouse_pos[1] // GRID_SIZE
                    path = update_obstacle(grid, row, col)

        win.fill(WHITE)
        draw_grid(grid)
        if path:
            draw_path(path)
        pygame.display.update()

if __name__ == '__main__':
    main()

