
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "List.h"
#include "Record.h"
#include "AVLTree.h"

typedef struct node *Node;
struct node {
    Record rec;
    Node   left;
    Node   right;
    int    height;
};

struct tree {
    Node    root;
    int     (*compare)(Record, Record);
};

////////////////////////////////////////////////////////////////////////
// Auxiliary functions

static void doTreeFree(Node n, bool freeRecords);
static Node newNode(Record rec);
static Record doTreeSearch(Tree t, Node n, Record rec);

////////////////////////////////////////////////////////////////////////

static Node newNode(Record rec) {
    Node n = malloc(sizeof(*n));
    if (n == NULL) {
        fprintf(stderr, "error: out of memory\n");
        exit(EXIT_FAILURE);
    }

    n->left = NULL;
    n->right = NULL;
    n->rec = rec;
    return n;
}

////////////////////////////////////////////////////////////////////////

Tree TreeNew(int (*compare)(Record, Record)) {
    Tree t = malloc(sizeof(*t));
    if (t == NULL) {
        fprintf(stderr, "error: out of memory\n");
        exit(EXIT_FAILURE);
    }

    t->root = NULL;
    t->compare = compare;
    return t;
}

////////////////////////////////////////////////////////////////////////

void TreeFree(Tree t, bool freeRecords) {
    doTreeFree(t->root, freeRecords);
    free(t);
}

static void doTreeFree(Node n, bool freeRecords) {
    if (n != NULL) {
        doTreeFree(n->left, freeRecords);
        doTreeFree(n->right, freeRecords);
        if (freeRecords) {
            RecordFree(n->rec);
        }
        free(n);
    }
}

////////////////////////////////////////////////////////////////////////

Record TreeSearch(Tree t, Record rec) {
    return doTreeSearch(t, t->root, rec);
}

static Record doTreeSearch(Tree t, Node n, Record rec) {
    if (n == NULL) {
        return NULL;
    }

    int cmp = t->compare(rec, n->rec);
    if (cmp < 0) {
        return doTreeSearch(t, n->left, rec);
    } else if (cmp > 0) {
        return doTreeSearch(t, n->right, rec);
    } else {
        return n->rec;
    }
}


////////////////////////////////////////////////////////////////////////
/* IMPORTANT: 
   Do NOT modify the code above this line. 
   You must not modify the 'node' and 'tree' structures defined above.
   You must not modify the functions defined above.
*/
////////////////////////////////////////////////////////////////////////

/* Function Declarations */

// Used for insertion method
bool TreeInsert(Tree t, Record rec);
Node doTreeInsert(Tree t, Node n, Record rec, bool *inserted);
Node rotateRight(Node n);
Node rotateLeft(Node n);
int max(int a, int b);
int getHeight(Node n);

// Used for search between
List TreeSearchBetween(Tree t, Record lower, Record upper);
static void doTreeSearchBetween(Tree t, Node n, Record lower,
                                Record upper, List l);

// Used for TreeNext
Record TreeNext(Tree t, Record r);
Record doTreeNext(Tree t, Node n, Record r);

////////////////////////////////////////////////////////////////////////

// called to insert the record into the tree and balance it
// Input: 
//  t: tree struct we are inserting into
//  rec: record struct which is being inserted
// Output: 
//  bool: true if the record is inserted, else false
// Complexity: O(log n)
bool TreeInsert(Tree t, Record rec) {
    bool inserted = false;
    t->root = doTreeInsert(t, t->root, rec, &inserted);
    return inserted;
}

// helper function which is used to insert the record
// Input: 
//  t: tree we are inserting into
//  n: node which we are currently at in the tree
//  rec: record struct which is being inserted
//  *inserted: pointer to the inserted boolean
// Output: 
//  node: returns the root of the tree with the record inserted and inserted becomes true,
//  if the record already exists in the tree then original tree is returned
// Complexity: O(log n)
Node doTreeInsert(Tree t, Node n, Record rec, bool *inserted) {
    // if we've found where we need to insert, put it in and inserted becomes true
    if (n == NULL) {
        *inserted = true;
        Node new = newNode(rec);
        new->height = 1; // initialise as a leaf node
        return new;
    } else if (rec == n->rec) { // if the record already exists
        return n;
    } else {
        // finds direction the record has to go in the tree
        if (t->compare(rec, n->rec) < 0) {
            n->left = doTreeInsert(t, n->left, rec, inserted);
        } else if (t->compare(rec, n->rec) > 0) {
            n->right = doTreeInsert(t, n->right, rec, inserted);
        }

        // restructure after insertion
        int leftHeight = getHeight(n->left);
        int rightHeight = getHeight(n->right);

        // update the height 
        n->height = 1 + max(leftHeight, rightHeight);
        
        if ((leftHeight - rightHeight) > 1) {
            if (t->compare(rec, n->left->rec) > 0) {
                n->left = rotateLeft(n->left);
            }
            n = rotateRight(n);
        } else if ((rightHeight - leftHeight) > 1) {
            if (t->compare(rec, n->right->rec) < 0) {
                n->right = rotateRight(n->right);
            }
            n = rotateLeft(n);
        }
        return n;
    }
}

