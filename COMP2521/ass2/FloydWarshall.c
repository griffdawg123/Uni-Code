// Floyd Warshall ADT interface
// COMP2521 Assignment 2

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "FloydWarshall.h"
#include "Graph.h"

// creates a nxn int matrix where n is the number of nodes
static int **vertexMatrix(int numNodes);
// initialises a vertex matrix with the distances of edges in a graph g
// distMatrix[i][j] = INFINITY -> for non existing edge(i, j)
// distMatrix[i][j] = 0 -> when i == j
// distMatrix[i][j] = weight(i, j)  -> otherwise
static void initialiseDistMatrix(Graph g, int numNodes, int **vertexMatrix);
// initialises a vertex matrix containing the information regarding the next vertex in the path from i->j
// next[i][j] = j -> if edge(i, j) exists or i==j
// next[i][j] = -1 -> if there is no edge(i, j)
static void initialiseNextMatrix(Graph g, int numNodes, int **vertexMatrix);
// frees a vertex matrix and its components
static void freeVertexMatrix(int numNodes, int **vertexMatrix);
// returns the weight of the edge to dest in the Adjlist outlinks of a particular src
static int AdjListWeight(AdjList outlinks, Vertex dest);
// true if edge(src, intermediate) and edge(intermediate, dest) exists, else false
static bool intermediatePathExists(Vertex src, Vertex intermediate, Vertex dest, int **distMatrix);
/**	
 * Finds all shortest paths between all pairs of nodes.
 * 
 * The  function  returns  a 'ShortestPaths' structure with the required
 * information:
 * - the number of vertices in the graph
 * - distance matrix
 * - matrix of intermediates (see description above)
 */
// Source: https://en.wikipedia.org/wiki/Floyd–Warshall_algorithm
ShortestPaths FloydWarshall(Graph g) {
	int numVertices = GraphNumVertices(g);
	int **distances = vertexMatrix(GraphNumVertices(g));
	initialiseDistMatrix(g, numVertices, distances);
	int **next = vertexMatrix(GraphNumVertices(g));
	initialiseNextMatrix(g, numVertices, next);
	for (int intermediate = 0; intermediate < numVertices; intermediate++) {
		for (int src = 0; src < numVertices; src++) {
			for (int dest = 0; dest < numVertices; dest++) {
				// ensures that neither of the intermediate paths are INFINITY
				if (intermediatePathExists(src, intermediate, dest, distances)) {
					// if the path through the intermediate is shorter than the current,
					// update the matrices to reflect the new shortest path
					if (distances[src][intermediate] + distances[intermediate][dest] < distances[src][dest]) {
						distances[src][dest] = distances[src][intermediate] + distances[intermediate][dest];
						next[src][dest] = next[src][intermediate];
					} 
				}
			}
		}
	}
	ShortestPaths sps = {numVertices, distances, next};
	// sps->numNodes = numVertices;
	// printf("im okay\n");
	// sps->dist = distances;
	// sps->next = next;
	return sps;
}

/**
 * This  function  is  for  you to print out the ShortestPaths structure
 * while you are debugging/testing your implementation. 
 * 
 * We will not call this function during testing, so you may  print  out
 * the  given  ShortestPaths  structure in whatever format you want. You
 * may choose not to implement this function.
 */
void showShortestPaths(ShortestPaths sps) {
	printf("Printing Graph with %d Nodes:\n", sps.numNodes);
	printf("Distance array:\n");
	for (int i = 0; i < sps.numNodes; i++) {
		for (int j = 0; j < sps.numNodes; j++) {
			if (sps.dist[i][j] == INFINITY) {
				printf("INF\t");
			} else {
				printf("%d\t", sps.dist[i][j]);
			}
		}
		printf("\n");
	}
	printf("Next array:\n");
	for (int i = 0; i < sps.numNodes; i++) {
		for (int j = 0; j < sps.numNodes; j++) {
			if (sps.next[i][j] == -1) {
				if (i == j) {
					printf("-\t");
				} else {
					printf("NA\t");
				}
			} else {
				printf("%d\t", sps.next[i][j]);
			}
		}
		printf("\n");
	}
}

/**
 * Frees  all  memory associated with the given ShortestPaths structure.
 * We will call this function during testing, so you must implement it.
 */
void freeShortestPaths(ShortestPaths sps) {
	int n = sps.numNodes;
	freeVertexMatrix(n, sps.next);
	freeVertexMatrix(n, sps.dist);
}

// creates a nxn int matrix where n is the number of nodes
static int **vertexMatrix(int numNodes) {
	int **distances = (int **)malloc(numNodes*sizeof(int *));
	for (int i = 0; i < numNodes; i++) {
		distances[i] = (int *)malloc(numNodes*sizeof(int));
	}
	return distances;
}

// initialises a vertex matrix with the distances of edges in a graph g
// distMatrix[i][j] = INFINITY -> for non existing edge(i, j)
// distMatrix[i][j] = 0 -> when i == j
// distMatrix[i][j] = weight(i, j)  -> otherwise
static void initialiseDistMatrix(Graph g, int numNodes, int **vertexMatrix)
 {
	for (int src = 0; src < numNodes; src++) {
		AdjList outlinks = GraphOutIncident(g, src);
		for (int dest = 0; dest < numNodes; dest++) {
			if (GraphIsAdjacent(g, src, dest)) {
				vertexMatrix[src][dest] = AdjListWeight(outlinks, dest);
			} else if (dest == src) {
				vertexMatrix[src][dest] = 0;
			} else {
				vertexMatrix[src][dest] = INFINITY;
			}
		}
	}
}

// initialises a vertex matrix containing the information regarding the next vertex in the path from i->j
// next[i][j] = j -> if edge(i, j) exists or i==j
// next[i][j] = -1 -> if there is no edge(i, j)
static void initialiseNextMatrix(Graph g, int numNodes, int **vertexMatrix) {
	for (int src = 0; src < numNodes; src++) {
		for (int dest = 0; dest < numNodes; dest++) {
			if (GraphIsAdjacent(g, src, dest)) {
				vertexMatrix[src][dest] = dest;
			}  else {
				vertexMatrix[src][dest] = -1;	
			}
		}
	}
}

// frees a vertex matrix and its components
static void freeVertexMatrix(int numNodes, int **vertexMatrix) {
	for (int i = 0; i < numNodes; i++) {
		free(vertexMatrix[i]);
	}
	free(vertexMatrix);
}

// returns the weight of the edge to dest in the Adjlist outlinks of a particular src
static int AdjListWeight(AdjList outlinks, Vertex dest) {
	while (outlinks->v != dest) {
		outlinks = outlinks->next;
	}
	return outlinks->weight;
}

// true if edge(src, intermediate) and edge(intermediate, dest) exists, else false
static bool intermediatePathExists(Vertex src, Vertex intermediate, Vertex dest, int **distMatrix) {
	return (distMatrix[src][intermediate] != INFINITY) && (distMatrix[intermediate][dest] != INFINITY);
}
