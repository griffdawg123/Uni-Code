#include <stdio.h>
#include <stdlib.h>

#include "Graph.h"
#include "Queue.h"

void breadthFirstSearch(Graph g, int src) {
	Queue q = QueueNew();
	QueueEnqueue(q, src);
	int numVertices = GraphNumVertices(g);
	int *visited = calloc(numVertices, sizeof(int));
	visited[src] = 1;
	while (!QueueIsEmpty(q)) {
		int curr = QueueDequeue(q);
		printf("%d ", curr);
		for (int v = 0; v < numVertices; v++) {
			if (GraphIsAdjacent(g, curr, v) && (visited[v] == 0)) {
				QueueEnqueue(q, v);
				visited[v] = 1;
			}
		}
	}
	QueueFree(q);
	free(visited);
}

