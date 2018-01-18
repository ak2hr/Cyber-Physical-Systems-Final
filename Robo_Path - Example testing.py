#This is the script for making a Robot get from one point to another

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
            ('D','G','F','R'),
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
            ('O','N','I','L'),
            ('O','N','M','F'),
            ('A','O','A','U'),
            ('A','O','B','L'),
            ('A','O','N','F'),
            ('B','O','B','U'),
            ('B','O','A','R'),
            ('B','O','N','L'),
            ('N','O','N','U'),
            ('N','O','A','F'),
            ('N','O','B','R')]


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

node_A = Node('A', ('B','C','D'), (3,4,2))
node_B = Node('B', ('A','C','E'), (3,4,2))
node_C = Node('C', ('A','B','E'), (4,4,6))
node_D = Node('D', ('A','E','F'), (2,1,4))
node_E = Node('E', ('B','C','D','F'), (2,6,1,2))
node_F = Node('F', ('D','E'), (4,2))


#then it's time to run the algorithm

#first we need to make a list of all of the unsettled nodes

unsett = [node_A, node_B, node_C, node_D, node_E, node_F]

#and then create a list of the settled nodes, which begins empty

sett = []

#then we need to add our starting node to this list, and set it's cost to zero

node_A.updateCost(0, '')

#then we need to look through all of the nodes connected to A, update their costs,
#and settle the lowest node. We will do this with all the nodes until they
#have all been found

curNode = node_A
endNode = node_F

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

startNode = node_A
curAt = endNode
path = ""
while curAt != startNode:
    path += curAt.name
    for i in sett:
        if i.name == curAt.fromNode:
            curAt = i
path += startNode.name
print(path)
    












        
