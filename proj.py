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
	graphs.append(g)
	fig = nx.draw(g)
	name = "plots/graphs/n"+str(n)+"p"+str(p)[:6]+".png"
	plt.savefig(name)
	plt.clf()
	p += 0.0005
	n += 5
	
















