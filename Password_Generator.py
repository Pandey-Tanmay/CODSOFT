import random
import string


def generate_password(length):
    """Generate a random password using letters, digits, and symbols."""
    char_pool = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(char_pool) for _ in range(length))


def main():
    print("🔐 Welcome to Password Generator")
    print("-" * 50)

    # Ensure password length is valid
    while True:
        try:
            length = int(input("Enter password length: "))
            if length <= 0:
                print("❌ Password length must be greater than 0.")
                continue
            break
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

    # Generate password
    password = generate_password(length)
    print(f"\n✅ Your Generated Password: {password}")


if __name__ == "__main__":
    main()
