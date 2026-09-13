#include <stdio.h>

void helloworld(char name[]) {
    printf("Hello %s\n", name);
}

int main() {
    int i;
    int a;
    int j = 0;
    int k = 5;

    char name[50] = "Chawadol";
    int age = 23;

    printf("Hello! You are %s. You are %d years old\n", name, age);

    printf("Enter your number: ");
    scanf("%d", &a);

    for (i = 0; i < a; i++) {
        printf("%d\n", i);
    }

    while (j < 5) {
        printf("%d\n", j);
        j++;
    }

    if (k < 5) {
        printf("I don't know\n");
    } 
    else if (k > 5) {
        printf("Know don't I\n");
    } 
    else {
        printf("Don't I know\n");
    }

    helloworld("Tag");

    return 0;
}