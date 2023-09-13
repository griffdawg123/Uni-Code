// DFS maze solver

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "Cell.h"
#include "helpers.h"
#include "Maze.h"
#include "Stack.h"

bool insideBounds(int row, int col, Maze m) {
    return ((row >= 0) && (col >= 0) && (row < MazeHeight(m)) && (col < MazeWidth(m)));
}

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

    Stack s = StackNew();
    StackPush(s, MazeGetStart(m));

    Cell** adjacencyMatrix = createCellMatrix(MazeHeight(m), MazeWidth(m));  
    bool** visitedMatrix = createBoolMatrix(MazeHeight(m), MazeWidth(m));
    Cell curr;

    while (!StackIsEmpty(s)) {
        curr = StackPop(s);
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
                StackPush(s, *cell);
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
                StackPush(s, *cell);
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
                StackPush(s, *cell);
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
                StackPush(s, *cell);
                adjacencyMatrix[cell->row][cell->col] = curr;
            } else {
                free(cell);
            }
        }
    }

    StackFree(s);
    freeCellMatrix(adjacencyMatrix);
    freeBoolMatrix(visitedMatrix);

    return pathFound;
}

