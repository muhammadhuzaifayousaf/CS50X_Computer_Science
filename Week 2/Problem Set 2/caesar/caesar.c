#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool only_digits(string s);
char rotate(char c, int k);

int main(int argc, string argv[])
{
    // Check if there is exactly one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Check if the key is a digit
    if (!only_digits(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Convert the key from a string to an integer
    int k = atoi(argv[1]);

    // Prompt user for plaintext
    string plaintext = get_string("plaintext:  ");

    // Print the ciphertext
    printf("ciphertext: ");

    // Iterate over each character in the plaintext
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        // Rotate the character and print it
        printf("%c", rotate(plaintext[i], k));
    }

    printf("\n");

    return 0;
}

// Function to check if the string contains only digits
bool only_digits(string s)
{
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (!isdigit(s[i]))
        {
            return false;
        }
    }
    return true;
}

// Function to rotate a character by k positions
char rotate(char c, int k)
{
    // Check if the character is an uppercase letter
    if (isupper(c))
    {
        return 'A' + (c - 'A' + k) % 26;
    }
    // Check if the character is a lowercase letter
    else if (islower(c))
    {
        return 'a' + (c - 'a' + k) % 26;
    }
    // If it's not a letter, return the character unchanged
    else
    {
        return c;
    }
}
