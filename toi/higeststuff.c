#include<stdio.h>

int main() {
    int num1;
    int num2;
    int num3;

    scanf("%d %d %d", &num1, &num2, &num3);
    int highest = num1;
    if (num2 > highest) {
        highest = num2;
    }
    if (num3 > highest) {
        highest = num3;
    }
    printf("%d\n", highest);
    return 0;
}