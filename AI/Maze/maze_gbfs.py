# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 16:58:57 2022

@author: Bharati Panigrahi
"""
import sys

class Node():
    def __init__(self, state, parent, action, dist):
        self.state = state
        self.parent = parent
        self.action = action
        self.dist = dist
        
class GBFS():
    def __init__(self):
        self.frontier = []
        
    def add(self, node): #used for adding node to frontier
        self.frontier.append(node)
        
    def contains_state(self, state): #used to check if some state is already in frontier
        return any(node.state == state for node in self.frontier)
    
    def empty(self): #used for checking if frontier is empty or not
        return len(self.frontier) == 0
    
    def remove(self): #used for removing a node from frontier
        if self.empty():
            raise Exception('Empty Frontier')
        else:
            d1=self.frontier[0].dist
            remove_node=0
            for n in range(1,len(self.frontier)):
                if self.frontier[n].dist<=d1:
                    remove_node=n
                    d1 = self.frontier[n].dist
            node=self.frontier.pop(remove_node)
            return node
        

class Maze():
    
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()
            
        # Validate start and goal
        if contents.count('A') != 1:
            raise Exception('Maze must have exactly one start point.')
        if contents.count('B') !=1:
            raise Exception('Maze must have exactly one goal point.')
            
        # Detremine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)
        
        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row=[]
            for j in range(self.width):
                try:
                    if contents[i][j] == 'A':
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == 'B':
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == ' ':
                        row.append(False)
                    else:
                        row.append(True)
                
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        self.solution = None
    
    
    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print(' ', end='')
                elif (i, j) == self.start:
                    print('A', end='')
                elif (i, j) == self.goal:
                    print('B', end='')
                elif solution is not None and (i, j) in solution:
                    print('*', end='')
                else:
                    print(' ', end='')
            print()
        print()
        
        
    def neighbors(self, state):
        row, col = state
        candidates = [
            ('up', (row-1, col)),
            ('down', (row+1, col)),
            ('left', (row, col-1)),
            ('right', (row, col+1))
            ]
        
        result = []
        for action, (r,c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r,c)))
        return result
    
    
    def solve(self):
        #Find solution to maze if one exists
        
        #Keep track of number of states explored
        self.num_explored = 0
        
        #Initialize frontier to justr the starting position
        start = Node( state = self.start, parent = None, action = None, dist = (abs(self.goal[1]-self.start[1])+abs(self.goal[0]-self.start[0])) )
        frontier = GBFS()
        frontier.add(start)
        
        #Initialize an empty explored set
        self.explored = set()
        
        #Keep looping until solution found
        while True:
            #If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception('No solution')
                
            #Choose a node from the frontier
            node = frontier.remove()
            self.num_explored+=1
            
            #If node is goal then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            
            #Mark node as explored
            self.explored.add(node.state)
            
            #Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state = state, parent = node, action = action, dist = (abs(self.goal[1]-state[1])+abs(self.goal[0]-state[0])))
                    frontier.add(child)
                    

'''if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")
    
m = Maze(sys.argv[1])''' 
m = Maze(input('Filename : '))

print("Maze : ")
m.print()
print('Solving...')
m.solve()
print('States Explored : ', m.num_explored)
print('Solution : ')
m.print()

