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
from collections import defaultdict




class Graph:
	def __init__(self, n, p, popd=0.001):
		n = int(n)
		p = float(p)
		self.graph = nx.erdos_renyi_graph(n,p)
		self.initializeGraph(popd)

	def isConnected(self):
		'''
			Returns True if graph is connected, else False
		'''
		return nx.is_connected(self.graph)

	def getRandomNode(self):
		'''
			Returns a node selected at random from the graph
		'''
		nodes = self.graph.number_of_nodes()
		return self.graph.node[random.randint(0, nodes - 1)]

	def number_of_nodes(self):
		'''
			Returns the number of nodes in the graph
		'''
		return nx.number_of_nodes(self.graph)

	def numberOfComponents(self):
		'''
			Returns the number of distinct components in the graph
		'''
		return nx.number_connected_components(self.graph)

	def connectedSubgraphs(self):
		'''
			Returns connected subgraphs as iterable of graphs
		'''
		return nx.connected_component_subgraphs(self.graph)

	def diameter(self):
		return nx.diameter(self.graph)


	def help(self):
		print("isConnected: Returns True if graph is connected, else False\n")
		print("number_of_nodes: Returns the number of nodes in the graph\n")
		print("numberOfComponents: Returns the number of distinct components in the graph\n")
		print("randomWalk: Performs random walk to find target node\n\ttakes graph object as single parameter\nReturns tuple:\n\t(number of nodes visited, time elapsed)\n\tif node cannot be found, both values are returned 0\n")
		print("kRandomWalk: Performs k random walk to find target node\ntakes graph object as first parameter\n\ttakes k value (correspoding to number of random walkers) as second parameter\nReturns tuple:\n\t(number of nodes visited, time elapsed, hops made (by each walker, not total))\n\tif node cannot be found, all values are returned 0\n")
		print("gnutellaFlooding: Performs gnutella flooding to find target node\ntakes ttl as first parameter (deafault is 7)\nReturns tuple:\n\t(number of nodes visited, time elapsed)\n\tif node cannot be found, both values are returned 0\n")
		print("show: draws and displays graph")

	def listen(self):
		'''
			for real time interaction with graph object
			provides access to functions and attributes from cli
		'''
		functs = {"gnuFlood":self.gnuFlood, "help":self.help,"isConnected":self.isConnected,"number_of_nodes":self.number_of_nodes,"numberOfComponents":self.numberOfComponents,"randomWalk":self.randomWalk,"kRandomWalk":self.kRandomWalk,"gnutellaFlooding":self.gnutellaFlooding,"show":self.show}
		while True:
			x = input().strip().split()
			if (x == "end"):
				break
			else:
				fun = functs.get(x[0])
				if (fun == None):
					break
				print(fun(*x[1:]))

	def show(self):
		nx.draw(self.graph)
		plt.show()

	def initializeGraph(self, popd):
		'''
			Set node attributes for targetNode and visited to False for all nodes in graph
		'''
		nx.set_node_attributes(self.graph, "targetNode", False)
		nx.set_node_attributes(self.graph, "visited", False)

		numberOfObjects = int(self.graph.number_of_nodes() * popd)
		for i in range(numberOfObjects):
			node = self.getRandomNode()
			node['targetNode'] = True

	def randomWalk(self):
		'''
			Performs random walk to find target node
				takes graph object as single parameter
			Returns tuple:
				(number of nodes visited, time elapsed)
				if node cannot be found, both values are returned 0
		'''
		numberOfNodes = self.graph.number_of_nodes() 
		startNode = random.randint(0, numberOfNodes - 1)
		nodesVisited = 1
		start = time.time()
		while (self.graph.node[startNode]['targetNode'] == False):
			self.graph.node[startNode]['visited'] = True
			possibleNextStep = self.graph.neighbors(startNode)
			if len(possibleNextStep) == 0:
				return (0,0)
			startNode = random.choice(possibleNextStep)
			while self.graph.node[startNode]['visited'] == True:
				possibleNextStep.remove(startNode)
				if len(possibleNextStep) != 0:
					startNode = random.choice(possibleNextStep)
				else:
					return (0,0)
					
			nodesVisited +=1

		end = time.time()
		elapsedtime = end - start
		return (nodesVisited,elapsedtime)


	def kRandomWalk(self,k=5):
		'''
			Performs k random walk to find target node
				takes graph object as first parameter
				takes k value (correspoding to number of random walkers) as second parameter
			Returns tuple:
				(number of nodes visited, time elapsed, hops made (by each walker, not total))
				if node cannot be found, all values are returned 0
		'''
		numberOfNodes = self.graph.number_of_nodes()
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
				self.graph.node[i]['visited'] = True
				if self.graph.node[i]['targetNode'] == True:
					end = time.time()
					return (nodesVisited,end-start,hopsBeforeFound)
				else:
					possibleNextStep = self.graph.neighbors(i)

					if len(possibleNextStep) == 0:
						return (0,0,0)

					for item in possibleNextStep:
						if self.graph.node[item]['targetNode'] == True:
							end = time.time()
							return (nodesVisited,end-start,hopsBeforeFound)
					startNode = random.choice(possibleNextStep)
					while self.graph.node[startNode]['visited'] == True:
						possibleNextStep.remove(startNode)
						if len(possibleNextStep) != 0:
							startNode = random.choice(possibleNextStep)
						else:
							return (0,0,0)
					startNodes[index] = startNode
					index +=1
					nodesVisited +=1
			hopsBeforeFound +=1

	def gnutellaFlooding(self, ttl=7):
		'''
			Performs gnutella flooding to find target node
				takes graph object as first parameter
				second parameter is ttl of flood, defaults to 7
			Returns tuple:
				(number of nodes visited, time elapsed)
				if node cannot be found, both values are returned 0
		'''
		numberOfNodes = self.graph.number_of_nodes()
		initialNode = (random.randint(0, numberOfNodes - 1))
		nodesVisited = 0
		nodesToCheck = [initialNode]

		start = time.time()
		for i in range(ttl):
			for node in nodesToCheck:
				if self.graph.node[node]['targetNode'] == True:
					end = time.time()
					return (nodesVisited, end-start)
				else:
					for neighbor in self.graph.neighbors(node):
						nodesToCheck.append(neighbor)
					nodesToCheck.remove(node)
				nodesVisited += 1
		return (0,0)





