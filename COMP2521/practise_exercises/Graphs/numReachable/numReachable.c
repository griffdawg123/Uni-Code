
#include <stdio.h>
#include <stdlib.h>

#include "Graph.h"

void doNumReachable(Graph g, int src, int *visited);

int numReachable(Graph g, int src) {
	int numVertices = GraphNumVertices(g);
	int *visited = calloc(numVertices, sizeof(int));
	visited[src] = true;
	doNumReachable(g, src, visited);
	int numReachable = 0;
	for (int i = 0; i < numVertices; i++) {
		numReachable += visited[i];
	}
	free(visited);
	return numReachable;
}

void doNumReachable(Graph g, int src, int *visited) {
	int numVertices = GraphNumVertices(g);
	for (int v = 0; v < numVertices; v++) {
		if (GraphIsAdjacent(g, src, v) && !visited[v]) {
			visited[v] = true;
			doNumReachable(g, v, visited);
		}
	}
}