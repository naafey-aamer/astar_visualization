# A_star_visualization
A* Pathfinding Visualization with Pygame

Run astar.py. You can click on a box to make it an obstacle, and click on it again to make it a valid. Empty squares are represented by WHITE, the path by BLUE, and the obstacles by BLACK (make sure you have the required dependencies installed ,pygame and random, before running).

This .py file demonstrates a visualization of the A* pathfinding algorithm using the Pygame library. The algorithm finds the shortest path between a starting point and a goal point on a grid, taking obstacles into account.

The A* algorithm uses a priority queue to store nodes based on their f value (cost from start to current + estimated cost from current to goal). The algorithm iteratively selects the node with the lowest f value, explores its neighbors, and updates their g, h, and f values accordingly. The algorithm terminates when the goal node is reached or there are no more nodes to explore.

Overall, this notebook provides an interactive visualization of the A* pathfinding algorithm, allowing users to add and remove obstacles on the grid while observing the shortest path from the start to the goal node.
