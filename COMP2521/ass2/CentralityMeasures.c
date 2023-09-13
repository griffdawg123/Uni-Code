// Centrality Measures ADT interface
// COMP2521 Assignment 2

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "CentralityMeasures.h"
#include "FloydWarshall.h"
#include "Graph.h"

// creates a nxn double matrix where n is the number of nodes
static double **vertexMatrix(int numNodes);
// initialises a centrality matrix which contains the information about the centrality of edges in a graph
// centralityMatrix[i][j] = 0 -> when edge(i,j) exists and is part of a shortest path
// centralityMatrix[i][j] = -1 -> otherwise
static double **initialiseCentralityMatrix(Graph G, double **vertexMatrix, int **nextMatrix);

/**
 * Finds  the  edge  betweenness  centrality  for each edge in the given
 * graph and returns the results in a  EdgeValues  structure.  The  edge
 * betweenness centrality of a non-existant edge should be set to -1.0.
 */
// Inspiration from: https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.72.9610&rep=rep1&type=pdf
EdgeValues edgeBetweennessCentrality(Graph g) {
	int numNodes = GraphNumVertices(g);
	double **centrality = vertexMatrix(numNodes);
	ShortestPaths sps = FloydWarshall(g);
	centrality = initialiseCentralityMatrix(g, centrality, sps.next);
	int **next = sps.next;
	for (Vertex src = 0; src < numNodes; src++) {
		for (Vertex dest = 0; dest < numNodes; dest++) {
			Vertex curr = src;
			// walks along the path from src to dest 
			// adds 1 to each edge in the centralityMatrix
			while (curr != dest) {
				Vertex nextNode = next[curr][dest];
				if (nextNode == -1) {
					break;
				} 
				centrality[curr][nextNode] += 1;
				curr = nextNode;
			}
		}
	}
	freeShortestPaths(sps);
	EdgeValues e = {numNodes, centrality};
	// EdgeValues *e = malloc(sizeof(*e));
	// e->numNodes = numNodes;
	// e->values = centrality;
	// return *e;
	return e;
}

/**
 * Prints  the  values in the given EdgeValues structure to stdout. This
 * function is purely for debugging purposes and will NOT be marked.
 */
void showEdgeValues(EdgeValues evs) {
	printf("Now printing the Edge Centrality of a graph with %d nodes:\n", evs.numNodes);
	for (int i = 0; i < evs.numNodes; i++) {
		for (int j = 0; j < evs.numNodes; j++) {
			printf("Edge %d-%d occurs %f times\n", i, j, evs.values[i][j]);
		}
	}
}

/**
 * Frees all memory associated with the given EdgeValues  structure.  We
 * will call this function during testing, so you must implement it.
 */
void freeEdgeValues(EdgeValues evs) {
	for (int i = 0; i < evs.numNodes; i++) {
		free(evs.values[i]);
	}
	free(evs.values);
}

// creates a nxn double matrix where n is the number of nodes
static double **vertexMatrix(int numNodes) {
	double **distances = calloc(numNodes, sizeof(double *));
	for (int i = 0; i < numNodes; i++) {
		distances[i] = calloc(numNodes, sizeof(double));
	}
	return distances;
}

// initialises a centrality matrix which contains the information about the centrality of edges in a graph
// centralityMatrix[i][j] = 0 -> when edge(i,j) exists and is part of a shortest path
// centralityMatrix[i][j] = -1 -> otherwise
static double **initialiseCentralityMatrix(Graph g, double **vertexMatrix, int **nextMatrix) {
	int numNodes = GraphNumVertices(g);
	for (int src = 0; src < numNodes; src++) {
		for (int dest = 0; dest < numNodes; dest++) {
			if (nextMatrix[src][dest] != -1 && GraphIsAdjacent(g, src, dest)) {
				vertexMatrix[src][dest] = 0;
			} else {
				vertexMatrix[src][dest] = -1;
			}
		}
	}
	return vertexMatrix;
}