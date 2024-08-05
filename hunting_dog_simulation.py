from random import randint, choices
from collections import Counter
import math


def run_simulation(
    dogs: list, num_paths: int = 2, num_trials: int = 100000
) -> tuple[int, int, int]:
    """Simulates the outcome of `dogs` picking from `num_paths` `num_trials` times.
    Returns the number of correctly chosen paths for the following three strategies:
        - Waldo's Strategy: follow the majority of the dogs if one exists, otherwise go completely random
        - Follow One Dog: follow the choice of the highest probability dog
        - Random: Pick a completely random path
    """
    paths = [i + 1 for i in range(num_paths)]

    follow_majority = 0
    follow_one_dog = 0
    follow_random = 0

    for _ in range(num_trials):
        # generate outcomes by weighted choice
        for dog in dogs:
            dog[1] = choices(paths, weights=dog[0], k=1)[0]

        # following the majority/random strategy
        # find the majority outcome
        outcomes = [dog[1] for dog in dogs]
        c = Counter(outcomes)
        value, count = c.most_common()[0]
        percent_count = count / len(dogs)
        if percent_count > 0.5:  # there is a majority opinion
            chosen_path = value
        else:  # disagreement, go random
            chosen_path = randint(1, num_paths)

        if chosen_path == 1:
            follow_majority += 1

        # following a single dog
        first_dog = dogs[-1][1]  # since we sort, the last dog is best
        if first_dog == 1:
            follow_one_dog += 1

        # following random
        if randint(1, num_paths) == 1:
            follow_random += 1

    return follow_majority, follow_one_dog, follow_random


def get_integer(prompt: str) -> int:
    """Just prompts the user for an integer until they give one"""
    while True:
        user_input = input(prompt)
        try:
            value = int(user_input)
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def get_probability_sequence(n: int) -> list[float]:
    """
    Asks the user to input the probabilities of the dogs in the form 'p1, p2, p3, ... , pn'.
    For example, '0.4, 0.5,0.5' is a valid input. I insist that the probabilities are increasing or equal for ease of calculations later.
    """
    if n <= 0:
        raise ValueError("The number of probabilities must be greater than 0.")

    sequence = []
    while len(sequence) < n:
        try:
            # Prompt user for input
            user_input = input(
                f"Enter {n} probabilities (one for each dog, each between 0 and 1, comma-separated): "
            )
            user_input = user_input.replace(" ", "")
            # Split input by commas to get multiple probabilities
            probabilities = user_input.split(",")

            # Convert to floats and validate
            if len(probabilities) != n:
                raise ValueError(f"Please enter exactly {n} probabilities.")

            probabilities = [float(p) for p in probabilities]

            # Validate that each probability is between 0 and 1
            for p in probabilities:
                if p < 0 or p > 1:
                    raise ValueError("Each probability must be between 0 and 1.")

            # Validate that probabilities are successively larger
            if any(
                probabilities[i] > probabilities[i + 1]
                for i in range(len(probabilities) - 1)
            ):
                raise ValueError("Each probability must be successively larger.")

            # If all validations pass, return the sequence
            return probabilities

        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")


def main():
    print("Welcome to Hunting Dog Simulator!")
    # get number of paths
    num_paths = get_integer(
        "You reach a fork in the road. How many paths forward are there? "
    )
    # now get the number of dogs.
    num_dogs = get_integer("How many dogs are in your hunting party? ")
    # now get probabilities
    probabilities = get_probability_sequence(num_dogs)
    # now ask how many trials to run?
    # num_trials = get_integer("How many trials would you like to run? ")
    num_trials = 100000

    dogs = [
        [[p] + [(1 - p) / (num_paths - 1) for _ in range(num_paths - 1)], 0]
        for p in probabilities
    ]

    follow_majority, follow_one_dog, follow_random = run_simulation(
        dogs, num_paths, num_trials
    )
    majority_accuracy, single_accuracy, random_accuracy = (
        follow_majority / num_trials,
        follow_one_dog / num_trials,
        follow_random / num_trials,
    )

    print("\n")

    print("***** Results *****")
    print(f"The simulation has been run {num_trials} times for a situation with {num_paths} possible paths and {num_dogs} dogs.")
    print("\n")

    print("*** Waldo's Strategy ***")
    print(
        "Waldo's strategy is to trust the dogs if they agree, and otherwise go random."
    )
    print(
        f"- Correct in {follow_majority} runs out of {num_trials} attempts\n- Accuracy of {majority_accuracy:.3f}"
    )
    print("\n")

    print("*** Single Dog Strategy ***")
    print("This strategy is to always trust the dog with the highest probability.")
    print(
        f"- Correct in {follow_one_dog} runs out of {num_trials} attempts\n- Accuracy of {single_accuracy:.3f}"
    )
    print("\n")

    print("*** Random Strategy ***")
    print("Always just pick a random path.")
    print(
        f"- Correct in {follow_random} runs out of {num_trials} attempts\n- Accuracy of {random_accuracy:.3f}"
    )
    print("\n")

    tolerance = 0.005
    if math.isclose(single_accuracy, majority_accuracy, abs_tol=tolerance):
        print(f"With a tolerance of {tolerance}, Waldo's strategy is equal to following the single best dog.")
    else:
        print(f"With a tolerance of {tolerance}, Waldo's strategy is NOT equal to following the single best dog.")


if __name__ == "__main__":
    main()
