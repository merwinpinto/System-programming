// Sample C program for testing the lexical analyzer

#include <stdio.h>

int main() {
    int num1 = 10;
    int num2 = 20;
    int result = 0;

    if (num1 > num2) {
        result = num1 - num2;
    } else {
        result = num1 + num2;
    }

    for (int i = 0; i < result; i++) {
        printf("Iteration %d\n", i);
    }

    return 0;
}