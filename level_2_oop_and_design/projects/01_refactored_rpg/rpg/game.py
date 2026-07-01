# rpg/game.py
#
# Port the main game loop here from starter_legacy_rpg/main.py.
# Use your Hero, Monster, and combat functions from the other modules.
# Requirements:
#   - choose_hero() -> Hero   (prompts for name and class, returns Hero object)
#   - run_combat(hero, monster) — one full battle with turns
#   - main() — dungeon menu: fight / stats / save / quit
#   - save_log() and save_game() / load_game() as in the original
#
# Tip: start with main() and stub the other functions, then fill them in.

import csv  # noqa: F401
import json  # noqa: F401
import os  # noqa: F401
import random  # noqa: F401

from rpg.hero import Hero, HeroClass  # noqa: F401
from rpg.monster import Monster, MONSTER_TEMPLATES  # noqa: F401
from rpg.combat import hero_turn, monster_turn  # noqa: F401


# TODO: implement choose_hero() -> Hero


# TODO: implement run_combat(hero: Hero, monster: Monster) -> None


# TODO: implement save_log(), save_game(), load_game()


# TODO: implement main()


if __name__ == "__main__":
    main()  # noqa: F821
