import random
import time

class NumberGuessingGame:
    def __init__(self):
        self.number_to_guess = None
        self.attempts = 0
        self.best_score = None
        self.start_time = None

    def select_difficulty(self):
        print("Select Difficulty Level:")
        print("1. Easy (1–50)")
        print("2. Medium (1–100)")
        print("3. Hard (1–200)")
        while True:
            try:
                choice = int(input("Enter your choice (1/2/3): "))
                if choice == 1:
                    return 50
                elif choice == 2:
                    return 100
                elif choice == 3:
                    return 200
                else:
                    print("Invalid choice. Please select 1, 2, or 3.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def start_game(self):
        max_number = self.select_difficulty()
        self.number_to_guess = random.randint(1, max_number)
        self.attempts = 0
        self.start_time = time.time()
        print(f"\nI'm thinking of a number between 1 and {max_number}. Can you guess it?\n")

        while True:
            try:
                guess = int(input("Enter your guess: "))
                self.attempts += 1

                if guess < self.number_to_guess:
                    print("Too low! Try again.")
                elif guess > self.number_to_guess:
                    print("Too high! Try again.")
                else:
                    time_taken = round(time.time() - self.start_time, 2)
                    print(f"\n🎉 Congratulations! You guessed the number in {self.attempts} attempts and {time_taken} seconds.")
                    if self.best_score is None or self.attempts < self.best_score:
                        self.best_score = self.attempts
                        print("🎉 New best score!")
                    break

                # Provide a hint every 3 wrong attempts
                if self.attempts % 3 == 0:
                    self.provide_hint()

            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def provide_hint(self):
        if self.number_to_guess % 2 == 0:
            print("Hint: The number is even.")
        else:
            print("Hint: The number is odd.")

        for i in range(3, 11):
            if self.number_to_guess % i == 0:
                print(f"Hint: The number is divisible by {i}.")
                break

    def play_again(self):
        while True:
            choice = input("\nDo you want to play again? (yes/no): ").lower()
            if choice in ['yes', 'y']:
                return True
            elif choice in ['no', 'n']:
                print("Thanks for playing! Goodbye!")
                return False
            else:
                print("Invalid input. Please type 'yes' or 'no'.")

    def display_leaderboard(self):
        if self.best_score is not None:
            print(f"\n🏆 Best Score: {self.best_score} attempts\n")

# Start the game
if __name__ == "__main__":
    game = NumberGuessingGame()
    while True:
        game.start_game()
        game.display_leaderboard()
        if not game.play_again():
            break
