from cs50 import get_float


def main():
    # Prompt the user for change owed in dollars, convert to cents
    cents = -1
    while cents < 0:
        dollars = get_float("Change owed: ")
        cents = round(dollars * 100)

    # Initialize total coin count
    coins = 0

    # Calculate how many quarters you should give customer
    coins += calculate_quarters(cents)
    cents = cents % 25

    # Calculate how many dimes you should give customer
    coins += calculate_dimes(cents)
    cents = cents % 10

    # Calculate how many nickels you should give customer
    coins += calculate_nickels(cents)
    cents = cents % 5

    # Calculate how many pennies you should give customer
    coins += calculate_pennies(cents)

    # Print the total number of coins
    print(coins)

def calculate_quarters(cents):
    return cents // 25

def calculate_dimes(cents):
    return cents // 10

def calculate_nickels(cents):
    return cents // 5

def calculate_pennies(cents):
    return cents


if __name__ == "__main__":
    main()
