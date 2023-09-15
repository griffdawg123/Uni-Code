// Assignment 1 20T1 COMP1511: Minesweeper
// minesweeper.c
//
// This program was written by Griffin Doyle (z5311098)
// on March, 2020
//
// Version 1.0.0 (2020-03-08): Assignment released.
// Version 1.0.1 (2020-03-08): Fix punctuation in comment.
// Version 1.0.2 (2020-03-08): Fix second line of header comment to say minesweeper.c

#include <stdio.h>
#include <stdlib.h>

// Possible square states.
#define VISIBLE_SAFE    0
#define HIDDEN_SAFE     1
#define HIDDEN_MINE     2

// The size of the starting grid.
#define SIZE 8

// Command codes.
#define NO_INPUT                0
#define DETECT_ROW              1
#define DETECT_COL              2
#define DETECT_SQUARE           3
#define REVEAL_SQUARE           4
#define GAMEPLAY_MODE           5
#define DEBUG_MODE              6
#define REVEAL_RADIAL           7

// Function initilalisation
void initialise_field(int minefield[SIZE][SIZE]);
void startup(int *numMines, int minefield[SIZE][SIZE]);
void setMines(int numMines, int minefield[SIZE][SIZE]);
void gameLoop(int minefield[SIZE][SIZE]);
void print_debug_minefield(int minefield[SIZE][SIZE]);
void checkRow(int rowNum, int minefield[SIZE][SIZE]);
void checkCol(int colNum, int minefield[SIZE][SIZE]);
int checkSquare(int row, int col, int size, int minefield[SIZE][SIZE]);
int revealSquare(int row, int col, int minefield[SIZE][SIZE]);
int checkWin(int minefield[SIZE][SIZE]);
void print_gameplay_minefield(int gameOver, int minefield[SIZE][SIZE]);
int revealRadial(int row, int col, int minefield[SIZE][SIZE]);
void shiftGrid(int row, int col, int minefield[SIZE][SIZE]);
int withinBounds(int rowCol);
void printElements(int row, int col, int gameOver, int minefield[SIZE][SIZE]);
void radialArm(int row, int col, int i, int j, int minefield[SIZE][SIZE]);
void changeCoord(int row, int col, int new[SIZE][SIZE], int minefield[SIZE][SIZE]);

int main(void) {
    // variable initialisation
    int minefield[SIZE][SIZE];
    int numMines;
    // Game Startup
    startup(&numMines, minefield);
    // Scan in the number of pairs of mines.
    setMines(numMines, minefield);
    // Main game loop
    gameLoop(minefield);
    return 0;
}

// Set the entire minefield to HIDDEN_SAFE.
void initialise_field(int minefield[SIZE][SIZE]) {
    int i = 0;
    while (i < SIZE) {
        int j = 0;
        while (j < SIZE) {
            minefield[i][j] = HIDDEN_SAFE;
            j++;
        }
        i++;
    }
}

// Intialises game
void startup(int *numMines, int minefield[SIZE][SIZE]) {
    initialise_field(minefield);
    printf("Welcome to minesweeper!\n");
    printf("How many mines? ");
    scanf("%d", numMines);
}

// Places mines into minefield
void setMines(int numMines, int minefield[SIZE][SIZE]) {
    printf("Enter pairs:\n");
    int i = 0;
    int row, col;
    //loops to get information about all mine locations
    while (i < numMines) {
        scanf("%d %d", &row, &col);
        // checks for valid input
        if (withinBounds(row) && withinBounds(col)) { 
            minefield[row][col] = HIDDEN_MINE;
            
        }
        i++;
    }
}

