//determines the date of easter in a specific year
//Griffin Doyle (z5311098), February 2020

#include <stdio.h>

int main(void) {
    int year;
    int a, b, c, d, e, f, g, h, i, k, l, m, p;
    int month, date;
    
    printf("Enter year: ");
    scanf("%d", &year);
    
    a = year%19;
    b = year/100;
    c = year%100;
    d = b/4;
    e = b%4;
    f = (b + 8)/25;
    g = (b - f + 1)/3;
    h = (19 * a + b - d - g + 15)%30;
    i = c / 4;
    k = c%4;
    l = (32 + 2 * e + 2 * i - h - k)%7;
    m = (a + 11 * h + 22 * l)/451;
    month = (h + l - 7 * m + 114)/31;
    p = (h + l - 7 * m + 114) % 31;
    date = p + 1;
    
    printf("Easter is ");
    if (month == 3) {
        printf("March %d in %d.\n", date, year);
    } else if (month == 4) {
        printf("April %d in %d.\n", date, year);
    }
    return 0;
}
