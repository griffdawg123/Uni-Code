// Implementation of the Queue ADT using a circular array

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include "Queue.h"

#define DEFAULT_SIZE 16 // DO NOT change this line

// DO NOT modify this struct
struct queue {
	Item *items;
	int size;
	int capacity;
	int frontIndex;
};

/**
 * Creates a new empty queue
 */
Queue QueueNew(void) {
	Queue q = malloc(sizeof(*q));
	if (q == NULL) {
		fprintf(stderr, "couldn't allocate Queue");
		exit(EXIT_FAILURE);
	}
	
	q->items = malloc(DEFAULT_SIZE * sizeof(Item));
	if (q->items == NULL) {
		fprintf(stderr, "couldn't allocate Queue");
		exit(EXIT_FAILURE);
	}
	
	q->size = 0;
	q->capacity = DEFAULT_SIZE;
	q->frontIndex = 0;
	return q;
}

/**
 * Frees all resources associated with the given queue
 */
void QueueFree(Queue q) {
	free(q->items);
	free(q);
}

/**
 * Adds an item to the end of the queue
 */
void QueueEnqueue(Queue q, Item it) {
	if (q->size >= q->capacity) { // test if we need to increase the size of the queue
		q->items = realloc(q->items, sizeof(Item)*2*q->capacity); // double the capacity
		if (q->items == NULL) { // error checks if there is enough space
			fprintf(stderr, "couldn't resize Queue\n");
			exit(EXIT_FAILURE);
		}
		for (int i = 0; i < q->size + q->frontIndex - q->capacity; i++) { // moves queue elements that are looped around to the front to the end
			q->items[q->capacity+i] = q->items[i];
		}
		q->capacity *= 2;
	}
	int newIndex = q->frontIndex + q->size; // finds the next available slot for the item to be inserted
	if (newIndex >= q->capacity) { // if the index goes past the end of the queue, send it back to the front
		newIndex -= q->capacity;
	}

	q->items[newIndex] = it;
	q->size++;

}

/**
 * Removes an item from the front of the queue and returns it
 * Assumes that the queue is not empty
 */
Item QueueDequeue(Queue q) {
	
	Item item = q->items[q->frontIndex]; // gets head of queue
	q->size--; // shrinks size of queue
	q->frontIndex++; // increases head index
	if (q->frontIndex >= q->capacity) {
		q->frontIndex -= q->capacity; // if head index goes past the end of the queue, loop to the front
	}
	return item;
}

/**
 * Gets the item at the front of the queue without removing it
 * Assumes that the queue is not empty
 */
Item QueueFront(Queue q) {
	assert(q->size > 0);
	
	return q->items[q->frontIndex];
}

/**
 * Gets the size of the given queue
 */
int QueueSize(Queue q) {
	return q->size;
}

/**
 * Returns true if the queue is empty, and false otherwise
 */
bool QueueIsEmpty(Queue q) {
	return q->size == 0;
}

/**
 * Prints the queue to the given file with items space-separated
 */
void QueueDump(Queue q, FILE *fp) {
	for (int i = q->frontIndex, j = 0; j < q->size; i = (i + 1) % q->capacity, j++) {
		fprintf(fp, "%d ", q->items[i]);
	}
	fprintf(fp, "\n");
}