void gameLoop(int minefield[SIZE][SIZE]) {

    //variable initialisation
    int gameOver = 0;
    int command[4] = {0};
    int numHints = 0;
    int gameplay = 0;
    int firstTurn = 1;
    
    printf("Game Started\n");
    print_debug_minefield(minefield);
    
    // checks if command is input and the game is still running
    while (scanf("%d", &command[0]) && !gameOver) {
    
        if (command[0] == DETECT_ROW) {
            scanf(" %d", &command[1]);
            //check that user has used less than 3 hints
            if (numHints < 3) {
                checkRow(command[1], minefield);
                numHints++;
            } else {
                printf("Help already used\n");
            }                
        } else if (command[0] == DETECT_COL) {
            scanf(" %d", &command[1]);
            if (numHints < 3) {
                checkCol(command[1], minefield);
                numHints++;
            } else {
                printf("Help already used\n");
            }
        } else if (command[0] == DETECT_SQUARE) {
            scanf(" %d %d %d", &command[1], &command[2], &command[3]);
            if (numHints < 3) {
                printf(
"There are %d mine(s) in the square centered at row %d, column %d of size %d\n", 
                checkSquare(command[1], command[2], command[3], minefield), 
                command[1], 
                command[2], 
                command[3]);
                numHints++;
            } else {
                printf("Help already used\n");
            }    
        }
        if (command[0] == REVEAL_SQUARE) {
            scanf(" %d", &command[1]);
            scanf(" %d", &command[2]);
            // if first turn, shift grid until input is viable
            if (firstTurn) {
                shiftGrid(command[1], command[2], minefield);
                firstTurn = 0;
            }
            gameOver = revealSquare(command[1], command[2], minefield);
            
        } else if (command[0] == REVEAL_RADIAL) {
            scanf(" %d", &command[1]);
            scanf(" %d", &command[2]);
            if (firstTurn) {
                shiftGrid(command[1], command[2], minefield);
                firstTurn = 0;  
            }
            gameOver = revealRadial(command[1], command[2], minefield);
        } else if (command[0] == GAMEPLAY_MODE) {
            gameplay = 1;
            printf("Gameplay mode activated\n");
        } else if (command[0] == DEBUG_MODE)  {
            gameplay = 0;
            printf("Debug mode activated\n");
        }  else if (command[0] == NO_INPUT) {
            gameOver = 1;
        } 
        if (checkWin(minefield)) {
            printf("Game Won!\n");
            gameOver = 1;
        }
        // if game is still going, print the minefield
        if (command[0]) {
            if (gameplay) {
                print_gameplay_minefield(gameOver, minefield);
            } else {
                print_debug_minefield(minefield);
            }
        }
        // reset inputs
        int i = 0;
        while (i < 4) {
            command[i] = 0;
            i++;
        }
    }
}

// Print out the actual values of the minefield.
void print_debug_minefield(int minefield[SIZE][SIZE]) {
    int i = 0;
    while (i < SIZE) {
        int j = 0;
        while (j < SIZE) {
            printf("%d ", minefield[i][j]);
            j++;
        }
        printf("\n");
        i++;
    }
}

// prints number of mines in a row
void checkRow(int rowNum, int minefield[SIZE][SIZE]) {
    int i = 0;
    int mineCount = 0;
    // increments mineCount if there is a hidden mine
    while (i < SIZE) {
        if (minefield[rowNum][i] == HIDDEN_MINE) {
            mineCount++;
        }
        i++;
    }
    printf("There are %d mine(s) in row %d\n", mineCount, rowNum);
}

// prints number of mines in a column
void checkCol(int colNum, int minefield[SIZE][SIZE]) {
    int i = 0;
    int mineCount = 0;
    // increments mineCount if there is a hidden mine
    while (i < SIZE) {
        if (minefield[i][colNum] == HIDDEN_MINE) {
            mineCount++;
        }
        i++;
    }
    printf("There are %d mine(s) in column %d\n", mineCount, colNum);
}

// checks for hidden mines in a square centered at (row, col) of size size
int checkSquare(int row, int col, int size, int minefield[SIZE][SIZE]) {
    int i = 0;
    int mineCount = 0;
    // (row-offset, col-offset) is the coordinates of the top left square
    int offset = (size-1)/2;
    //iterating through rows
    while (i < size) {
        //check if the row is within the minefield size
        int currRow = row - offset + i;
        int j = 0;
        //iterates to cols
        while (j < size) {
            //check if col is within the minefield size
            int currCol = col - offset + j;
            if (withinBounds(currCol) && withinBounds(currRow)) {
                if (minefield[currRow][currCol] == HIDDEN_MINE) {mineCount++;}
            }
            j++;
        }             
        i++;
    }
    return mineCount;
}

//reveals given square if there is an adjacent mine, otherwise reveal 3*3 square
int revealSquare(int row, int col, int minefield[SIZE][SIZE]) {
    // if player attempts to reveal a mine, game over
    if (minefield[row][col] == HIDDEN_MINE) {
        printf("Game Over\n");
        return 1;
    }
    // if mine surrounds chose square, only reveal that square
    if (checkSquare(row, col, 3, minefield)) {
        minefield[row][col] = VISIBLE_SAFE;
        return 0;
    }
    // iterates through square and reveals each location
    int i = 0;
    while (i < 3) {
        int currRow = row - 1 + i;
        int j = 0;
        while (j < 3) {
            int currCol = col - 1 + j;
            if (withinBounds(currCol) && withinBounds(currRow)) {
                minefield[currRow][currCol] = VISIBLE_SAFE;
            }
            j++;
        }
        i++;
    }
    return 0;
}

