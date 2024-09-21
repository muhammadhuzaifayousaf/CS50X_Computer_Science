#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// Define a BYTE type
typedef uint8_t BYTE;

// Define the block size
#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open the forensic image
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open file %s.\n", argv[1]);
        return 1;
    }

    BYTE buffer[BLOCK_SIZE];
    FILE *img = NULL;
    char filename[8];
    int file_count = 0;

    // Read the forensic image block by block
    while (fread(buffer, sizeof(BYTE), BLOCK_SIZE, file) == BLOCK_SIZE)
    {
        // Check if the block is the beginning of a new JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If a new JPEG is found and an image file is already open, close it
            if (img != NULL)
            {
                fclose(img);
            }

            // Create a new filename for the new JPEG
            sprintf(filename, "%03i.jpg", file_count);
            img = fopen(filename, "w");
            file_count++;
        }

        // If an image file is open, write the block to it
        if (img != NULL)
        {
            fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, img);
        }
    }

    // Close any remaining files
    if (img != NULL)
    {
        fclose(img);
    }
    fclose(file);

    return 0;
}
