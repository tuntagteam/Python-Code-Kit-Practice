#include<stdio.h>

int deposit(int *balance, int amount){
    if (amount<=0){
        return 0;
    }
    
    *balance = *balance + amount;
    return 1;
}

int main()
{   
    int balance = 100;
    printf("Your balance is %d. How much more would you like to deposit? ", balance);
    int deposit_amount;
    scanf("%d", &deposit_amount);
    
    int success = deposit(&balance, deposit_amount);
    
    if (success==1){
        printf("New Balance: %d", balance);
    }else {
        printf("Transation Failed!");
    }
    
    return 0;
}