// if there are any hidden safe squares still on the board, no win
int checkWin(int minefield[SIZE][SIZE]){
    int i = 0;
    while (i < SIZE) {
        int j = 0;
        while (j < SIZE) {
            if (minefield[i][j] == HIDDEN_SAFE) {
                return 0;
            }
            j++;
        }
        i++;
    }
    return 1;
}

// prints formatted gamefield
void print_gameplay_minefield(int gameOver, int minefield[SIZE][SIZE]) {
    //prints face depending if game is won or not
    if (!gameOver || checkWin(minefield)) {
        printf("..\n\\/\n");
    } else {
        printf("XX\n/\\\n");
    }
    printf("    ");
    int i = 0;
    // column numbers 
    while (i < SIZE) {
        printf("0%d ", i);
        i++;
    }
    printf("\n");
    printf("   -------------------------\n");
    i = 0;
    while (i < SIZE) {
        int j = 0;
        printf("0%d |", i);
        while (j < SIZE) {
            printElements(i, j, gameOver, minefield);
            j++;
        }
        printf("|\n");
        i++;
    }
    printf("   -------------------------\n");
}

void printElements(int row, int col, int gameOver, int minefield[SIZE][SIZE]) {
    if (minefield[row][col] == HIDDEN_MINE || 
        minefield[row][col] == HIDDEN_SAFE) { //checking if hidden
        if (minefield[row][col] == HIDDEN_MINE && 
        gameOver == 1 && 
        !checkWin(minefield)) { //checking if game is over
            printf("()");
        } else {
            printf("##");
        }
    } else { //safe
        if (checkSquare(row, col, 3, minefield) == 0) { //checking if surrounding mines
            printf("  ");
        } else {
            printf("0%d", checkSquare(row, col, 3, minefield));
        }
    }
    // if on the last column, dont print a space 
    if (col < SIZE-1) {
        printf(" ");
    }
}

// reveals mines in lines from the centre until a mine is detected
int revealRadial(int row, int col, int minefield[SIZE][SIZE]) {
    // if attepting to reveal a mine, game over
    if (minefield[row][col] == HIDDEN_MINE) {
        printf("Game Over\n");
        return 1;
    } 
    // if there is a mine surrounding selected square, only reveal that square
    if (checkSquare(row, col, 3, minefield)) {
        minefield[row][col] = VISIBLE_SAFE;
        return 0;
    }
    minefield[row][col] = VISIBLE_SAFE;
    int i = 0;
    while (i < 3) {
        int j = 0;
        int boxRow = row-1+i; // box row is which row the radial arm starts from
        while (j < 3) {
            int boxCol = col-1+j; // box col is which col the radial arm starts
            if (!((i == 1) && (j == 1))) {
                radialArm(boxRow, boxCol, i, j, minefield);
            }
            j++;
        }
        i++;
    }
    return 0;
}

//loops through moving away from box close to centre 
void radialArm(int row, int col, int relRow, int relCol, int minefield[SIZE][SIZE]) {
    int extNo = 0; // how far from centre
    int rowExt = 0; // row of current box
    int colExt = 0; // col of current box 
    while (withinBounds(row + rowExt) && 
    withinBounds(col + colExt)) {
        if (minefield[row + rowExt][col + colExt] == HIDDEN_SAFE) {
            minefield[row + rowExt][col + colExt] = VISIBLE_SAFE;
        } else {
            extNo = SIZE;
        }                
        if (checkSquare(row + rowExt, col + colExt, 3, minefield)) {
            extNo = SIZE;
        } else {
            extNo++;
        }
        rowExt = (relRow-1) * extNo;
        colExt = (relCol-1) * extNo;
    }
}

// while entered coordinate has a mine, shift all coordinates down one
void shiftGrid(int row, int col, int minefield[SIZE][SIZE]) {
    while (minefield[row][col] == HIDDEN_MINE) {
        int i = 0;
        int new[SIZE][SIZE] = {0};
        while (i < SIZE) { 
            int j = 0;
            while (j < SIZE) {
                changeCoord(i, j, new, minefield);
                j++;
            }
            i++;
        }
        i = 0;
        while (i < SIZE) {
            int j = 0;
            while (j < SIZE) {
                minefield[i][j] = new[i][j];
                j++;
            }
            i++;
        }
    }
}

// inserts minefield coords into new coords
void changeCoord(int row, int col, int new[SIZE][SIZE], int minefield[SIZE][SIZE]) {
    if (row == SIZE - 1) {
        new[0][col] = minefield[row][col];
    } else {
        new[row+1][col] = minefield[row][col];
    }
}

// tests whether or not row or column is within the minefield's range
int withinBounds(int rowCol) {
    return (rowCol >= 0 && rowCol < SIZE);
}
