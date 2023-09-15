// prints the nth tribonacci number
// Griffin Doyle (z5311098)
// 05/05

#include <stdio.h>
#include <stdlib.h>



int main (int argc, char *argv[]) {
    int n = atoi(argv[1]);
    int num = 0;
    if (n == 1 || n == 2 || n == 3) {
        num = 1;
    } else {
        int i = 3;
        int a = 1;
        int b = 1;
        
        while (i <= n) {
            int temp = num;
            num += (a + b);
            a = b;
            b = temp;
            i++;
        }
    }
    printf("%d\n", num);
}

