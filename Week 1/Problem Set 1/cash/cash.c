#include <cs50.h>
#include <stdio.h>

int calculate_quarters(int cents);
int calculate_dimes(int cents);
int calculate_nickels(int cents);
int calculate_pennies(int cents);

int main(void)
{
    // Prompt the user for change owed, in cents
    int cents;
    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents < 0);

    // Initialize total coin count
    int coins = 0;

    // Calculate how many quarters you should give customer
    coins += calculate_quarters(cents);
    cents = cents % 25;

    // Calculate how many dimes you should give customer
    coins += calculate_dimes(cents);
    cents = cents % 10;

    // Calculate how many nickels you should give customer
    coins += calculate_nickels(cents);
    cents = cents % 5;

    // Calculate how many pennies you should give customer
    coins += calculate_pennies(cents);

    // Print the total number of coins
    printf("%d\n", coins);
}

// Calculate how many quarters to give
int calculate_quarters(int cents)
{
    return cents / 25;
}

// Calculate how many dimes to give
int calculate_dimes(int cents)
{
    return cents / 10;
}

// Calculate how many nickels to give
int calculate_nickels(int cents)
{
    return cents / 5;
}

// Calculate how many pennies to give
int calculate_pennies(int cents)
{
    return cents;
}
