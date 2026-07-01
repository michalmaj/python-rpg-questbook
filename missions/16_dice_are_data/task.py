import numpy as np

# In Mission 09 you rolled one die at a time with random.randint.
# NumPy lets you roll thousands of dice in a single line — and do math on all of them at once.

# TODO: Simulate 1000 d6 rolls (values 1–6).
# Hint: np.random.randint(low, high, size) — note that high is EXCLUSIVE.
rolls = None  # replace None with your np.random.randint(...) call

# TODO: Calculate the total damage dealt across all 1000 rolls.
total_damage = None  # replace None with rolls.sum()

# TODO: Calculate the average roll.
average_roll = None  # replace None with rolls.mean()

# TODO: Find the minimum and maximum roll.
min_roll = None  # replace None with rolls.min()
max_roll = None  # replace None with rolls.max()

if __name__ == "__main__":
    if rolls is None:
        print("Fill in the TODO above first: rolls = np.random.randint(...)")
    else:
        print(f"Rolls (first 10): {rolls[:10]}")
        print(f"Total damage:     {total_damage}")
        print(f"Average roll:     {average_roll:.2f}")
        print(f"Min roll:         {min_roll}")
        print(f"Max roll:         {max_roll}")
