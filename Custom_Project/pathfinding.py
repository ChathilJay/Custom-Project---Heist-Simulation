import heapq

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

def a_star_search(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
    start_node = Node(None, start)
    end_node = Node(None, end)

    open_list = []
    closed_list = set()

    heapq.heappush(open_list, start_node)

    while len(open_list) > 0:
        current_node = heapq.heappop(open_list)
        closed_list.add(current_node.position)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        (x, y) = current_node.position
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)] # Adjacent squares

        for next_pos in neighbors:
            if next_pos[1] < 0 or next_pos[1] >= len(maze) or next_pos[0] < 0 or next_pos[0] >= len(maze[0]):
                continue
            if maze[next_pos[1]][next_pos[0]] == 'W':
                continue
            if next_pos in closed_list:
                continue

            neighbor = Node(current_node, next_pos)
            neighbor.g = current_node.g + 1
            neighbor.h = ((neighbor.position[0] - end_node.position[0]) ** 2) + ((neighbor.position[1] - end_node.position[1]) ** 2)
            neighbor.f = neighbor.g + neighbor.h
            
            if any(n for n in open_list if neighbor == n and neighbor.g > n.g):
                continue
            
            heapq.heappush(open_list, neighbor)

    return None # Path not found
