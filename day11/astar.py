import heapq
from .utils import indent

class PriorityQueue:

    def __init__(self, *elements):
        self.elements = []
        for element in elements:
            self.put(*element)

    def __bool__(self):
        return bool(self.elements)

    def __len__(self):
        return len(self.elements)

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
        #print(self.elements)

    def get(self):
        priority, item = heapq.heappop(self.elements)
        #print(self.elements)
        return item


class Heuristic(object):

    def __init__(self, goal):
        self.cache = {}
        for fn, floor in enumerate(goal.floors, start=1):
            for item in floor:
                self.cache[item] = fn

    def __call__(self, from_):
        #cost = 1 + (from_.elevator - to.elevator)
        cost = 0

        for fn, floor in enumerate(from_.floors, start=1):
            for item in floor:
                cost += abs(fn - self.cache[item])

        return cost


def find(start, goal):
    heuristic = Heuristic(goal)

    frontier = PriorityQueue((start, 0))

    came_from = {start: None}
    cost_so_far = {start: 0}
    rank_key = lambda item: item[0]

    cost = None
    while frontier:
        current = frontier.get()

        print(indent('current:', 2))
        print(indent(current, 2))

        if current is goal:
            print('GOOOOOOOOAL')
            break

        for neighbor in current.neighbors():
            print(indent('neighbor:', 4))
            print(indent(neighbor, 4))

            cost = cost_so_far[current] + current.cost(neighbor)
            print(indent('cost: %s' % cost, 4))

            if neighbor not in cost_so_far or cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = cost
                rank = cost + heuristic(neighbor)
                frontier.put(neighbor, rank)
                came_from[neighbor] = current

    return came_from, cost_so_far

def draw(came_from, start, goal):
    print(goal)
    print()

    v = came_from[goal]
    if v is not None:
        print(v)
        print()

    steps = 2
    while True:
        v = came_from[v]
        print(v)
        if v == start:
            break
        steps += 1
        print()

    print('Solved in %s steps' % steps)
