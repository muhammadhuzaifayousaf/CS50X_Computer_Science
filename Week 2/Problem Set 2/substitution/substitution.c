#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

bool is_valid_key(string key);
char substitute(char c, string key);

int main(int argc, string argv[])
{
    // Step 1: Check for correct number of command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    // Step 2: Validate the key
    string key = argv[1];
    if (!is_valid_key(key))
    {
        printf("Key must contain 26 unique alphabetic characters.\n");
        return 1;
    }

    // Step 3: Get plaintext from user
    string plaintext = get_string("plaintext: ");

    // Step 4: Encrypt plaintext
    printf("ciphertext: ");
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        printf("%c", substitute(plaintext[i], key));
    }
    printf("\n");

    // Step 5: End program
    return 0;
}

// Check if the key is valid
bool is_valid_key(string key)
{
    // Check if the key length is 26
    if (strlen(key) != 26)
    {
        return false;
    }

    // Check if all characters in the key are unique and alphabetic
    bool seen[26] = {false};
    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(key[i]))
        {
            return false;
        }

        int index = toupper(key[i]) - 'A';
        if (seen[index])
        {
            return false;
        }
        seen[index] = true;
    }

    return true;
}

// Substitute character with key
char substitute(char c, string key)
{
    if (isalpha(c))
    {
        if (isupper(c))
        {
            return toupper(key[c - 'A']);
        }
        else
        {
            return tolower(key[c - 'a']);
        }
    }
    return c;
}
