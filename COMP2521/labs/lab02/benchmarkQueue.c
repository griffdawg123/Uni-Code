
#include <stdio.h>
#include <stdlib.h>

#include "Queue.h"

int main(void) {
	Queue q = QueueNew();
	
	// basic enqueueining
	for (int i = 1; i < 16; i++) {
		QueueEnqueue(q, i);
	}

	// basic dequeueuing
	for (int i = 1; i < 6; i++) {
		QueueDequeue(q);
	}
	
	// expansion of queue
	for (int i = 16; i < 20000; i++) {
		QueueEnqueue(q, i);
	}
	
	// extensive dequeueing
	for (int i = 1; i < 15000; i++) {
		QueueDequeue(q);
	}

	QueueFree(q);
}

