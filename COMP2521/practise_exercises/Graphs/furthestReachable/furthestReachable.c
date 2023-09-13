
#include <stdio.h>
#include <stdlib.h>

#include "Graph.h"
#include "Queue.h"

int furthestReachable(Graph g, int src) {
	int numVertices = GraphNumVertices(g);
	int *visited = calloc(numVertices, sizeof(int));
	int *distFromSrc = calloc(numVertices, sizeof(int));
	for (int i = 0; i < numVertices; i++) {
		distFromSrc[i] = -1;
	}
	Queue q = QueueNew();
	QueueEnqueue(q, src);
	visited[src] = true;
	distFromSrc[src] = 0;
	while (!QueueIsEmpty(q)) {
		int curr = QueueDequeue(q);
		for (int v = 0; v < numVertices; v++) {
			if (GraphIsAdjacent(g, curr, v) && !visited[v]) {
				QueueEnqueue(q, v);
				visited[v] = true;
				distFromSrc[v] = distFromSrc[curr]+1;
			}
		}
	}
	int furthest = src;
	int biggestDist = 0;
	for (int i = 0; i < numVertices; i++) {
		if (distFromSrc[i] >= biggestDist) {
			biggestDist = distFromSrc[i];
			furthest = i;
		}
	}
	free(visited);
	free(distFromSrc);
	QueueFree(q);
	return furthest;
}

