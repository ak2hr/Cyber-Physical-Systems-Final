#This is the script for making a Robot get from one point to another

import sys


#first, we need to create the list of instructions for each node, which
#takes into account:
# 1. The Node that the robot came from
# 2. The Node that the robot is at
# 3. The Node that the robot needs to go to
# 4. The Command that corresponds to this course of action (F, L, R, U)

commands = [('B','A','O','L'),
            ('O','A','B','R'),
            ('B','A','B','U'),
            ('O','A','O','U'),
            ('A','B','O','R'),
            ('A','B','C','F'),
            ('O','B','A','L'),
            ('O','B','C','R'),
            ('C','B','A','F'),
            ('C','B','O','L'),
            ('A','B','A','U'),
            ('O','B','O','U'),
            ('C','B','C','U'),
            ('B','C','H','R'),
            ('B','C','D','F'),
            ('H','C','B','L'),
            ('H','C','D','R'),
            ('D','C','B','F'),
            ('D','C','H','L'),
            ('B','C','B','U'),
            ('H','C','H','U'),
            ('D','C','D','U'),
            ('C','D','E','F'),
            ('C','D','G','R'),
            ('E','D','C','F'),
            ('E','D','G','L'),
            ('G','D','C','L'),
            ('G','D','E','R'),
            ('C','D','C','U'),
            ('E','D','E','U'),
            ('G','D','G','U'),
            ('D','E','F','R'),
            ('F','E','D','L'),
            ('D','E','D','U'),
            ('F','E','F','U'),
            ('E','F','G','R'),
            ('G','F','E','L'),
            ('E','F','E','U'),
            ('G','F','G','U'),
            ('D','G','F','L'),
            ('D','G','J','F'),
            ('F','G','D','R'),
            ('F','G','J','L'),
            ('J','G','D','F'),
            ('J','G','F','R'),
            ('D','G','D','U'),
            ('F','G','F','U'),
            ('J','G','J','U'),
            ('C','H','C','U'),
            ('C','H','I','L'),
            ('I','H','I','U'),
            ('I','H','C','R'),
            ('H','I','H','U'),
            ('H','I','J','F'),
            ('H','I','N','R'),
            ('J','I','J','U'),
            ('J','I','H','F'),
            ('J','I','N','L'),
            ('N','I','N','U'),
            ('N','I','H','L'),
            ('N','I','J','R'),
            ('I','J','I','U'),
            ('I','J','G','L'),
            ('I','J','K','R'),
            ('G','J','G','U'),
            ('G','J','I','R'),
            ('G','J','K','F'),
            ('K','J','K','U'),
            ('K','J','I','L'),
            ('K','J','G','F'),
            ('J','K','J','U'),
            ('J','K','L','R'),
            ('L','K','J','L'),
            ('L','K','L','U'),
            ('K','L','K','U'),
            ('K','L','M','F'),
            ('M','L','M','U'),
            ('M','L','K','F'),
            ('L','M','L','U'),
            ('L','M','N','R'),
            ('N','M','L','L'),
            ('N','M','N','U'),
            ('I','N','I','U'),
            ('I','N','M','L'),
            ('I','N','O','R'),
            ('M','N','M','U'),
            ('M','N','I','R'),
            ('M','N','O','F'),
            ('O','N','O','U'),
            ('O','N','I','F'),
            ('O','N','M','R'),
            ('A','O','A','U'),
            ('A','O','B','L'),
            ('A','O','N','F'),
            ('B','O','B','U'),
            ('B','O','A','R'),
            ('B','O','N','L'),
            ('N','O','N','U'),
            ('N','O','A','F'),
            ('N','O','B','R'),
            ('Z','A','B','F'),
            ('Z','A','O','R')]


#Next, we need to write everything associated with our node objects

class Node(object):
    
    def __init__(self, name, possible, dists):
        self.name = name            #name of node
        self.cost = 1000            #current cost of node
        self.possible = possible    #all possible nodes to travel to 
        self.dists = dists          #the cost to travel to each respective node
        self.fromNode = ''          #the node to travel from for the shortest path

    def updateCost(self, newCost, newFromNode):
        self.cost = newCost;
        self.fromNode = newFromNode
        
    def updatePossible(self, newPossible):
        possible = newPossible


#Next, we need to make all of the nodes for this map

node_A = Node('A', ('B','O'), (33.75, 30.75))
node_B = Node('B', ('A','C','O'), (33.75, 26.5, 39))
node_C = Node('C', ('B','D','H'), (26.5, 22, 28.25))
node_D = Node('D', ('C','E','G'), (22, 14.75, 16))
node_E = Node('E', ('D','F'), (14.75, 17))
node_F = Node('F', ('E','G'), (17, 17))
node_G = Node('G', ('D', 'F', 'J'), (16, 17, 29.5))
node_H = Node('H', ('C', 'I'), (28.25, 13))
node_I = Node('I', ('H', 'J', 'N'), (13, 30, 24.25))
node_J = Node('J', ('G', 'I', 'K'), (29,5, 30, 18))
node_K = Node('K', ('J', 'L'), (18, 26.25))
node_L = Node('L', ('K', 'M'), (26.25, 27.5))
node_M = Node('M', ('L', 'N'), (27.5, 26.25))
node_N = Node('N', ('I', 'M', 'O'), (24.25, 26.25, 25.5))
node_O = Node('O', ('A', 'B', 'N'), (30.75, 39, 25.5))
node_Z = Node('Z', ('A'), (10))


#then it's time to run the algorithm

#first we need to make a list of all of the unsettled nodes

unsett = [node_A, node_B, node_C, node_D, node_E, node_F, node_G,
          node_H, node_I, node_J, node_K, node_L, node_M, node_N, node_O, node_Z]

#and then create a list of the settled nodes, which begins empty

sett = []

#then we have to set our previous node

for i in unsett:
    if i.name == sys.argv[1]:
        prevNode = i


#then we need to add our starting node to this list, and set it's cost to zero

for i in unsett:
    if i.name == sys.argv[2]:
        startNode = i

startNode.updateCost(0, '')


#then we need to determine the destination node

for i in unsett:
    if i.name == sys.argv[3]:
        endNode = i


#then we need to look through all of the nodes connected to the start node,
#update their costs, and settle the lowest node. We will do this with all
#the nodes until they have all been found

curNode = startNode

while len(unsett) > 0:
    minimum = 10000
    for i in unsett:
        if i.cost < minimum:
            curNode = i
            minimum = i.cost
    sett.append(curNode)
    unsett.remove(curNode)
    k = 0
    for i in curNode.possible:
        for j in unsett:
            if j.name == i:
                if j.cost > curNode.cost + curNode.dists[k]:
                    j.cost = curNode.cost + curNode.dists[k]
                    j.fromNode = curNode.name
        k += 1


#now we need to create the path based on each nodes fromNode trait

curAt = endNode
path = ""
while curAt != startNode:
    path += curAt.name
    for i in sett:
        if i.name == curAt.fromNode:
            curAt = i
path += startNode.name
path += prevNode.name

#need to reverse to path string

directions = path[1]
path = path[::-1]


#Now we need to turn this node progression into a list of commands


for i in range(1, len(path) - 1):
    for j in commands:
        if path[i - 1] == j[0]:
            if path[i] == j[1]:
                if path[i + 1] == j[2]:
                    directions += j[3]

directions += 'D'
print(directions)
    



    













        
