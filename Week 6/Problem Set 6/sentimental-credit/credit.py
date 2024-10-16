from cs50 import get_string


def luhn_algorithm(number):
    sum = 0
    count = 0

    # Iterate over the digits of the number from right to left
    for digit in reversed(number):
        digit = int(digit)

        # If the position is even (starting from 1)
        if count % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9  # Same as adding the two digits together

        sum += digit
        count += 1

    # Valid if the total modulo 10 is 0
    return (sum % 10) == 0


def identify_card_type(number):
    length = len(number)
    first_digit = int(number[0])
    first_two_digits = int(number[:2])

    # Identify based on length and starting digits
    if length == 15 and (first_two_digits == 34 or first_two_digits == 37):
        print("AMEX")
    elif length == 16 and (51 <= first_two_digits <= 55):
        print("MASTERCARD")
    elif (length == 13 or length == 16) and first_digit == 4:
        print("VISA")
    else:
        print("INVALID")


def main():
    # Prompt the user for the credit card number
    card_number = get_string("Number: ")

    # Check if the card number is valid using Luhn's algorithm
    if luhn_algorithm(card_number):
        # Identify the card type if valid
        identify_card_type(card_number)
    else:
        # If not valid, print INVALID
        print("INVALID")


if __name__ == "__main__":
    main()
