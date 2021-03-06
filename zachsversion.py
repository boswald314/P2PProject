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

"""

import networkx as nx
import random
import matplotlib.pyplot as plt
import math
import time


	
def randomWalk(graph):
	numberOfNodes = graph.number_of_nodes() -1
	startNode = random.randint(0, numberOfNodes)
	nodesVisited = 1
	start = time.time()
	while (graph.node[startNode]['targetNode'] == False):
		graph.node[startNode]['visited'] = True
		possibleNextStep = graph.neighbors(startNode)
		if len(possibleNextStep) == 0:
			return 0
		startNode = random.choice(possibleNextStep)
		while graph.node[startNode]['visited'] == True:
			possibleNextStep.remove(startNode)
			if len(possibleNextStep) != 0:
				startNode = random.choice(possibleNextStep)
			else:
				return 0
				
		nodesVisited +=1

	end = time.time()
	elapsedtime = end - start
	return (nodesVisited,elapsedtime)
	  


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
				return (nodesVisited,end-start,hopsBeforeFound)
			else:
				possibleNextStep = graph.neighbors(i)
				if len(possibleNextStep) == 0:
					return 0
				startNode = random.choice(possibleNextStep)
				while graph.node[startNode]['visited'] == True:
					possibleNextStep.remove(startNode)
					if len(possibleNextStep) != 0:
						startNode = random.choice(possibleNextStep)
					else:
						return 0
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
				return (nodesVisited, end-start)
			else:
				neighbors = graph.neighbors(i)
				for item in neighbors:
					if graph.node[item]['visited'] == False:
						nodesToCheck.append(item)
				nodesToCheck.remove(i)
				if len(nodesToCheck) == 0:
					return 0
			nodesVisited += 1


def degDist(n, minp, maxp):
	number = maxp - minp
	xList = []
	yList = []
	#iterations = 0
	while p <= 0.05:
		#print(p)
		graph = nx.erdos_renyi_graph(n, p)
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
	#plt.show()
	plt.savefig("DegreeDistributionGraph.png")



#graph1 = nx.erdos_renyi_graph(n, p)



'''
if nx.is_connected(graph1) == True:
	print("The diameter is: "+ str(nx.diameter(graph1)))
else:
	print("Diameter cannot be found")
'''




#kRandomWalk(graph1,5)
#gnutellaFlooding(graph1)
graphs500 = []
graphs1000 = []
graphs2000 = []
graphs5000 = []
graphlist = [graphs500]#, graphs1000, graphs2000, graphs5000]
#generate a number of random erdos renyi graphs of sizes and prob from 0.0001 to 0.05

p = 0.0001
n = 500
ppList = []
while p <= 0.05 :
   	graphs500.append(nx.erdos_renyi_graph(n,p))
   	ppList.append(p)
   	p += 0.000499
'''
p = 0.0001
n = 1000
while p <= 0.05 :
   	graphs1000.append(nx.erdos_renyi_graph(n,p))   
   	p += 0.000499	

p = 0.0001
n = 2000
while p <= 0.05 :
   	graphs2000.append(nx.erdos_renyi_graph(n,p))
   	p += 0.000499

p = 0.0001
n = 5000
while p <= 0.05 :
   	graphs5000.append(nx.erdos_renyi_graph(n,p))
   	p += 0.000499
'''

res500 = []
res1000 = []
res2000 = []
res5000 = []


#graphs of size 500,1000,2000,5000
for glist in graphlist:

	RW_res = []
	kRW_res = []
	flood_res = []

	#going threw the 100 graphs for each 500,1000,2000,5000
	popdensity = 0.001
	while popdensity <= .01:
		for i in range(int(numberOfNodes*popdensity)):
				numberOfNodes -= 1
				graph.node[random.randint(0, numberOfNodes)]['targetNode'] = True

		
		nx.set_node_attributes(graph, "targetNode", False)
		nx.set_node_attributes(graph, "visited", False)

		for graph in glist:

			nx.set_node_attributes(graph, "targetNode", False)
			numberOfNodes = graph.number_of_nodes()
			
			
			RW_res.append(randomWalk(graph))

			nx.set_node_attributes(graph, "visited", False)
			kRW_res.append(kRandomWalk(graph,5))

			nx.set_node_attributes(graph, "visited", False)
			flood_res.append(gnutellaFlooding(graph))

			nx.set_node_attributes(graph, "visited", False)
		popdensity += 0.001
		#										first 10 are for 0.001 endos and .001 to .01 popdensity
		#at this point point we have a list = 	[pop = 0.001(x,y),pop=.002(x,y)...pop=.01(x,y) |||  
		#onto next 10 with p=.00015 - pop = 0.001(x,y),pop=.002(x,y)...pop=.01(x,y) ]
		#										where x = nodes and y = time


		#pop = 0.0001
		#popden .001 to .01
		#^^ first 10

		#pop = 0.0001 + .499
		#next 10



		#x = nodes visited
		#y = probability
		#graph with target node population at 0.001, n = 500
		#add of the ones with 0.001 pop


	#RW_res is list of two tuples (nodesVisted, timeElapsed)

	X_Values_nodes = []
	X_Values_time = []
	myY_Values = []
	for pval in ppList:
		for i in range(10):
			X_Values_nodes.append(RW_res[i][0])
			X_Values_time.append(RW_res[i][1])
		myY_Values.append(pval)




	plt.title("Random Walk N=500 p=0.0001")

'''
	X_Values_nodes = []
	X_Values_time = []
	myY_Values = []
	for pval in ppList:
		for i in range(10):
			X_Values_nodes.append(RW_res[i][0])
			X_Values_time.append(RW_res[i][1])


	X_Values_nodes = []
	X_Values_time = []
	myY_Values = []
	for pval in ppList:
		for i in range(10):
			X_Values_nodes.append(RW_res[i][0])
			X_Values_time.append(RW_res[i][1])

'''







