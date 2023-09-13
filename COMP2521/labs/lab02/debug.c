#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include "Queue.h"
int main(void) {
    Queue q = QueueNew();
        
    // enqueue 1 to 10
    for (int i = 1; i <= 10; i++) {
        QueueEnqueue(q, i);
        assert(QueueSize(q) == i);
    }
        
    // dequeue 1 to 5
    for (int j = 1; j <= 5; j++) {
        assert(QueueFront(q) == j);
        assert(QueueDequeue(q) == j);
    }
    assert(QueueSize(q) == 5);
}