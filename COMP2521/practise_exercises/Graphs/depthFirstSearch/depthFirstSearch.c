
#include <stdio.h>
#include <stdlib.h>

#include "Graph.h"

void doDepthFirstSearch(Graph g, int src, int *visited);

void depthFirstSearch(Graph g, int src) {
	int numVertices = GraphNumVertices(g);
	int *visited = calloc(numVertices, sizeof(int));
	doDepthFirstSearch(g, src, visited);
	free(visited);
}

void doDepthFirstSearch(Graph g, int src, int *visited) {
	int numVertices = GraphNumVertices(g);
	printf("%d ", src);
	visited[src] = 1;
	for (int v = 0; v < numVertices; v++) {
		if (GraphIsAdjacent(g, src, v) && visited[v] == 0) {
			doDepthFirstSearch(g, v, visited);
		}
	}
}
