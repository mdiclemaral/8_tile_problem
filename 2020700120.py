'''
8-tile problem

Implemented by Maral Dicle Maral March 2021

A modified version of an 8-tile problem by implementing various search algorithms,namely BFS, DFS, UCS, A* Search with various heuristic methods, compares these methods’ performances in different tile configurations.
'''

import sys

class Node:  #Stores tile boards
    def __init__(self, data, parent):
        self.data = data
        self.parent = parent
        self.shift = None
        self.cost = 0
        self.num_costs = []
        self.num_dict = {}
        self.h = 0
        self.f = 0

    def child_born(self, visited, num_costs, num_dict, nInsertedNodes):  # Creates a new board with new tile configuration
        children = []
        for cost in num_costs:
            new_positions = []
            x = num_dict[cost][0]
            y = num_dict[cost][1]
            new_positions.extend([[x-1, y, " left"], [x+1, y, " right"], [x, y-1, " up"], [x, y+1, " down"]])  #left right up down
            for j in new_positions:
                child = self.shift_position(x, y, j[0], j[1])
                if child is not None and child not in visited:
                    childN = Node(child, self)
                    childN.shift = "move " + str(cost)+ j[2]
                    childN.cost = cost + childN.parent.cost
                    children.append(childN)
                    nInsertedNodes += 1
        return children, nInsertedNodes

    def shift_position(self, x1, y1, x2, y2):  # Shifts the positions to the given directions

        child = self.copy(self.data)
        if (x2>= 0 and y2>= 0 and x2 < len(self.data) and y2 < len(self.data)):

            if self.data[y2][x2] == ".":
                temp_pos = child[y2][x2]
                child[y2][x2] = child[y1][x1]
                child[y1][x1] = temp_pos
                return child
            else:
                return None
        else:
            return None

    def copy(self, node):  # Creates a copy of the current board
        temp = []
        for i in range(0, len(node)):
            t = node[i].copy()
            temp.append(t)
        return temp

    def find_number(self):  # Finds the positions of the tiles
        num_costs = []
        number_found = {}
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data)):
                if not (self.data[i][j] == "." or self.data[i][j] == "x"):
                    current_tile = int(self.data[i][j])
                    num_costs.append(current_tile)
                    number_found[current_tile] = [j, i]
        return num_costs, number_found


