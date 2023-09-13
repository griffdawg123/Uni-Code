
#include <stdio.h>
#include <stdlib.h>

#include "Graph.h"
#include "Queue.h"

int shortestDistance(Graph g, int src, int dest) {
	int numVertices = GraphNumVertices(g);
	Queue q = QueueNew();
	int *predecessorArray = calloc(numVertices, sizeof(int));
	for (int i = 0; i < numVertices; i++) {
		predecessorArray[i] = -1;
	}
	int *visited = calloc(numVertices, sizeof(int));
	QueueEnqueue(q, src);
	visited[src] = true;
	while (!QueueIsEmpty(q)) {
		int curr = QueueDequeue(q);
		for (int v = 0; v < numVertices; v++) {
			if (GraphIsAdjacent(g, curr, v) && !visited[v]) {
				QueueEnqueue(q, v);
				visited[v] = true;
				predecessorArray[v] = curr;
			}
		}
	}
	int dist = 0;
	int curr = dest;
	while (curr != src && curr != -1) {
		curr = predecessorArray[curr];
		dist++;
	}
	if (curr == -1) {
		dist = -1;
	}
	QueueFree(q);
	free(predecessorArray);
	free(visited);
	return dist;
}

