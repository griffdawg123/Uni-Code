#include <stdio.h>
#include <string.h>

#include "put_string.h"

// print s to stdout with a new line appended using fputc (only)

void put_string(char *s) {

   for (int i = 0; i < strlen(s); i++) {
      putc(s[i], stdout);
   }
   putc('\n', stdout);
}
