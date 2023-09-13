// calculateViralTransmission.c ... implementation of
// calculateViralTransmission function

#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "Graph.h"
#include "Queue.h"

/*
    You will submit only this one file.

    Implement the function "calculateViralTransmission" below.
    Read the exam paper for a detailed specification and
    description of your task.

    - DO NOT modify the code in any other files except for debugging
      purposes.
    - If you wish, you can add static variables and/or helper functions
      to this file.
    - DO NOT add a "main" function to this file.
*/

void calculateViralTransmission(Graph g, int src, int srcViralLoad,
                                double *trasmissionArray) {
  // initialise important variables
	int numVertices = GraphNumVertices(g);
  int *visited = calloc(numVertices, sizeof(int));
  int *distArray = calloc(numVertices, sizeof(int));
  for (int i = 0; i < numVertices; i++) {
    distArray[i] = -1;
  }
  Queue q = QueueNew();
  // initialise src for BFS
  QueueEnqueue(q, src);
  visited[src] = true;
  distArray[src] = 0;
  trasmissionArray[src] = srcViralLoad;
  while (!QueueIsEmpty(q)) {
    int curr = QueueDequeue(q);
    // loop through all of the vertices
    for (int v = 0; v < numVertices; v++) {
      // if we've found a vertex we haven't seen yet which is reachable
      if (GraphIsAdjacent(g, curr, v) && !visited[v]) {
        QueueEnqueue(q, v);
        visited[v] = true;
        //calculate distances
        int dist = distArray[curr]+1;
        distArray[v] = dist;
        // set viral load transmission
        double virus = srcViralLoad * pow(0.6, dist);
        trasmissionArray[v] = (virus < 10) ? 0 : virus;
      }
    }
  }
  // free memory
  free(visited);
  free(distArray);
  QueueFree(q);
}

