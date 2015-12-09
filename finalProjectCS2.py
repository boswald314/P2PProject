# -*- coding: utf-8 -*-
"""
Final Project - (Project #2)
By: Zachary Cain & Bryan Oswald

@author: ZachCain
Student ID: 00792287

"""

import networkx as nx
import random
import matplotlib.pyplot as plt
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
					return (0,0)
			nodesVisited += 1


def diameterDist(n, minp, maxp):
    number = maxp - minp
    xList = []
    yList = []
    p = minp
    while p <= maxp:
        graph = nx.erdos_renyi_graph(n, p)
        if nx.is_connected(graph) == True:
            graphDiameter = nx.diameter(graph)
            yList.append(p)
            xList.append(graphDiameter)
        p += number/100
        #print(p)
    
    plt.title('Diameter Distribution Graph, n = {}'.format(str(n)))
    plt.xlabel('Diameter')
    plt.ylabel('Probability')
    plt.scatter(xList,yList)
    plt.savefig("DiameterDistributionGraph{}.png".format(str(n)))


def main1():
    # Degree distribution for n = 500
    diameterDist(500,0.0001,0.05)
    print("Graph for Diameter distribution, n = 500 made!")
    
    # Degree distribution for n = 1000
    diameterDist(1000,0.0001,0.05)
    print("Graph for Diameter distribution, n = 1000 made!")
    """
    # Degree distribution for n = 2000
    degDist(2000,0.0001,0.05)
    print("Graph for Diameter distribution, n = 2000 made!")
    # Degree distribution for n = 5000
    degDist(5000,0.0001,0.05)
    print("Graph for Diameter distribution, n = 5000 made!")
    """
    
main1()

def main():

    #kRandomWalk(graph1,5)
    #gnutellaFlooding(graph1)
    graphs500 = []
    graphs1000 = []
    graphs2000 = []
    graphs5000 = []
    listlist = [graphs500]
    
    p = 0
    n = 500
    probabilityList = []
    while p <= 0.05 :
    	p += 0.0005
    	graphs500.append(nx.erdos_renyi_graph(n,p))
    	probabilityList.append(p)
    
    
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
     
    	#going threw the 100 graphs for each 500,1000,2000,5000
    	for graph in graphlist:
    		
    		nx.set_node_attributes(graph, "targetNode", False)
    		nx.set_node_attributes(graph, "visited", False)
    
    		#base population density
    		density = 0.001
    		while density <= .01:
    			
    			nx.set_node_attributes(graph, "targetNode", False)
    			numberOfNodes = graph.number_of_nodes()
    			for i in range(int(numberOfNodes*density)):
    				numberOfNodes -= 1
    				graph.node[random.randint(0, numberOfNodes)]['targetNode'] = True
        
    			res = randomWalk(graph)
    			RW_res.append(res)
    
    			nx.set_node_attributes(graph, "visited", False)
    			kRW_res.append(kRandomWalk(graph,5))
    
    			nx.set_node_attributes(graph, "visited", False)
    			flood_res.append(gnutellaFlooding(graph))
    
    			nx.set_node_attributes(graph, "visited", False)
    			density += 0.001
    			density = float(str(density)[:6])
    
    
    
    	X_Values_nodes = []
    	X_Values_time = []
    
    
    
    	for x in range(10):
    		X_Values_nodes = []
    		X_Values_time = []
    
    		for i in range(0,len(RW_res),10):
    			#Gives us the list of NodesVisted and Time for Density = 0.001
    			X_Values_nodes.append(RW_res[i+x][0])
    			X_Values_time.append(RW_res[i+x][1])
    
    		#print(len(RW_res))
    
    		
    		plt.title("Random Walker N=500 Population Density={}".format(str(densityList[x])[:6]))
    		plt.xlabel("Nodes Visited")
    		plt.ylabel("probability value")
    		plt.scatter(X_Values_nodes,probabilityList)
    		plt.savefig("plots/nodes/walker/plotDensity{}.png".format(str(densityList[x])[:6]))
    		plt.clf()
    
    
    		plt.title("Random Walker N=500 Population Density={}".format(str(densityList[x])[:6]))
    		plt.xlabel("Time to complete (seconds)")
    		plt.ylabel("probability value")
    		plt.scatter(X_Values_time,probabilityList)
    		plt.savefig("plots/time/walker/timeAtDensity{}.png".format(str(densityList[x])[:6]))
    		plt.clf()
    
    	for x in range(10):
    		X_Values_nodes = []
    		X_Values_time = []
    
    		for i in range(0,len(kRW_res),10):
    			#Gives us the list of NodesVisted and Time for Density = 0.001
    			X_Values_nodes.append(kRW_res[i+x][0])
    			X_Values_time.append(kRW_res[i+x][1])
    
    		#print(len(RW_res))
    
    		
    		plt.title("K Random Walker N=500 Population Density={}".format(str(densityList[x])[:6]))
    		plt.xlabel("Nodes Visited")
    		plt.ylabel("probability value")
    		plt.scatter(X_Values_nodes,probabilityList)
    		plt.savefig("plots/nodes/kwalker/kplotDensity{}.png".format(str(densityList[x])[:6]))
    		plt.clf()
    
    
    		plt.title("K Random Walker N=500 Population Density={}".format(str(densityList[x])[:6]))
    		plt.xlabel("Time to complete (seconds)")
    		plt.ylabel("probability value")
    		plt.scatter(X_Values_time,probabilityList)
    		plt.savefig("plots/time/kwalker/ktimeAtDensity{}.png".format(str(densityList[x])[:6]))
    		plt.clf()
    
    	for x in range(10):
    		X_Values_nodes = []
    		X_Values_time = []
    
    		for i in range(0,len(flood_res),10):
    			#Gives us the list of NodesVisted and Time for Density = 0.001
    			X_Values_nodes.append(flood_res[i+x][0])
    			X_Values_time.append(flood_res[i+x][1])
    
    		#print(len(RW_res))
    
    		
    		plt.title("Gnutella Flood N=500 Population Density={}".format(str(densityList[x])[:6]))
    		plt.xlabel("Nodes Visited")
    		plt.ylabel("probability value")
    		plt.scatter(X_Values_nodes,probabilityList)
    		plt.savefig("plots/nodes/flood/floodplotDensity{}.png".format(str(densityList[x])[:6]))
    		plt.clf()
    
    
    		plt.title("Gnutella Flood N=500 Population Density={}".format(str(densityList[x])[:6]))
    		plt.xlabel("Time to complete (seconds)")
    		plt.ylabel("probability value")
    		plt.scatter(X_Values_time,probabilityList)
    		plt.savefig("plots/time/flood/floodtimeAtDensity{}.png".format(str(densityList[x])[:6]))
    		plt.clf()