def diameterDist(n=500, minp=0.0001, maxp=0.05, graphs=100):
	'''
		Plots diameter distribution for Erdos-Renyi graphs with p in range(0.0001,0.05)
			if graph is not connected it is discarded
	'''
	stepSize = (maxp - minp) / graphs
	xList = []
	yList = []
	p = minp
	while p <= maxp:
		graph = Graph(n, p)
		if (graph.isConnected()) == True:
			yList.append(p)
			xList.append(graph.diameter())
		p += stepSize
	
	plt.title('Diameter Distribution Graph, n = {}'.format(str(n)))
	plt.xlabel('Diameter')
	plt.ylabel('Probability')
	plt.scatter(xList,yList)
	plt.savefig("diamDistN={}minp={}maxp={}graphs={}.png".format(str(n),minp,maxp,graphs))



def run(FACTOR=100):

	graphs500 = []
	graphs1000 = []
	graphs2000 = []
	graphs5000 = []
	listlist = [graphs500, graphs1000, graphs2000, graphs5000]


	#generate a number of random erdos renyi graphs of sizes and prob from 0.0001 to 0.05

	p = 0
	n = 5 * FACTOR
	ppList = []
	while p <= 0.05 :
		p += 0.0005
		graphs500.append(Graph(n,p))
		ppList.append(p)
		

	p = 0
	n = 10 * FACTOR
	while p <= 0.05 :
		p += 0.0005	
		graphs1000.append(Graph(n,p))   

	p = 0
	n = 20 * FACTOR
	while p <= 0.05 :
		p += 0.0005
		graphs2000.append(Graph(n,p))

	p = 0
	n = 50 * FACTOR
	while p <= 0.05 :
		p += 0.0005
		graphs5000.append(Graph(n,p))


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
			
			nx.set_node_attributes(graph.graph, "targetNode", False)
			nx.set_node_attributes(graph.graph, "visited", False)

			#base population density
			density = 0.001
			while density <= .01:
				nx.set_node_attributes(graph.graph, "targetNode", False)
				numberOfNodes = graph.number_of_nodes()
				for i in range(int(numberOfNodes*density)):
					node = graph.getRandomNode()
					node['targetNode'] = True
				res = graph.randomWalk()
				#print(res)
				RW_res.append(res)

				nx.set_node_attributes(graph.graph, "visited", False)
				kRW_res.append(graph.kRandomWalk(5))

				nx.set_node_attributes(graph.graph, "visited", False)
				flood_res.append(graph.gnutellaFlooding())

				nx.set_node_attributes(graph.graph, "visited", False)
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




