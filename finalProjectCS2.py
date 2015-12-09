# -*- coding: utf-8 -*-
"""
Final Project

@author: ZachCain
@author: Bryan Oswald

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
import time


	
def randomWalk(graph):
	'''
		Performs random walk to find target node
			takes graph object as single parameter
		Returns tuple:
			(number of nodes visited, time elapsed)
			if node cannot be found, both values are returned 0
	'''
	numberOfNodes = graph.number_of_nodes() -1
	startNode = random.randint(0, numberOfNodes)
	nodesVisited = 1
	start = time.time()
	while (graph.node[startNode]['targetNode'] == False):
		graph.node[startNode]['visited'] = True
		possibleNextStep = graph.neighbors(startNode)
		if len(possibleNextStep) == 0:
			return (0,0)
		startNode = random.choice(possibleNextStep)
		while graph.node[startNode]['visited'] == True:
			possibleNextStep.remove(startNode)
			if len(possibleNextStep) != 0:
				startNode = random.choice(possibleNextStep)
			else:
				return (0,0)
				
		nodesVisited +=1

	end = time.time()
	elapsedtime = end - start
	return (nodesVisited,elapsedtime)
	  


def kRandomWalk(graph,k=5):
	'''
		Performs k random walk to find target node
			takes graph object as first parameter
			takes k value (correspoding to number of random walkers) as second parameter
		Returns tuple:
			(number of nodes visited, time elapsed, hops made (by each walker, not total))
			if node cannot be found, all values are returned 0
	'''
	numberOfNodes = graph.number_of_nodes()
	startNodes = [0]*k
	for i in range(0,k):
		nodeToAdd = random.randint(0, numberOfNodes - 1)
		while nodeToAdd in startNodes[:i]:
			nodeToAdd = random.randint(0, numberOfNodes - 1)
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
					return (0,0,0)

				for item in possibleNextStep:
					if graph.node[item]['targetNode'] == True:
						end = time.time()
						return (nodesVisited,end-start,hopsBeforeFound)
				startNode = random.choice(possibleNextStep)
				while graph.node[startNode]['visited'] == True:
					possibleNextStep.remove(startNode)
					if len(possibleNextStep) != 0:
						startNode = random.choice(possibleNextStep)
					else:
						return (0,0,0)
				startNodes[index] = startNode
				index +=1
				nodesVisited +=1
		hopsBeforeFound +=1




def gnutellaFlooding(graph, ttl=7):
	'''
		Performs gnutella flooding to find target node
			takes graph object as first parameter
			second parameter is ttl of flood, defaults to 7
		Returns tuple:
			(number of nodes visited, time elapsed)
			if node cannot be found, both values are returned 0
	'''
	numberOfNodes = graph.number_of_nodes()
	nodesToCheck = [random.randint(0, numberOfNodes - 1)]
	nodesVisited = 1
	
	start = time.time()
	while True:
		if (nodesVisited > ttl):
			return(0, 0)
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
					return (0,0)
			nodesVisited += 1





def diamDist(n, minp, maxp):
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
	plt.savefig("DiameterDistributionGraph.png")






def run():

	graphs500 = []
	graphs1000 = []
	graphs2000 = []
	graphs5000 = []
	listlist = [graphs500, graphs1000, graphs2000, graphs5000]


	#generate a number of random erdos renyi graphs of sizes and prob from 0.0001 to 0.05
	FACTOR = 100

	p = 0
	n = 5 * FACTOR
	ppList = []
	while p <= 0.05 :
		p += 0.0005
		graphs500.append(nx.erdos_renyi_graph(n,p))
		ppList.append(p)
		

	p = 0
	n = 10 * FACTOR
	while p <= 0.05 :
		p += 0.0005	
		graphs1000.append(nx.erdos_renyi_graph(n,p))   

	p = 0
	n = 20 * FACTOR
	while p <= 0.05 :
		p += 0.0005
		graphs2000.append(nx.erdos_renyi_graph(n,p))

	p = 0
	n = 50 * FACTOR
	while p <= 0.05 :
		p += 0.0005
		graphs5000.append(nx.erdos_renyi_graph(n,p))


	res500 = []
	res1000 = []
	res2000 = []
	res5000 = []

	x = 0.001
	densityList = []
	for i in range(10):
		densityList.append(x)
		x += 0.001

	#graphs of size 500,1000,2000,5000
	for graphlist in listlist:
		graphindex = 0

		RW_res = []
		kRW_res = []
		flood_res = []


		#going through the 100 graphs for each 500,1000,2000,5000
		for graph in graphlist:
			
			nx.set_node_attributes(graph, "targetNode", False)
			nx.set_node_attributes(graph, "visited", False)

			#base population density
			density = 0.001
			while density <= .01:
				nx.set_node_attributes(graph, "targetNode", False)
				numberOfNodes = graph.number_of_nodes()
				for i in range(int(numberOfNodes*density)):
					graph.node[random.randint(0,numberOfNodes-1)]['targetNode'] = True
				res = randomWalk(graph)
				#print(res)
				RW_res.append(res)

				nx.set_node_attributes(graph, "visited", False)
				kRW_res.append(kRandomWalk(graph,5))

				nx.set_node_attributes(graph, "visited", False)
				flood_res.append(gnutellaFlooding(graph))

				nx.set_node_attributes(graph, "visited", False)
				density += 0.001
				density = float(str(density)[:6])

			'''
			nx.draw(graph)
			plt.savefig("plots/graphs/Graph with N={} and p={}.png".format(numberOfNodes, ppList[graphindex]))
			plt.clf
			'''


		X_Values_nodes = []
		X_Values_time = []
		
		#RW_res is list of two tuples (nodesVisted, timeElapsed)

		for x in range(10):
			X_Values_nodes = []
			X_Values_time = []

			for i in range(0,len(RW_res),10):
				#Gives us the list of NodesVisted and Time for Density = 0.001
				X_Values_nodes.append(RW_res[i+x][0])
				X_Values_time.append(RW_res[i+x][1])


			
			plt.title("Random Walker N={} Population Density={}".format(str(numberOfNodes), str(densityList[x])[:6]))
			plt.xlabel("Nodes Visited")
			plt.ylabel("probability value")
			plt.scatter(X_Values_nodes,ppList)
			plt.savefig("plots/nodes/walker/N={}plotDensity{}.png".format(str(numberOfNodes), str(densityList[x])[:6]))
			plt.clf()


			plt.title("Random Walker N={} Population Density={}".format(str(numberOfNodes), str(densityList[x])[:6]))
			plt.xlabel("Time to complete (seconds)")
			plt.ylabel("probability value")
			plt.scatter(X_Values_time,ppList)
			plt.savefig("plots/time/walker/N={}timeAtDensity{}.png".format(str(numberOfNodes), str(densityList[x])[:6]))
			plt.clf()

			X_Values_nodes = []
			X_Values_time = []


			for i in range(0,len(kRW_res),10):
				#Gives us the list of NodesVisted and Time for Density = 0.001
				X_Values_nodes.append(kRW_res[i+x][0])
				X_Values_time.append(kRW_res[i+x][1])

			
			plt.title("K Random Walker N={} Population Density={}".format(str(numberOfNodes), str(densityList[x])[:6]))
			plt.xlabel("Nodes Visited")
			plt.ylabel("probability value")
			plt.scatter(X_Values_nodes,ppList)
			plt.savefig("plots/nodes/kwalker/N={}kplotDensity{}.png".format(str(numberOfNodes), str(densityList[x])[:6]))
			plt.clf()


			plt.title("K Random Walker N={} Population Density={}".format(str(numberOfNodes), str(densityList[x])[:6]))
			plt.xlabel("Time to complete (seconds)")
			plt.ylabel("probability value")
			plt.scatter(X_Values_time,ppList)
			plt.savefig("plots/time/kwalker/N={}ktimeAtDensity{}.png".format(str(numberOfNodes), str(densityList[x])[:6]))
			plt.clf()

			X_Values_nodes = []
			X_Values_time = []



			for i in range(0,len(flood_res),10):
				#Gives us the list of NodesVisted and Time for Density = 0.001
				X_Values_nodes.append(flood_res[i+x][0])
				X_Values_time.append(flood_res[i+x][1])


			
			plt.title("Gnutella Flood N={} Population Density={}".format(str(numberOfNodes), str(densityList[x])[:6]))
			plt.xlabel("Nodes Visited")
			plt.ylabel("probability value")
			plt.scatter(X_Values_nodes,ppList)
			plt.savefig("plots/nodes/flood/N={}floodplotDensity{}.png".format(str(numberOfNodes), str(densityList[x])[:6]))
			plt.clf()


			plt.title("Gnutella Flood N={} Population Density={}".format(str(numberOfNodes), str(densityList[x])[:6]))
			plt.xlabel("Time to complete (seconds)")
			plt.ylabel("probability value")
			plt.scatter(X_Values_time,ppList)
			plt.savefig("plots/time/flood/N={}floodtimeAtDensity{}.png".format(str(numberOfNodes), str(densityList[x])[:6]))
			plt.clf()


		X_Values_nodes = []
		X_Values_time = []


def getRandomNode(graph):
	nodes = graph.number_of_nodes()
	return graph.node[random.randint(0, nodes - 1)]

def initializeGraph(graph,popd):
	nx.set_node_attributes(graph, "targetNode", False)
	nx.set_node_attributes(graph, "visited", False)

	numberOfObjects = int(graph.number_of_nodes() * popd)
	for i in range(numberOfObjects):
		node = getRandomNode(graph)
		node['targetNode'] = True

	return graph





def test(n=1000,p=0.01,popd=0.005):
	n = int(n)
	p = float(p)
	popd = float(popd)

	graph = nx.erdos_renyi_graph(n,p)
	graph = initializeGraph(graph, popd)

	print("The graph contained {} nodes, was generated with p={}, and has an object density of {}".format(n,p,popd))
	res = randomWalk(graph)
	print("The random walker visited {} nodes and took {} seconds".format(res[0],res[1]))
	nx.set_node_attributes(graph, "visited", False)
	res = kRandomWalk(graph,5)
	print("The k random walkers visited {} nodes over {} seconds and {} rounds of hops".format(res[0],res[1],res[2]))
	res = gnutellaFlooding(graph)
	print("The gnutella flood sent {} queries and took {} seconds\n".format(res[0],res[1]))



def listcommands(cmd=''):
	print("Commands available:")
	if (cmd==''):
		print("test: simple test function, generates a graph and lists results for each search strategy")
		print("run: runs main function we used to generate graphs, search, and plot results (warning -- long run time)")
		print("end: exit")
		print("help: display this message")
	elif (cmd=='test'):
		print("test generates a graph and lists results for each search strategy")
		print("It takes three optional parameters:")
		print("\tN: number of nodes in graph to be used")
		print("\tp: value of p to be used in generating Erdos-Renyi graph")
		print("\tpopd: the population density at which objects should appear in the graph")

	print("\n")



if __name__ == "__main__":
	funcs = {"test":test, "run":run, "help":listcommands}

	print("Type a command. ('help' for help)\n")

	while True:
		x = input().split(' ')
		if (x == "end"):
			break
		else:
			fun = funcs.get(x[0])
			fun(*x[1:])















