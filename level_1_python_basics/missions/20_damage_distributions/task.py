import numpy as np

# Two weapons with the same average damage but different spread.
# Warrior uses a d6 (1–6), Rogue uses a d4+1 (2–5).
warrior_rolls = np.random.randint(1, 7, size=10000)
rogue_rolls   = np.random.randint(2, 6, size=10000)

# TODO: Calculate the mean damage for each weapon.
warrior_mean = None
rogue_mean   = None

# TODO: Calculate the standard deviation for each weapon.
# Higher std = less predictable (wider spread of values).
warrior_std = None
rogue_std   = None

# TODO: Find the 25th and 75th percentile damage for the Warrior.
# p25 = "worst 25% of rolls land at or below this"
# p75 = "75% of rolls land at or below this"
warrior_p25 = None
warrior_p75 = None

if __name__ == "__main__":
    if warrior_mean is None:
        print("Fill in the TODO above first: warrior_mean = warrior_rolls.mean(), etc.")
    else:
        print("=== Warrior (d6: 1–6) ===")
        print(f"Mean:     {warrior_mean:.2f}")
        print(f"Std dev:  {warrior_std:.2f}")
        print(f"25th pct: {warrior_p25}")
        print(f"75th pct: {warrior_p75}")
        print()
        print("=== Rogue (d4+1: 2–5) ===")
        print(f"Mean:     {rogue_mean:.2f}")
        print(f"Std dev:  {rogue_std:.2f}")
        print()
        print("Same average, different spread — which do you prefer?")
