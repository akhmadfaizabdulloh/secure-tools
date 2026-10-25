import string
import secrets
import subprocess
import sys


SYMBOLS = "!@#$%^&*"


def generate_password(
    length,
    use_uppercase=True,
    use_lowercase=True,
    use_numbers=True,
    use_symbols=True
):
    character_groups = []

    if use_uppercase:
        character_groups.append(string.ascii_uppercase)

    if use_lowercase:
        character_groups.append(string.ascii_lowercase)

    if use_numbers:
        character_groups.append(string.digits)

    if use_symbols:
        character_groups.append(SYMBOLS)

    # Pick one character from every selected group
    password_characters = [
        secrets.choice(group)
        for group in character_groups
    ]

    # Combine all selected character groups
    all_characters = "".join(character_groups)

    # Fill the remaining password length
    remaining_length = length - len(password_characters)

    for _ in range(remaining_length):
        password_characters.append(
            secrets.choice(all_characters)
        )

    # Shuffle the password characters
    secrets.SystemRandom().shuffle(password_characters)

    return "".join(password_characters)


def copy_to_clipboard(password):
    try:
        subprocess.run(
            ["xclip", "-selection", "clipboard"],
            input=password,
            text=True,
            check=True
        )

        print("\nPassword copied to clipboard.")

    except FileNotFoundError:
        print("\nxclip is not installed.")
        print("Install it with: $ sudo apt install xclip")


def ask_character_options():
    print("\nCharacter options:")

    use_uppercase = input(
        "Include uppercase? [Y/n]: "
    ).lower() != "n"

    use_lowercase = input(
        "Include lowercase? [Y/n]: "
    ).lower() != "n"

    use_numbers = input(
        "Include numbers?   [Y/n]: "
    ).lower() != "n"

    use_symbols = input(
        "Include symbols?   [Y/n]: "
    ).lower() != "n"

    return (
        use_uppercase,
        use_lowercase,
        use_numbers,
        use_symbols
    )


def ask_custom_options():
    while True:
        try:
            length = int(input("\nPassword length: "))

            if length < 8:
                print("Password must be at least 8 characters.")
                continue

            break

        except ValueError:
            print("Please enter a valid number.")

    while True:
        options = ask_character_options()

        if not any(options):
            print(
                "\nYou must select at least one "
                "character type."
            )
            continue

        break

    return length, options


def handle_password(password):
    print("\nGenerated password:")
    print(password)

    while True:
        print("\nWhat would you like to do?")
        print("[1] Copy password")
        print("[2] Generate again")
        print("[3] Exit")

        choice = input("\nChoose [1/2/3]: ")

        if choice == "1":
            copy_to_clipboard(password)

        elif choice == "2":
            return True

        elif choice == "3":
            print("\nGoodbye! 👋")
            return False

        else:
            print("Invalid choice. Please choose 1, 2, or 3.")


def main():
    custom_mode = "--custom" in sys.argv

    print("🔐 Random Password Generator")
    print("-" * 30)

    if custom_mode:
        length, options = ask_custom_options()

    while True:

        if custom_mode:
            password = generate_password(
                length,
                *options
            )

        else:
            # Default mode
            length = secrets.randbelow(8) + 8

            password = generate_password(length)

        generate_again = handle_password(password)

        if not generate_again:
            break


if __name__ == "__main__":
    main()