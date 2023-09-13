// BFS maze solver

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "Cell.h"
#include "helpers.h"
#include "Maze.h"
#include "Queue.h"

bool insideBounds(int row, int col, Maze m) {
    return ((row >= 0) && (col >= 0) && (row < MazeHeight(m)) && (col < MazeWidth(m)));
}

// worst case: O(n), assuming MazeMarkPath is O(1)
void markPath(Maze m, Cell* exit, Cell** predecessors) {
    MazeMarkPath(m, *exit);
    Cell curr = predecessors[exit->row][exit->col];
    while (curr.row != 0 && curr.col != 0) {
        MazeMarkPath(m, curr);
        curr = predecessors[curr.row][curr.col];
    }
    MazeMarkPath(m, curr);
}

bool solve(Maze m) {

   bool pathFound = false;

    Queue q = QueueNew();
    QueueEnqueue(q, MazeGetStart(m));

    //O(n^2) each
    Cell** adjacencyMatrix = createCellMatrix(MazeHeight(m), MazeWidth(m));  
    bool** visitedMatrix = createBoolMatrix(MazeHeight(m), MazeWidth(m));
    Cell curr;


    while (!QueueIsEmpty(q)) {
        curr = QueueDequeue(q);
        int currX = curr.col;
        int currY = curr.row;
        if(MazeVisit(m, curr)) {
            pathFound = true;
            markPath(m, &curr, adjacencyMatrix);
            break;
        }
        visitedMatrix[currY][currX] = true;

        if (insideBounds(currY, currX+1, m) && !(visitedMatrix[currY][currX+1])) {
            Item* cell = malloc(sizeof(*cell));
            cell->row = currY;
            cell->col = currX+1;
            if (!MazeIsWall(m, *cell)) {
                QueueEnqueue(q, *cell);
                adjacencyMatrix[cell->row][cell->col] = curr;
            } else {
                free(cell);
            } 
        }
        if (insideBounds(currY+1, currX, m) && !(visitedMatrix[currY+1][currX])) {
            Item* cell = malloc(sizeof(*cell));
            cell->row = currY+1;
            cell->col = currX;
            if (!MazeIsWall(m, *cell)) {
                QueueEnqueue(q, *cell);
                adjacencyMatrix[cell->row][cell->col] = curr;
            } else {
                free(cell);
            }
        }
        if (insideBounds(currY, currX-1, m) && !(visitedMatrix[currY][currX-1])) {
            Item* cell = malloc(sizeof(*cell));
            cell->row = currY;
            cell->col = currX-1;
            if (!MazeIsWall(m, *cell)) {
                QueueEnqueue(q, *cell);
                adjacencyMatrix[cell->row][cell->col] = curr;
            } else {
                free(cell);
            }
        }
        if (insideBounds(currY-1, currX, m) && !(visitedMatrix[currY-1][currX])) {
            Item* cell = malloc(sizeof(*cell));
            cell->row = currY-1;
            cell->col = currX;
            if (!MazeIsWall(m, *cell)) {
                QueueEnqueue(q, *cell);
                adjacencyMatrix[cell->row][cell->col] = curr;
            } else {
                free(cell);
            }
        }
    }

    QueueFree(q);
    freeCellMatrix(adjacencyMatrix);
    freeBoolMatrix(visitedMatrix);

    return pathFound;
}