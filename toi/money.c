#include<stdio.h>

int main() {
    int money;
    scanf("%d", &money);
    int tenCoin = 0;
    int fiveCoin = 0;
    int twoCoin = 0;
    int oneCoin = 0;
    tenCoin = money / 10;
    money = money % 10;
    fiveCoin = money / 5;
    money = money % 5;
    twoCoin = money / 2;
    money = money % 2;
    oneCoin = money;
    printf("10:%d\n5:%d\n2:%d\n1:%d\n", tenCoin, fiveCoin, twoCoin, oneCoin);
    return 0;
}