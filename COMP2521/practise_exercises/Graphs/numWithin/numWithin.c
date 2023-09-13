
#include <stdio.h>
#include <stdlib.h>

#include "Graph.h"
#include "Queue.h"

int numWithin(Graph g, int src, int dist) {
	int numVertices = GraphNumVertices(g);
	Queue q = QueueNew();
	QueueEnqueue(q, src);
	int *visited = calloc(numVertices, sizeof(int));
	int *distMatrix = calloc(numVertices, sizeof(int));
	for (int v = 0; v < numVertices; v++) {
		distMatrix[v] = -1;
	}
	visited[src] = true;
	distMatrix[src] = 0;
	while (!QueueIsEmpty(q)) {
		int curr = QueueDequeue(q);
		for (int v = 0; v < numVertices; v++) {
			if (GraphIsAdjacent(g, curr, v) && !visited[v]) {
				QueueEnqueue(q, v);
				visited[v] = true;
				distMatrix[v] = distMatrix[curr] + 1;
			}
		}
	}
	int within = 0;
	for (int v = 0; v < numVertices; v++) {
		if (distMatrix[v] <= dist && distMatrix[v] >= 0) {
			within++;
		}
	}
	QueueFree(q);
	free(visited);
	free(distMatrix);
	return within;
}

