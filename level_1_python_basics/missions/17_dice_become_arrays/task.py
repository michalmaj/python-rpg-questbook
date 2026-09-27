# Mission 17: Dice Become Arrays

import numpy as np

# --- Step 1: a small, fixed roll ---
rolls_list = [1, 4, 6, 2]

# TODO: Turn rolls_list into a NumPy array.
rolls = None  # replace with np.array(rolls_list)

# --- Step 2: shape and dtype ---

# TODO: How many elements does rolls hold, and in how many dimensions?
rolls_shape = None  # replace with rolls.shape

# TODO: What kind of values does rolls hold?
rolls_dtype = None  # replace with rolls.dtype

# --- Step 3: element-wise, array -> array ---

# TODO: Double every roll in ONE operation on the whole array.
doubled = None  # replace with rolls * 2

# --- Step 4: array + scalar ---

# TODO: Add a flat +1 bonus to every roll.
buffed = None  # replace with rolls + 1

# --- Step 5: aggregations ---

total = None    # sum of rolls
average = None  # mean of rolls
lowest = None   # min of rolls
highest = None  # max of rolls

print("=== Four rolls ===")
print(f"rolls:    {rolls}")
print(f"shape:    {rolls_shape}   dtype: {rolls_dtype}")
print(f"doubled:  {doubled}")
print(f"buffed:   {buffed}")
print(f"total={total}  average={average}  lowest={lowest}  highest={highest}")

# --- Step 6: scale up ---
#
# Same operations, 1000 rolls instead of 4. high is EXCLUSIVE, so 1-6
# needs randint(1, 7, ...).

# TODO: Simulate 1000 d6 rolls (values 1-6).
big_rolls = None  # replace with np.random.randint(1, 7, size=1000)

# TODO: The same four aggregations, now on big_rolls.
big_total = None
big_average = None
big_lowest = None
big_highest = None

if __name__ == "__main__":
    print()
    print("=== 1000 rolls ===")
    if big_rolls is None:
        print("Fill in Step 6 first: big_rolls = np.random.randint(1, 7, size=1000)")
    else:
        print(f"first 10: {big_rolls[:10]}")
        print(
            f"total={big_total}  average={big_average:.2f}  "
            f"lowest={big_lowest}  highest={big_highest}"
        )
