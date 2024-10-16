import csv
import sys
import re


def main():
    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        return

    # Read database file into a variable
    db_filename = sys.argv[1]
    with open(db_filename) as db_file:
        reader = csv.DictReader(db_file)
        database = list(reader)
        str_names = reader.fieldnames[1:]  # All STR names, excluding the first column (name)

    # Read DNA sequence file into a variable
    sequence_filename = sys.argv[2]
    with open(sequence_filename) as sequence_file:
        dna_sequence = sequence_file.read().strip()

    # Find longest match of each STR in DNA sequence
    str_counts = {}
    for str_name in str_names:
        str_counts[str_name] = longest_match(dna_sequence, str_name)

    # Check database for matching profiles
    for person in database:
        if all(str_counts[str_name] == int(person[str_name]) for str_name in str_names):
            print(person["name"])
            return

    # If no match found
    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    for i in range(sequence_length):
        count = 0

        # Check for a match in a substring
        while True:
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there's a match
            if sequence[start:end] == subsequence:
                count += 1
            else:
                break

        longest_run = max(longest_run, count)

    return longest_run


if __name__ == "__main__":
    main()
