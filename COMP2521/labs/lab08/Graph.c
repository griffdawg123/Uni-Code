// Implementation of the undirected weighted graph ADT

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "Graph.h"
#include "Queue.h"

// graph representation (adjacency matrix)
typedef struct GraphRep {
	int nV;      // #vertices
	int nE;      // #edges
	int **edges; // matrix of weights (0 == no edge)
} GraphRep;

static int validVertex(Graph g, Vertex v);

////////////////////////////////////////////////////////////////////////

Graph GraphNew(int nV)
{
	assert(nV > 0);

	Graph new = malloc(sizeof(*new));
	assert(new != NULL);
	new->nV = nV;
	new->nE = 0;

	new->edges = calloc(nV, sizeof(int *));
	assert(new->edges != NULL);
	for (int v = 0; v < nV; v++) {
		new->edges[v] = calloc(nV, sizeof(int));
		assert(new->edges[v] != 0);
	}

	return new;
}

void GraphFree(Graph g)
{
	assert(g != NULL);
	for (int v = 0; v < g->nV; v++)
		free(g->edges[v]);
	free(g->edges);
	free(g);
}

////////////////////////////////////////////////////////////////////////

void GraphInsertEdge(Graph g, Vertex v, Vertex w, int weight)
{
	assert(g != NULL && validVertex(g, v) && validVertex(g, w));

	if (g->edges[v][w] != 0 && g->edges[w][v] != 0)
		return; // an edge already exists; do nothing.

	g->edges[v][w] = weight;
	g->edges[w][v] = weight;
	g->nE++;
}

void GraphRemoveEdge(Graph g, Vertex v, Vertex w)
{
	assert(g != NULL && validVertex(g, v) && validVertex(g, w));
	if (g->edges[v][w] == 0 && g->edges[w][v] == 0)
		return; // the edge doesn't exist; do nothing.

	g->edges[v][w] = 0;
	g->edges[w][v] = 0;
	g->nE--;
}

////////////////////////////////////////////////////////////////////////

/**
 * Finds  the  shortest path (in terms of the number of hops) from `src`
 * to `dest` such that no edge on the path has weight larger than `max`.
 * Stores  the  path  in the given `path` array including both `src` and
 * `dest` and returns the number of vertices stored in the  path  array.
 * Returns 0 if there is no such path.
 */
int findPath(Graph g, Vertex src, Vertex dest, int max, int *path)
{
	assert(g != NULL);
	// Queue holds nodes used for breadth first search
	Queue q = QueueNew();
	// Holds precursor for each node
	int *precursorArray = calloc(g->nV, sizeof(int));
	// holds information if a node is visited
	bool *visitedArray = calloc(g->nV, sizeof(bool));
	// enqueue the src
	QueueEnqueue(q, src);
	// add src to path in case src == dest
	path[0] = src;
	// src has been visited
	visitedArray[src] = 1;
	// if src == dest, no need to check neighbours
	bool foundDest = (src == dest);
	while (!QueueIsEmpty(q) && !foundDest) {
		// pop front of queue
		Vertex curr = QueueDequeue(q);
		for (int i = 0; i < g->nV; i++) {
			// go through each other node and if theres a link less than the max
			// and the node hasn't been visited, add it
			if ((g->edges[curr][i] < max) && (g->edges[curr][i]) && !visitedArray[i]) {
				QueueEnqueue(q, i);
				visitedArray[i] = 1;
				precursorArray[i] = curr;
				// break if we've found the dest
				if (i == dest) {
					foundDest = true;
					break;
				}
			}
		}
	}
	// if we get to the end of the queue and we haven't found the 
	// destination, there is no path
	if (QueueIsEmpty(q) && !foundDest) {
		return 0;
	}
	int counter = 0;
	// while we haven't added the destination
	while (path[counter] != dest) {
		
		// start at the destination
		int curr = dest;
		// while the precursor of the current node is not the one we just added
		// go to previous node
		while (precursorArray[curr] != path[counter]) {
			curr = precursorArray[curr];
		}
		counter++;
		// add current to path
		path[counter] = curr;
	}
	counter++;
	QueueFree(q);
	return counter;
}

////////////////////////////////////////////////////////////////////////

void GraphShow(Graph g, char **names)
{
	assert(g != NULL);
	printf("#vertices=%d, #edges=%d\n\n", g->nV, g->nE);
	int v, w;
	for (v = 0; v < g->nV; v++) {
		printf("%d %s\n", v, names[v]);
		for (w = 0; w < g->nV; w++) {
			if (g->edges[v][w]) {
				printf("\t%s (%d)\n", names[w], g->edges[v][w]);
			}
		}
		printf("\n");
	}
}

////////////////////////////////////////////////////////////////////////
// Helper Functions

static int validVertex(Graph g, Vertex v)
{
	return (g != NULL && v >= 0 && v < g->nV);
}

