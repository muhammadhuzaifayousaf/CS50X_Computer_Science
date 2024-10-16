def main():
    height = 0
    while height < 1 or height > 8:
        try:
            height = int(input("Height: "))
        except ValueError:
            continue

    for i in range(height):
        print(" " * (height - i - 1), end="")
        print("#" * (i + 1), end="")
        print("  ", end="")
        print("#" * (i + 1))


if __name__ == "__main__":
    main()
