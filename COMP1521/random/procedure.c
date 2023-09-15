#include <stdio.h>
#include <stdint.h>
#include <math.h>

int main(void) {
    double a[500];
    int n;
    printf("> ");
    scanf("%d", &n);
    a[0] = 2.25;
    a[1] = 1.75;
    for (int i = 2; i <= n; i++) {
        a[i] = 1/5 * sqrt(7+a[i-1])/a[i-2];
    }
    printf("%lf\n", a[n]);


}