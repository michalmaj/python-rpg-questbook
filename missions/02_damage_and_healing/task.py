def apply_damage(hero_hp: int, damage: int) -> int:
    # TODO: Subtract damage from hero_hp.
    # HP cannot go below 0.
    # Return the new HP value.
    pass


def apply_healing(hero_hp: int, heal_amount: int, max_hp: int) -> int:
    # TODO: Add heal_amount to hero_hp.
    # HP cannot exceed max_hp.
    # Return the new HP value.
    pass


if __name__ == "__main__":
    hp = 100
    print(f"Starting HP:       {hp}")

    hp = apply_damage(hp, 30)
    print(f"After 30 damage:   {hp}")

    hp = apply_healing(hp, 20, 100)
    print(f"After healing 20:  {hp}")

    hp = apply_damage(hp, 200)
    print(f"After 200 damage:  {hp}")
    print(f"(HP cannot go below 0)")
