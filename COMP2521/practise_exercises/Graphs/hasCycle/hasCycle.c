
#include <stdio.h>
#include <stdlib.h>

#include "Graph.h"
#include "Stack.h"

bool doHasCycle(Graph g, int *visited, int src, int curr);

bool hasCycle(Graph g) {
	int numVertices = GraphNumVertices(g);
	bool cycle;
	for (int i = 0; i < numVertices; i++) {
		int *visited = calloc(numVertices, sizeof(g));
		visited[i] = true;
		cycle = doHasCycle(g, visited, i, i);
		free(visited);
		if (cycle) {
			break;
		}
	}
	return cycle;
}

bool doHasCycle(Graph g, int *visited, int src, int curr) {
	int numVertices = GraphNumVertices(g);
	for (int v = 0; v < numVertices; v++) {
		if (GraphIsAdjacent(g, curr, v)) {
			if ((v == src && curr != src) || doHasCycle(g, visited, src, v)) {
				return true;
			} 
		}
	}
	return false;
}

