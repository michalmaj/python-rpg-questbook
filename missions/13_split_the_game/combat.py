# Mission 13: Split the Game — combat module
#
# TODO: Define three functions.

# apply_damage(hp, damage) — returns max(0, hp - damage)
def apply_damage(hp, damage):
    pass


# apply_healing(hp, heal_amount, max_hp) — returns min(max_hp, hp + heal_amount)
def apply_healing(hp, heal_amount, max_hp):
    pass


# is_alive(hp) — returns True if hp > 0, False otherwise
def is_alive(hp):
    pass


if __name__ == "__main__":
    # This block only runs when you execute: uv run python missions/13_split_the_game/combat.py
    # It does NOT run when another file does: from combat import ...
    print(apply_damage(100, 30))      # 70
    print(apply_healing(70, 20, 100)) # 90
    print(is_alive(0))                # False
