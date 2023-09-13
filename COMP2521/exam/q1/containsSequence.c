// containsSequence.c ... implementation of containsSequence function

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "list.h"

/*
    You will submit only this one file.

    Implement the function "containsSequence" below. Read the exam paper
    for a detailed specification and description of your task.

    - DO NOT modify the code in any other files except for debugging
      purposes.
    - If you wish, you can add static variables and/or helper functions
      to this file.
    - DO NOT add a "main" function to this file.
*/

int containsSequence(List seq1, List seq2) {
    Node curr1 = seq1->first;
    Node curr2 = seq2->first;
    // iterate through sub-sequence
    while (curr2 != NULL) {
      // begin moving through main list
      while (curr1 != NULL) {
        // if we've found the current item in the second sequence, move on
        if (curr1->value == curr2->value) {
          curr2 = curr2->next;
          break;
        }
        curr1 = curr1->next;
      }
      // if we've reached the end of the main sequence, we're done
      if (curr1 == NULL) {
        break;
      }
    }
    // end of main sequence found but sub sequence doesn't exist
    if (curr1 == NULL && curr2 != NULL) {
      return false;
    }
    return true;
}