class Puzzle: # Puzzle class to store the whole puzzle
    def __init__(self, innput, outtput, search_type):
        self.innput = innput
        self.outtput = outtput
        self.search_type = search_type
        self.start = None
        self.goal = None
        self.createPuzzle()
        self.goal_tiles = None
        self.goal_dict = None

    def createPuzzle(self):  # Creates the initial and goal nodes and initiates the puzzle
        final_input = []
        final_goal = []

        for i in range(0,len(self.innput)):

            temp_input = self.innput[i].split()
            final_input.append(temp_input)

            temp_goal = self.outtput[i].split()
            final_goal.append(temp_goal)

        self.start = Node(final_input, None)
        self.goal = Node(final_goal, None)

    def process(self, out_file):  # The main process function

        f = open(out_file, 'w')

        self.goal_tiles, self.goal_dict = self.goal.find_number()

        if self.search_type == "bfs":
            visited_node, nInsertedNodes = self.bfs()

        elif self.search_type == "dfs":
            visited_node, nInsertedNodes = self.dfs()

        elif self.search_type == "ucs":
            visited_node, nInsertedNodes= self.ucs()

        elif self.search_type == "astar0":
            visited_node, nInsertedNodes = self.astar0()

        elif self.search_type == "astar1":
            visited_node, nInsertedNodes = self.astar1()

        elif self.search_type == "my-astar-positive":
            visited_node, nInsertedNodes = self.my_astar_positive()

        elif self.search_type == "my-astar-all":
            visited_node, nInsertedNodes = self.my_astar_all()
        else:
            print("Search method is not found. ")
            visited_node = None
            nInsertedNodes = 0

        total_cost = visited_node.cost
        stack = []
        while (visited_node.parent != None):
            stack.append(visited_node.shift)
            visited_node = visited_node.parent
        for i in range(0, len(stack)):
            f.write(stack.pop() + "\n")
        f.write("nInsertedNodes: " + str(nInsertedNodes) + "\n")
        f.write("cost: " + str(total_cost) + "\n")

    def bfs(self):  # breath-first search

        nInsertedNodes = 1
        visited = []
        queue = [self.start]
        while queue:
            visiting_node = queue.pop(0)
            visited.append(visiting_node.data)
            count = 0
            count_goal = len(self.goal_tiles)
            current_cost, current_dict = visiting_node.find_number()
            for i in self.goal_tiles:
                if self.goal_dict[i] == current_dict[i]:
                    count += 1
            if count == count_goal:
                return visiting_node, nInsertedNodes
            else:
                children, nInsertedNodes = visiting_node.child_born(visited, current_cost, current_dict, nInsertedNodes)
                queue.extend(children)

    def dfs(self):  # depth-first search

        nInsertedNodes = 1
        visited = []
        stack = [self.start]
        while stack:
            visiting_node = stack.pop()
            visited.append(visiting_node.data)
            count = 0
            current_cost, current_dict = visiting_node.find_number()
            for i in self.goal_tiles:
                if self.goal_dict[i] == current_dict[i]:
                    count += 1
            if count == len(self.goal_tiles):
                return visiting_node, nInsertedNodes
            else:
                children, nInsertedNodes = visiting_node.child_born(visited, current_cost, current_dict, nInsertedNodes)
                stack.extend(children)

    def ucs(self):  # Uniform-cost search

        nInsertedNodes = 1
        visited = []
        queue = [self.start]
        while queue:
            queue.sort(key=lambda x: x.cost)
            visiting_node = queue.pop(0)
            visited.append(visiting_node.data)
            count = 0
            current_cost, current_dict = visiting_node.find_number()
            for i in self.goal_tiles:
                if self.goal_dict[i] == current_dict[i]:
                    count += 1
            if count == len(self.goal_tiles):
                return visiting_node, nInsertedNodes
            else:
                children, nInsertedNodes = visiting_node.child_born(visited, current_cost, current_dict, nInsertedNodes)
                queue.extend(children)

    def h0(self, current): # Heuristic method for Astar1 H(x) = Misplaced Tiles
        counter = 0
        for i in self.goal_tiles:
            [x,y] = self.goal_dict[i]
            if current.data[y][x] != str(i):
                counter += 1
        return counter

    def astar0(self): # Astar0 Algorithm with Manhattan Distance Heuristics

        nInsertedNodes = 1
        visited = []
        queue = [self.start]
        while queue:
            queue.sort(key=lambda x: x.f)
            visiting_node = queue.pop(0)
            visited.append(visiting_node.data)
            count = 0
            current_cost, current_dict = visiting_node.find_number()
            for i in self.goal_tiles:
                if self.goal_dict[i] == current_dict[i]:
                    count += 1
            if count == len(self.goal_tiles):
                return visiting_node, nInsertedNodes
            else:
                children, nInsertedNodes = visiting_node.child_born(visited, current_cost, current_dict, nInsertedNodes)
                for i in children:
                    i.h = self.h0(i)
                    i.f = i.cost + i.h
                    queue.append(i)

    def h1(self, current):  # Heuristic method for Astar1 H(x) = Manhattan Distance

        current_cost, current_dict = current.find_number()
        distance = 0
        for i in self.goal_tiles:
            distance += abs(int(self.goal_dict[i][0]) - int(current_dict[i][0])) + abs(int(self.goal_dict[i][1]) - int(current_dict[i][1]))
        return distance

    def astar1(self):  # Astar1 Algorithm with Misplaced Tiles Heuristics

        nInsertedNodes = 1
        visited = []
        queue = [self.start]
        while queue:
            queue.sort(key=lambda x: x.f)
            visiting_node = queue.pop(0)
            visited.append(visiting_node.data)
            count = 0
            current_cost, current_dict = visiting_node.find_number()
            for i in self.goal_tiles:
                if self.goal_dict[i] == current_dict[i]:
                    count += 1
            if count == len(self.goal_tiles):
                return visiting_node, nInsertedNodes
            else:
                children, nInsertedNodes = visiting_node.child_born(visited, current_cost, current_dict, nInsertedNodes)
                for i in children:
                    i.h = self.h1(i)
                    i.f = i.cost + i.h
                    queue.append(i)

    def my_h0(self, current):  # Heuristic method for My-astar-positive. H(x) = total of misplaced tiles' cost
        counter = 0
        for i in self.goal_tiles:
            [x, y] = self.goal_dict[i]
            if current.data[y][x] != str(i):
                counter += i
        return counter

    def my_astar_positive(self):  # My A* Algorithm for positive tiles
        nInsertedNodes = 1
        visited = []
        queue = [self.start]
        while queue:
            queue.sort(key=lambda x: x.f)
            visiting_node = queue.pop(0)
            visited.append(visiting_node.data)
            count = 0
            current_cost, current_dict = visiting_node.find_number()
            for i in self.goal_tiles:
                if self.goal_dict[i] == current_dict[i]:
                    count += 1
            if count == len(self.goal_tiles):
                return visiting_node, nInsertedNodes
            else:
                children, nInsertedNodes = visiting_node.child_born(visited, current_cost, current_dict, nInsertedNodes)
                for i in children:
                    i.h = self.my_h0(i)
                    i.f = i.cost + i.h
                    queue.append(i)

    def my_h1(self, current):  # Heuristic method for My-astar-all. H(x) = min(misplaced tiles’ cost) * total Manhattan Distance
        current_cost, current_dict = current.find_number()
        list_of_misplaced = []
        distance = 0
        min_cost = 0
        for i in self.goal_tiles:
            [x, y] = self.goal_dict[i]
            if current.data[y][x] != str(i):
                distance += abs(int(self.goal_dict[i][0]) - int(current_dict[i][0])) + abs(
                    int(self.goal_dict[i][1]) - int(current_dict[i][1]))
                list_of_misplaced.append(i)
        if len(list_of_misplaced) != 0:
            min_cost = min(list_of_misplaced)
        return min_cost * distance

    def my_astar_all(self): # My A* Algorithm for all types of tiles
        nInsertedNodes = 1
        visited = []
        queue = [self.start]
        while queue:
            queue.sort(key=lambda x: x.f)
            visiting_node = queue.pop(0)
            visited.append(visiting_node.data)
            count = 0
            current_cost, current_dict = visiting_node.find_number()
            for i in self.goal_tiles:
                if self.goal_dict[i] == current_dict[i]:
                    count += 1
            if count == len(self.goal_tiles):
                return visiting_node, nInsertedNodes
            else:
                children, nInsertedNodes = visiting_node.child_born(visited, current_cost, current_dict, nInsertedNodes)
                for i in children:
                    i.h = self.my_h1(i)
                    i.f = i.cost + i.h
                    queue.append(i)


search_type = sys.argv[1]
initial_state = sys.argv[2]
goal_state = sys.argv[3]
out_file = sys.argv[4]


with open(initial_state) as file_initial:
    input_initial = file_initial.readlines()

with open(goal_state) as file_goal:
    input_goal = file_goal.readlines()

puzz = Puzzle(input_initial, input_goal, search_type)
puzz.process(out_file)

