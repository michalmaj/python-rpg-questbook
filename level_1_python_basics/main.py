"""Starter script for Python RPG Questbook.

This file is intentionally tiny. The course should grow step by step, and each
new Python concept should add one meaningful piece to the terminal RPG.
"""


def main() -> None:
    hero_name = "Ada"
    hero_hp = 42
    damage = 13

    hero_hp = hero_hp - damage

    print("Python RPG Questbook")
    print("--------------------")
    print(f"Hero: {hero_name}")
    print(f"HP after attack: {hero_hp}")


if __name__ == "__main__":
    main()
