from cs50 import get_string
import re
import math


def count_letters(text):
    count = 0
    for char in text:
        if char.isalpha():
            count += 1
    return count


def count_words(text):
    # Split text by spaces and return the length of the list
    return len(text.split())


def count_sentences(text):
    # Count sentences based on '.', '!', or '?'
    return len(re.findall(r'[.!?]', text))


def main():
    # Prompt the user for some text
    text = get_string("Text: ")

    # Count the number of letters, words, and sentences in the text
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # Calculate the average number of letters and sentences per 100 words
    L = (letters / words) * 100
    S = (sentences / words) * 100

    # Compute the Coleman-Liau index
    index = 0.0588 * L - 0.296 * S - 15.8

    # Round the index to the nearest whole number
    grade = round(index)

    # Print the grade level
    if grade < 1:
        print("Before Grade 1")
    elif grade >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {grade}")


if __name__ == "__main__":
    main()
