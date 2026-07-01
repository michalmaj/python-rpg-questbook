import random


def roll_damage(min_val, max_val):
    return random.randint(min_val, max_val)


def apply_damage(hp, damage):
    return max(0, hp - damage)


def apply_healing(hp, heal_amount, max_hp):
    return min(max_hp, hp + heal_amount)


def is_alive(hp):
    return hp > 0
