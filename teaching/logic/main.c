#include<stdio.h>

int main() {
    int n;
    printf("Enter Number ");
    scanf("%d" ,&n);

    for(int i = 0; i < n; i++) {
        printf(" %d " ,i);
    }
}