// rotates the tree right around n
// Input:
//  n: the node to be rotated around
// Output:
//  node: the subtree rotated
// Complexity: O(1)
Node rotateRight(Node n) {
    Node newHead = n->left;
    if (newHead == NULL) {
        return n;
    }

    // new head's right sub tree is now old heads left subtree
    n->left = newHead->right;

    // New head's right sub tree becomes old head
    newHead->right = n;
    // update heights
    newHead->height = max(getHeight(newHead->left), getHeight(newHead->right))+1;
    n->height = max(getHeight(n->left), getHeight(n->right))+1;
    return newHead;
}

// rotates the tree left around n
// Input:
//  n: the node to be rotated around
// Output:
//  node: the subtree rotated
// Complexity: O(1)
Node rotateLeft(Node n) {
    Node newHead = n->right;
    if (newHead == NULL) {
        return n;
    }

    // new head's left sub tree is now old heads left subtree
    n->right = newHead->left;
    
    // New head's left sub tree becomes old head
    newHead->left = n;
    // update heights
    newHead->height = max(getHeight(newHead->left), getHeight(newHead->right))+1;
    n->height = max(getHeight(n->left), getHeight(n->right))+1;
    return newHead;
}

// finds the max of two integers
// Input:
//  a, b: ints to be compared
// Output:
//  int: the max of a and b
// Complexity: O(1)
int max(int a, int b) {
    return a > b ? a : b;
}

// returns height of a node to avoid segmentation fault
// Input:
//  n: the node ot find the height of
// Output:
//  int: the height of the node, 0 if it is NULL
// Complexity: O(1)
int getHeight(Node n) {
    if (n == NULL) {
        return 0;
    } 
    return n->height;
}

////////////////////////////////////////////////////////////////////////

// Called to find the records between (and including) two records
// Input:
//  t: the tree we are searching in
//  lower: the lower bound record
//  upper: the upper bound record
// Output:
//  List: the list of records found between the two supplied records
// Complexity: O(log(n+m))
List TreeSearchBetween(Tree t, Record lower, Record upper) {
    List l = ListNew();
    doTreeSearchBetween(t, t->root, lower, upper, l);
    return l;
}

// helper function to accumulate the inbetween records
// Input:
//  t: the tree we are searching in
//  n: the current node we are at
//  lower: the lower bound record
//  upper: the upper bound record
//  l: the list we are accumulating results in
// Complexity: O(log(n+m))
static void doTreeSearchBetween(Tree t, Node n, Record lower,
                                Record upper, List l) {
    // if we've reached the bottom of the tree, return
    if (n == NULL) {
        return;
    }

    // if we've gone out of range, move back inside
    if (t->compare(n->rec, lower) < 0) {
        doTreeSearchBetween(t, n->right, lower, upper, l);
    } else if (t->compare(n->rec, upper) > 0) {
        doTreeSearchBetween(t, n->left, lower, upper, l);
    } else { // once we've found bounds, do in order traversal
        doTreeSearchBetween(t, n->left, lower, upper, l);
        ListAppend(l, n->rec);
        doTreeSearchBetween(t, n->right, lower, upper, l);
    }
}

////////////////////////////////////////////////////////////////////////

// called to find the next record equal to or greater than the supplied record
// Input:
//  t: the tree we are searching in
//  r: the record we are search after
// Output:
//  Record: the record equal to or greater than the supplied record
// Complexity: O(log(n))
Record TreeNext(Tree t, Record r) {
    return doTreeNext(t, t->root, r);
}

// helper function to find the next record
// Input:
//  t: the tree were are currently searching in
//  n: the node we are currently at
//  r: the record we are looking after
// Output:
//  Record: the record equal to or greater than the supplied record
// Complexity: O(log(n))
// modelled after: https://www.geeksforgeeks.org/largest-number-bst-less-equal-n/
Record doTreeNext(Tree t, Node n, Record r) {
    if (n == NULL) { // if we've reached the end of a leaf or empty tree
        return NULL;
    } else if (t->compare(n->rec, r) == 0) { // if we've found the record
        return n->rec;
    } else if (t->compare(n->rec, r) > 0) { // if we need to go left
        Record leftCheck = doTreeNext(t, n->left, r); 
        if (leftCheck == NULL) { // check if we can go back and still be after entered record
            return n->rec;
        } else {
            return leftCheck;
        }
    } 
    return doTreeNext(t, n->right, r); // continue along bst
    
}
