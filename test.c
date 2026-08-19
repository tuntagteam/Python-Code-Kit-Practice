#include <stdio.h>

int main(void) {
    long long sum = 0;

    for (int i = 1; i <= 1000000; i++) {
        if (i % 2 == 0) {
            printf("%d Even\n", i);
            sum += i;
        } else {
            printf("%d Odd\n", i);
        }
    }

    printf("Total : %lld\n", sum);

    return 0;
}
