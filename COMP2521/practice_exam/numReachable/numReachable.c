
#include <stdio.h>
#include <stdlib.h>

#include "Graph.h"

void reachable(Graph g, int curr, int *seen);

int numReachable(Graph g, int src) {
	int numNodes = GraphNumVertices(g);
	int *seen = calloc(numNodes, sizeof(int));
	reachable(g, src, seen);
	int reached = 0;
	for (int i = 0; i < numNodes; i++) {
		if (seen[i]) {
			reached++;
		}
	}
	free(seen);
	return reached;
}

void reachable(Graph g, int curr, int *seen) {
	int numNodes = GraphNumVertices(g);
	seen[curr] = 1;
	for (int v = 0; v < numNodes; v++) {
		if (!seen[v] && GraphIsAdjacent(g, curr, v)) {
			reachable(g, v, seen);
		}
	}
}