# -*- coding: utf-8 -*-
"""
Final Project

@author: ZachCain

Project 2

Generate a number of random (Erdös-Rényi) graphs of sizes from to nodes for various values of the 
probability ranging from 0.0001 to 0.05.

(a) Use NetworkX (or an appropriate visualization software) to visualize these graphs.

(b) Use appropriate algorithms to observe if there is a single connected component, 
or a single giant component or multiple small trees.

(c) Compute the diameters of these graphs and match them with the theoretical results.

(d) Place replicas of objects at random locations. Choose various values of the population density 
(the fraction of nodes that will have a replica of the object) between 0.001 and 0.01.

(e) Now, run various search algorithms
(i) using Gnutella-type flooding
(ii) using the random walker model and
(iii) using the k-random walker model with one-hop replication for different values of k as 
proposed in Gnutella Gia paper [Paper 3 in the Readings List].
In each case, compute the search time from multiple trials, as well as the total number of nodes visited to locate the object. 
Then compare the performances of these different search algorithms.


import networkx as nx
import matplotlib.pyplot as plt




# used http://dbrownbeta.blogs.cultureplex.ca/2013/02/18/math-is-the-path-degree-distribution-of-the-prelims-graph-and-other-randomness/
# as guidance for plotting degree distribution
# helper function to create plot of degree distribution
def graph_distribution(graph):
	DegHist = nx.degree_histogram(graph)
	xvals = []
	yvals = []

	for degree,num in enumerate(DegHist):
		if num > 0:
			xvals.append(log(degree))
			yvals.append(log(num))

	plt.title('Degree Distribution')
	plt.xlabel('Degree')
	plt.ylabel('Frequency')


	plt.scatter(xvals,yvals)
	plt.show()

graphs = []

p = 0.0001
popd = .001
n = 500


for i in range(100):
	g = nx.erdos_renyi_graph(n,p)
	#graphs.append(g)
	fig = nx.draw(g)
	name = "img/n"+str(n)+"p"+str(p)[:6]+".png"
	plt.savefig(name)
	plt.clf()
	p += 0.0005
	n += 5


"""

import networkx as nx
import random
import matplotlib.pyplot as plt
import math
import time

#generate a number of random erdos renyi graphs of sizes and prob from 0.0001 to 0.05
p = 0.01
n = 500
#while p <= 0.05 :
#    p += 0.0501/100

graph1 = nx.erdos_renyi_graph(n, p)

nx.set_node_attributes(graph1, "targetNode", False)
nx.set_node_attributes(graph1, "visited", False)

p = 0.0001
number = .05 - .0001
xList = []
yList = []
#iterations = 0
while p <= 0.05:
    #print(p)
    graph1 = nx.erdos_renyi_graph(n, p)
    if nx.is_connected(graph1) == True:
        graphDiameter = nx.diameter(graph1)
        yList.append(p)
        xList.append(graphDiameter)
        print("The diameter is: "+ str(graphDiameter))
    else:
        print("Diameter cannot be found")
    p += number/100

plt.title('Diameter Distribution Graph')
plt.xlabel('Diameter')
plt.ylabel('Probability')
    
plt.scatter(xList,yList)
plt.show()
#plt.savefig("DegreeDistributionGraph.png")

    
if nx.is_connected(graph1) == True:
    print("The diameter is: "+ str(nx.diameter(graph1)))
else:
    print("Diameter cannot be found")

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
                if len(nodesToCheck) == 0:
                    print ("unable to find target node.")
                    return ("unable to find target node.")
            nodesVisited += 1


#randomWalk(graph1)
#kRandomWalk(graph1,5)
#gnutellaFlooding(graph1)
print("done")

"""
fig = nx.draw(g)
name = "img/n"+str(n)+"p"+str(p)[:6]+".png"
plt.savefig(name)
plt.clf()
"""




















