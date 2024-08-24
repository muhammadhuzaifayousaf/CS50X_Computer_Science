#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;

    // Prompt user for a positive integer between 1 and 8, inclusive
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // Loop to print each row
    for (int i = 0; i < height; i++)
    {
        // Print leading spaces for left-aligned pyramid
        for (int j = 0; j < height - i - 1; j++)
        {
            printf(" ");
        }

        // Print left side of pyramid
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        // Print gap between pyramids
        printf("  ");

        // Print right side of pyramid
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        // Move to the next line
        printf("\n");
    }
}