def test(n=1000,p=0.01,popd=0.005):
	n = int(n)
	p = float(p)
	popd = float(popd)

	graph = Graph(n,p)
	graph.initializeGraph(popd)

	print("The graph contained {} nodes, was generated with p={}, and has an object density of {}".format(n,p,popd))
	res = graph.randomWalk()
	print("The random walker visited {} nodes and took {} seconds".format(res[0],res[1]))
	nx.set_node_attributes(graph.graph, "visited", False)
	res = graph.kRandomWalk(5)
	print("The k random walkers visited {} nodes over {} seconds and {} rounds of hops".format(res[0],res[1],res[2]))
	res = graph.gnutellaFlooding()
	print("The gnutella flood sent {} queries and took {} seconds\n".format(res[0],res[1]))

def testFlood(n=1000,pmin=0.0001,pmax=0.05,popdmin=0.002,popdmax=0.009):
	n = int(n)
	pmin = float(pmin)
	pmax = float(pmax)
	popdmin = float(popdmin)
	popdmax = float(popdmax)

	print("Graph with {} nodes, starting flood trials".format(n))
	floodResults = []
	Y_values = []

	dStep = (popdmin + popdmax) / 10
	densityList = []
	density = popdmin
	for i in range(10):
		densityList.append(float(str(density)[:5]))
		density += dStep

	stepSize = (pmin + pmax) / 10
	p = pmin
	for i in range(10):
		Y_values.append(p)
		p += stepSize

	for density in densityList:
		for p in Y_values:
			graph = Graph(n, p, density)
			res = graph.gnutellaFlooding()
			floodResults.append(res[0])

	offset = 0
	for i in range(10):
		plt.title("Gnutella Flood N={} Population Density={}".format(n, densityList[i]))
		plt.xlabel("Nodes Visited")
		plt.ylabel("probability value")
		plt.scatter(floodResults[:10],Y_values)
		plt.savefig("plots/nodes/flood/N={}floodplotDensity{}.png".format(n, densityList[i]))
		plt.clf()

		floodResults = floodResults[10:]



def graphinfo(n=5000,p=0.0005):
	n = int(n)
	p = float(p)

	graph = Graph(n,p)
	print("Created graph with {} nodes and p = {}".format(n,p))

	print(graph.isConnected())
	if graph.isConnected():
		print("The graph is connected\n")
	else:
		print("The graph has {} componenets".format(graph.numberOfComponents()))

		componentSizes = []
		#componentSizes.append(graph.number_of_nodes())
		subgraphList = graph.connectedSubgraphs()
		for subgraph in subgraphList:
			componentSizes.append(subgraph.number_of_nodes())

		singleNodes = 0
		while componentSizes[-1] == 1:
			singleNodes += 1
			componentSizes = componentSizes[:-1]
		numMultiNodeComponents = len(componentSizes)


		subgraphList = graph.connectedSubgraphs()
		components = defaultdict(int)
		for subgraph in subgraphList:
			numNodes = subgraph.number_of_nodes()
			components[numNodes] += 1

		for size,num in components.items():
			print("There were {} components of size {}".format(num,size))
		print("\n")
				


def createGraph(n=1000,p=0.01):
	graph = Graph(n,p)
	graph.listen()


def listcommands(cmd=''):
	print("Commands available:")
	if (cmd==''):
		print("test: simple test function, generates a graph and lists results for each search strategy")
		print("run: runs main function we used to generate graphs, search, and plot results (warning -- VERY long run time -- used to generate plots)")
		print("graphinfo|gi: genrates a graph and prints information regarding its structure")
		print("Graph: generate a graph object which you can call functions on and read attributes from")
		print("diameterDist: Plots diameter distribution for Erdos-Renyi graphs of size n=500 with p from pmin=0.0001 to pmax=0.05 using graphs=100 graphs")
		print("end: exit")
		print("help: display this message")
	elif (cmd=='Graph'):
		print('create a Graph then type help for more info')
	elif (cmd=='test'):
		print("test generates a graph and lists results for each search strategy")
		print("It takes three optional parameters:")
		print("\tN: number of nodes in graph to be used")
		print("\tp: value of p to be used in generating Erdos-Renyi graph")
		print("\tpopd: the population density at which objects should appear in the graph")

	print("\n")




if __name__ == "__main__":
	funcs = {"test":test, "run":run, "help":listcommands, "graphinfo":graphinfo, "gi":graphinfo, "Graph":createGraph, "diameterDist":diameterDist, "testFlood":testFlood}

	print("Type a command. ('help' for help)\n")

	while True:
		x = input().strip().split(' ')
		if (x == "end"):
			break
		else:
			fun = funcs.get(x[0])
			if (fun == None):
				break
			fun(*x[1:])








			
