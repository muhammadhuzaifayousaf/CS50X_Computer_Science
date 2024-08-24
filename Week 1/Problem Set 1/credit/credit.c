#include <cs50.h>
#include <stdio.h>

bool luhn_algorithm(long number);
void identify_card_type(long number);

int main(void)
{
    // Prompt the user for the credit card number
    long card_number = get_long("Number: ");

    // Check if the card number is valid using Luhn's algorithm
    if (luhn_algorithm(card_number))
    {
        // Identify the card type if valid
        identify_card_type(card_number);
    }
    else
    {
        // If not valid, print INVALID
        printf("INVALID\n");
    }
}

// Function to implement Luhn's algorithm
bool luhn_algorithm(long number)
{
    int sum = 0;
    int count = 0;

    while (number > 0)
    {
        int digit = number % 10;

        // If the position is even (considering the last digit as position 1)
        if (count % 2 == 1)
        {
            digit *= 2;
            if (digit > 9)
            {
                digit -= 9; // Same as adding the two digits together
            }
        }

        sum += digit;
        number /= 10;
        count++;
    }

    // Valid if the total modulo 10 is 0
    return (sum % 10) == 0;
}

// Function to identify the card type based on the number
void identify_card_type(long number)
{
    int first_digit = 0;
    int first_two_digits = 0;
    int length = 0;

    long temp = number;
    while (temp > 0)
    {
        length++;
        if (temp < 10)
        {
            first_digit = temp;
        }
        if (temp < 100 && temp > 9)
        {
            first_two_digits = temp;
        }
        temp /= 10;
    }

    // Identify based on length and starting digits
    if (length == 15 && (first_two_digits == 34 || first_two_digits == 37))
    {
        printf("AMEX\n");
    }
    else if (length == 16 && (first_two_digits >= 51 && first_two_digits <= 55))
    {
        printf("MASTERCARD\n");
    }
    else if ((length == 13 || length == 16) && first_digit == 4)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}
