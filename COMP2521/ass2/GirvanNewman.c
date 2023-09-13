// Girvan-Newman Algorithm for community discovery
// COMP2521 Assignment 2

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "CentralityMeasures.h"
#include "GirvanNewman.h"
#include "Graph.h"

// does dfs on a graph to find all nodes within a specific collection
static void dfsComponent(Graph g, Vertex v, int collectionID, int *componentOf);
// returns the dendrogram that clusters communities of nodes together
static Dendrogram doGirvanNewman(Graph g, int collectionID, int *componentOf);
// returns the number of connected components in a community
static int numConnectedComponents(int numVertices, int collectionID, int *componentOf);
// returns a new leaf node with the given vertex number
static Dendrogram newLeaf(Vertex v);
// returns the highest betweenness value of the graph
static int highestBetweenness(int numVertices, double **values, int collectionID, int *componentOf);
// removes the highest betweenness edge
static void removeHighestBetweennessEdge(Graph g, double highest, int collectionID, int *componentOf, double **betweenness);
// finds the communities within a graph
static int *findCommunities(Graph g, int collectionID, int *componentOf);
// checks if a new community has been created
static bool isNewComponentCreated(int numVertices, int *connectedness);
/**
 * Generates  a Dendrogram for the given graph g using the Girvan-Newman
 * algorithm.
 * 
 * The function returns a 'Dendrogram' structure.
 */
Dendrogram GirvanNewman(Graph g) {
	int numVertices = GraphNumVertices(g);
	// all of the graph is connected
	int *componentOf = calloc(numVertices, sizeof(int));
	for (Vertex v = 0; v < numVertices; v++) {
		componentOf[v] = -1;
	}
	Dendrogram new = doGirvanNewman(g, -1, componentOf);
	free(componentOf);
	return new;
}

/**
 * Frees all memory associated with the given Dendrogram  structure.  We
 * will call this function during testing, so you must implement it.
 */
void freeDendrogram(Dendrogram d) {
	if (d == NULL) {
		return;
	}
	freeDendrogram(d->left);
	freeDendrogram(d->right);
	free(d);
}

// returns the dendrogram that clusters communities of nodes together
static Dendrogram doGirvanNewman(Graph g, int collectionID, int *componentOf) {
	int numVertices = GraphNumVertices(g);
	// calculate the number of connected vertices
	int numConnected = numConnectedComponents(numVertices, collectionID, componentOf);
	// if only one vertex return a leaf with the value
	if (numConnected == 1) {
		for (Vertex v = 0; v < numVertices; v++) {
			if (componentOf[v] == collectionID) {
				return newLeaf(v);
			}
		}
	} 
	EdgeValues evs = edgeBetweennessCentrality(g);
	double **betweenness = evs.values;
	double highest = highestBetweenness(numVertices, betweenness, collectionID, componentOf);
	// remove the edges with the highest betweenness and in the correct collection
	removeHighestBetweennessEdge(g, highest, collectionID, componentOf, betweenness);
	freeEdgeValues(evs);
	int *connectedness = findCommunities(g, collectionID, componentOf);
	bool newComponentCreated = isNewComponentCreated(numVertices, connectedness);
	if (newComponentCreated == true) {
		DNode *newNode = malloc(sizeof(*newNode));
		newNode->left = doGirvanNewman(g, 0, connectedness);
		newNode->right = doGirvanNewman(g, 1, connectedness);
		free(connectedness);
		return newNode;
	} else {
		Dendrogram new = doGirvanNewman(g, 0, connectedness);
		free(connectedness);
		return new;
	}
}

// returns the number of connected components in a community
static int numConnectedComponents(int numVertices, int collectionID, int *componentOf) {
	int numConnected = 0;
	for (Vertex v = 0; v < numVertices; v++) {
		if (componentOf[v] == collectionID) {
			numConnected++;
		}
	}
	return numConnected;
}

// returns a new leaf node with the given vertex number
static Dendrogram newLeaf(Vertex v) {
	Dendrogram leaf = malloc(sizeof(*leaf));
	leaf->left = NULL;
	leaf->right = NULL;
	leaf->vertex = v;
	return leaf;
}

// returns the highest betweenness value of the graph
static int highestBetweenness(int numVertices, double **values, int collectionID, int *componentOf) {
	//calculate the edge betweenness of the current graph
	double heighestBetweenness = 0;
	// find highest betweenness of the current graph and remove if its part of the current cluster
	for (Vertex src = 0; src < numVertices; src++) {
		for (Vertex dest = 0; dest < numVertices; dest++) {
			if ((values[src][dest] > heighestBetweenness) && (componentOf[src] == collectionID) && (componentOf[dest] == collectionID)) {
				heighestBetweenness = values[src][dest];
			}
		}
	}
	return heighestBetweenness;
}

// removes the highest betweenness edge
static void removeHighestBetweennessEdge(Graph g, double highest, int collectionID, int *componentOf, double **betweenness) {
	int numVertices = GraphNumVertices(g);
	for (Vertex src = 0; src < numVertices; src++) {
		for (Vertex dest = 0; dest < numVertices; dest++) {
			if ((betweenness[src][dest] == highest) && (componentOf[src] == collectionID) && (componentOf[dest] == collectionID)) {
				GraphRemoveEdge(g, src, dest);
			}
		}
	}
}

// finds the communities within a graph
// https://edstem.org/courses/5409/discussion/440119
static int *findCommunities(Graph g, int collectionID, int *componentOf) {
	int numVertices = GraphNumVertices(g);
	int *connectedness = calloc(numVertices, sizeof(int));
	// check the connectedness of the graph
	for (Vertex v = 0; v < numVertices; v++) {
		connectedness[v] = -1;
	}
	int curr = 0;
	// only consider the vertecies of the current collection
	for (Vertex v = 0; v < numVertices; v++) {
		if ((connectedness[v] == -1) && (componentOf[v] == collectionID)) {
			dfsComponent(g, v, curr, connectedness);
			curr++;
		}
	}
	return connectedness;
}

// does dfs on a graph to find all nodes within a specific collection
static void dfsComponent(Graph g, Vertex v, int collectionID, int *componentOf) {
	int numVertices = GraphNumVertices(g);
	componentOf[v] = collectionID;
	for (Vertex dest = 0; dest < numVertices; dest++) {
		// if there is an edge from src-dest and the destination has not been set
		if ((GraphIsAdjacent(g, v, dest) || GraphIsAdjacent(g, dest, v)) && (componentOf[dest] == -1)) {
			dfsComponent(g, dest, collectionID, componentOf);
		}
	}
}

// checks if a new community has been created
static bool isNewComponentCreated(int numVertices, int *connectedness) {
	for (Vertex v = 0; v < numVertices; v++) {
		if (connectedness[v] == 1) {
			return true;
		}
	}
	return false;
}