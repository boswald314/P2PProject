import networkx as nx
import random
import matplotlib.pyplot as plt
import math
import time

#generate a number of random erdos renyi graphs of sizes and prob from 0.0001 to 0.05
p = 0.01
n = 5000
#while p <= 0.05 :
#    p += 0.0501/100

graph1 = nx.erdos_renyi_graph(n, p, seed=None, directed=False)
#nx.diameter(graph1)
nx.set_node_attributes(graph1, "targetNode", False)
nx.set_node_attributes(graph1, "visited", False)
#print (graph1.node[1]['targetNode'])
#graph2 = graph1
#graph1.node[1]['targetNode'] = True
#print (graph1.node[1]['targetNode'])
#print(graph2.node[1]['targetNode'])
#print (graph2 == graph1)
#print (graph1.number_of_nodes())

"""
for i in range(0,5000):
    if len(graph1.neighbors(i)) == 0:
        print(len(graph1.neighbors(i) == 0))
        
        import time

start = time.time()
print "hello"
end = time.time()
print end - start


just make list of tuples (p, density, n), append a new tuple for each failure
then we can graph the shit
"""

for i in range(0,100):
    numberOfNodes = graph1.number_of_nodes() -1
    graph1.node[random.randint(0, numberOfNodes)]['targetNode'] = True

    
def randomWalk(graph):
    numberOfNodes = graph.number_of_nodes() -1
    startNode = random.randint(0, numberOfNodes)
    nodesVisited = 1
    start = time.time()
    while (graph.node[startNode]['targetNode'] == False):
        graph.node[startNode]['visited'] = True
        possibleNextStep = graph.neighbors(startNode)
        if len(possibleNextStep) == 0:
            print("Could not find target node.")
            return "Could not find target node."
        startNode = random.choice(possibleNextStep)
        while graph.node[startNode]['visited'] == True:
            possibleNextStep.remove(startNode)
            if len(possibleNextStep) != 0:
                startNode = random.choice(possibleNextStep)
            else:
                print("Could not find target node.")
                return "Could not find target node."
                
        nodesVisited +=1
    end = time.time()
    
    print("Target node found after: "+str(nodesVisited)+" node(s) were visited.") 
    print("This took: "+ str(end - start) + " seconds.")
      


def kRandomWalk(graph,k):
    numberOfNodes = graph.number_of_nodes() -1
    startNodes = [0]*k
    for i in range(0,k):
        nodeToAdd = random.randint(0, numberOfNodes)
        while nodeToAdd in startNodes[:i]:
            nodeToAdd = random.randint(0, numberOfNodes)
        startNodes[i] = nodeToAdd
    nodesVisited = 1
    hopsBeforeFound = 0
    start = time.time()
    while True:
        index = 0
        for i in startNodes:
            graph.node[i]['visited'] = True
            if graph.node[i]['targetNode'] == True:
                end = time.time()
                print("Target node found after: "+str(nodesVisited)+" node(s) were visited.") 
                print("This took: "+ str(end - start) + " seconds.")
                print("Total number of hops was: "+ str(hopsBeforeFound))
                return "Tartget node found"
            else:
                possibleNextStep = graph.neighbors(i)
                if len(possibleNextStep) == 0:
                    print("Could not find target node.")
                    return "Could not find target node."
                startNode = random.choice(possibleNextStep)
                while graph.node[startNode]['visited'] == True:
                    possibleNextStep.remove(startNode)
                    if len(possibleNextStep) != 0:
                        startNode = random.choice(possibleNextStep)
                    else:
                        print("Could not find target node.")
                        return "Could not find target node."
                startNodes[index] = startNode
                index +=1
                nodesVisited +=1
        hopsBeforeFound +=1
    print("Hi Bryan!")


def gnutellaFlooding(graph):
    numberOfNodes = graph.number_of_nodes() -1
    nodesToCheck = [random.randint(0, numberOfNodes)]
    nodesVisited = 1
    
    start = time.time()
    while True:
        for i in nodesToCheck:
            graph.node[i]['visited'] = True
            if graph.node[i]['targetNode'] == True:
                end = time.time()
                print("Target node found after: "+str(nodesVisited)+" node(s) were visited.") 
                print("This took: "+ str(end - start) + " seconds.")
                return "Tartget node found"
            else:
                neighbors = graph.neighbors(i)
                for item in neighbors:
                    if graph.node[item]['visited'] == False:
                        nodesToCheck.append(item)
                nodesToCheck.remove(i)
            nodesVisited += 1

#randomWalk(graph1)



#kRandomWalk(graph1,5)
gnutellaFlooding(graph1)
print("done")
