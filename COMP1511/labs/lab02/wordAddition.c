
//A program that adds two numbers together and displays the sum in words
//Griffin Doyle (z5311098), February 2020

#include <stdio.h>

int main (void) {
    int num1, num2, num3;
    
    printf("Please enter two integers: ");
    scanf("%d %d", &num1, &num2);
    num3 = num1 + num2;
    if (num1 < 0) {
        printf("negative ");
    }
    if (num1 == 0) {
        printf("zero ");
    } else if (num1 == 1 || num1 == -1) {
        printf("one ");
    } else if (num1 == 2 || num1 == -2) {
        printf("two ");
    } else if (num1 == 3 || num1 == -3) {
        printf("three ");
    } else if (num1 == 4 || num1 == -4) {
        printf("four ");
    } else if (num1 == 5 || num1 == -5) {
        printf("five ");
    } else if (num1 == 6 || num1 == -6) {
        printf("six ");
    } else if (num1 == 7 || num1 == -7) {
        printf("seven ");
    } else if (num1 == 8 || num1 == -8) {
        printf("eight ");
    } else if (num1 == 9 || num1 == -9) {
        printf("nine ");
    } else if (num1 == 10 || num1 == -10) {
        printf("ten ");
    } else {
        printf("%d ", num1);
    }
    printf("+ ");
    if (num2 < 0) {
        printf("negative ");
    }
    if (num2 == 0) {
        printf("zero ");
    } else if (num2 == 1 || num2 == -1) {
        printf("one ");
    } else if (num2 == 2 || num2 == -2) {
        printf("two ");
    } else if (num2 == 3 || num2 == -3) {
        printf("three ");
    } else if (num2 == 4 || num2 == -4) {
        printf("four ");
    } else if (num2 == 5 || num2 == -5) {
        printf("five ");
    } else if (num2 == 6 || num2 == -6) {
        printf("six ");
    } else if (num2 == 7 || num2 == -7) {
        printf("seven ");
    } else if (num2 == 8 || num2 == -8) {
        printf("eight ");
    } else if (num2 == 9 || num2 == -9) {
        printf("nine ");
    } else if (num2 == 10 || num2 == -10) {
        printf("ten ");
    } else {
        printf("%d ", num2);
    }
    printf("= ");
    if (num3 < 0) {
        printf("negative ");
    }
    if (num3 == 0) {
        printf("zero ");
    } else if (num3 == 1 || num3 == -1) {
        printf("one ");
    } else if (num3 == 2 || num3 == -2) {
        printf("two ");
    } else if (num3 == 3 || num3 == -3) {
        printf("three ");
    } else if (num3 == 4 || num3 == -4) {
        printf("four ");
    } else if (num3 == 5 || num3 == -5) {
        printf("five ");
    } else if (num3 == 6 || num3 == -6) {
        printf("six ");
    } else if (num3 == 7 || num3 == -7) {
        printf("seven ");
    } else if (num3 == 8 || num3 == -8) {
        printf("eight ");
    } else if (num3 == 9 || num3 == -9) {
        printf("nine ");
    } else if (num3 == 10 || num3 == -10) {
        printf("ten ");
    } else {
        printf("%d ", num3);
    }
    printf("\n");
}
