// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Number of buckets in hash table (adjust based on performance)
const unsigned int N = 65536;  // 2^16 hash table buckets

// Hash table
node *table[N];

// Word counter
unsigned int word_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Get the hash index of the word
    unsigned int index = hash(word);

    // Access linked list at hash table index
    node *cursor = table[index];

    // Traverse linked list
    while (cursor != NULL)
    {
        // Compare word case-insensitively
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    // Word not found
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Hash function using djb2 algorithm (efficient for strings)
    unsigned long hash = 5381;
    int c;
    while ((c = tolower(*word++)))
    {
        hash = ((hash << 5) + hash) + c;  // hash * 33 + c
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Read words from file one at a time
    while (fscanf(file, "%45s", word) != EOF)
    {
        // Create a new node for each word
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            return false;
        }

        // Copy word into node
        strcpy(new_node->word, word);

        // Hash word to obtain a hash value
        unsigned int index = hash(word);

        // Insert node into hash table
        new_node->next = table[index];
        table[index] = new_node;

        // Increase word count
        word_count++;
    }

    // Close dictionary file
    fclose(file);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Free memory in hash table
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];

        // Free linked list
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }

    return true;
}
