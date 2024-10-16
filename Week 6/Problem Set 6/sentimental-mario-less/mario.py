def print_row(spaces, bricks):
    for i in range(spaces - bricks):
        print(" ", end="")

    for i in range(bricks):
        print("#", end="")

    print()


def main():
    while True:
        try:
            n = int(input("Height: "))
            if 1 <= n <= 8:
                break
        except ValueError:
            continue

    for i in range(n):
        print_row(n, i + 1)


if __name__ == "__main__":
    main()
