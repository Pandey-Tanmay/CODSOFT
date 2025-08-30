# Arithmetic Functions
def add_num(num1, num2):
    return num1 + num2


def sub_num(num1, num2):
    return num1 - num2


def mul_num(num1, num2):
    return num1 * num2


def div_num(num1, num2):
    return num1 / num2


class Calculator:
    def __init__(self):
        self.num_1 = 0
        self.num_2 = 0
        self.choice = ""
        self.operators = {
            "+": add_num,
            "-": sub_num,
            "*": mul_num,
            "/": div_num
        }

    @staticmethod
    def greet():
        print("Welcome to Calculator")
        print("-" * 50)

    def take_numbers(self):
        while True:
            try:
                self.num_1 = float(input("Enter the 1st number: "))
                self.num_2 = float(input("Enter the 2nd number: "))
                break
            except ValueError:
                print("❌ Invalid input! Please enter numbers only.")

    def take_operator(self):
        while True:
            self.choice = input("Enter an operator (+, -, *, /): ").strip()
            if self.choice in self.operators:
                break
            else:
                print("❌ Invalid operator! Please choose from (+, -, *, /).")

    def calculate(self):
        try:
            operation = self.operators[self.choice]
            result = operation(self.num_1, self.num_2)
            print(f"✅ Result: {result}")
        except ZeroDivisionError:
            print("❌ Error: Division by zero is not allowed.")

    @staticmethod
    def exit_cal():
        print("\nThank you for using Calculator!")
        print("-" * 50)


def main():
    app = Calculator()
    app.greet()

    try:
        while True:
            app.take_numbers()
            app.take_operator()
            app.calculate()

            # Continue or Exit
            while True:
                con_choice = input("Do you want to continue? (y/n): ").strip().lower()
                if con_choice == "y":
                    break
                elif con_choice == "n":
                    app.exit_cal()
                    return
                else:
                    print("❌ Invalid choice! Enter 'y' to continue or 'n' to exit.")

    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
        app.exit_cal()


if __name__ == "__main__":
    main()
