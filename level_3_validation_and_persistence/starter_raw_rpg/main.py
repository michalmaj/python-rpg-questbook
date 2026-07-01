# starter_raw_rpg/main.py
#
# A clean OOP RPG — result of Level 2 refactoring.
# Classes, type hints, enums, pure compute_damage function.
#
# But look at how data loading and saving work:
#
#   Smell 1 (M01/M02): json.load() with zero validation — wrong types,
#                       negative HP, missing fields all slip through silently.
#
#   Smell 2 (M04):     save_game() / load_game() are plain dicts, no
#                       schema_version, mixed directly into game logic.
#
#   Smell 3 (M05):     no abstraction over "where data is stored" —
#                       JsonSaveRepository vs SqliteSaveRepository is
#                       impossible without touching game code.
#
#   Smell 4 (M06):     CSV logging is scattered inside run_combat(),
#                       coupled to file paths and format details.
#
# Level 3 fixes these one mission at a time.

import csv
import json
import random
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

# ----- paths (smell: bare strings, not config) --------------------------------

_ROOT = Path(__file__).parent
DATA_DIR = _ROOT / "data"
SAVES_DIR = _ROOT / "saves"
SAVE_FILE = SAVES_DIR / "save_game.json"
LOG_FILE = SAVES_DIR / "combat_log.csv"


# ----- domain models ----------------------------------------------------------


class HeroClass(Enum):
    WARRIOR = "warrior"
    MAGE = "mage"
    ROGUE = "rogue"


@dataclass
class Hero:
    name: str
    hero_class: HeroClass
    hp: int
    max_hp: int
    atk: int
    def_: int
    potions: int = 3
    gold: int = 0
    wins: int = 0
    losses: int = 0

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)

    def use_potion(self) -> bool:
        if self.potions <= 0:
            return False
        self.hp = min(self.hp + 30, self.max_hp)
        self.potions -= 1
        return True


@dataclass
class Monster:
    name: str
    hp: int
    atk: int
    def_: int
    gold: int

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)


# ----- pure combat logic ------------------------------------------------------


def compute_damage(atk: int, def_: int, dice_roll: int) -> int:
    return max(1, atk + dice_roll - def_)


# ----- data loading (smell 1: no validation) ----------------------------------


def load_monsters() -> list[Monster]:
    with open(DATA_DIR / "monsters.json") as f:
        raw = json.load(f)
    # Direct dict access — if "hp" is missing or is a string, this crashes
    # or silently produces a Monster with wrong types.
    return [
        Monster(
            name=entry["name"],
            hp=entry["hp"],
            atk=entry["atk"],
            def_=entry["def"],
            gold=entry["gold"],
        )
        for entry in raw["monsters"]
    ]


def load_hero_classes() -> dict:
    with open(DATA_DIR / "hero_classes.json") as f:
        return json.load(f)


# ----- hero creation ----------------------------------------------------------


def choose_hero() -> Hero:
    classes = load_hero_classes()
    name = input("Hero name: ").strip() or "Hero"

    print("\nChoose class:")
    keys = list(classes.keys())
    for i, key in enumerate(keys, 1):
        d = classes[key]
        print(f"  {i}. {key.title()} — {d['description']}")

    choice = input("Choice (1-3): ").strip()
    try:
        idx = int(choice) - 1
        if not 0 <= idx < len(keys):
            raise ValueError
        chosen = keys[idx]
    except ValueError:
        chosen = "warrior"

    d = classes[chosen]
    return Hero(
        name=name,
        hero_class=HeroClass(chosen),
        hp=d["hp"],
        max_hp=d["hp"],
        atk=d["atk"],
        def_=d["def"],
    )


# ----- persistence (smell 2: no schema_version, no abstraction) ---------------


def save_game(hero: Hero) -> None:
    SAVES_DIR.mkdir(exist_ok=True)
    data = {
        "name": hero.name,
        "hero_class": hero.hero_class.value,
        "hp": hero.hp,
        "max_hp": hero.max_hp,
        "atk": hero.atk,
        "def_": hero.def_,
        "potions": hero.potions,
        "gold": hero.gold,
        "wins": hero.wins,
        "losses": hero.losses,
    }
    SAVE_FILE.write_text(json.dumps(data, indent=2))
    print("Game saved.")


def load_game() -> Hero | None:
    if not SAVE_FILE.exists():
        return None
    data = json.loads(SAVE_FILE.read_text())
    # No validation — if a field is missing or has the wrong type,
    # this crashes with a confusing KeyError or TypeError.
    return Hero(
        name=data["name"],
        hero_class=HeroClass(data["hero_class"]),
        hp=data["hp"],
        max_hp=data["max_hp"],
        atk=data["atk"],
        def_=data["def_"],
        potions=data["potions"],
        gold=data["gold"],
        wins=data["wins"],
        losses=data["losses"],
    )


# ----- combat logging (smell 4: I/O coupled to combat loop) -------------------


def _append_log_row(
    battle_id: int,
    turn: int,
    hero: Hero,
    monster: Monster,
    action: str,
    damage_dealt: int,
    damage_taken: int,
    result: str,
) -> None:
    SAVES_DIR.mkdir(exist_ok=True)
    write_header = not LOG_FILE.exists()
    with LOG_FILE.open("a", newline="") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow([
                "battle_id", "turn", "hero_name", "hero_class", "monster",
                "action", "damage_dealt", "damage_taken", "hero_hp", "monster_hp", "result",
            ])
        w.writerow([
            battle_id, turn, hero.name, hero.hero_class.value, monster.name,
            action, damage_dealt, damage_taken, hero.hp, monster.hp, result,
        ])


# ----- combat loop ------------------------------------------------------------


def run_combat(hero: Hero, monster: Monster, battle_id: int) -> bool:
    print(f"\n⚔  {hero.name} vs {monster.name}!")
    turn = 1

    while hero.is_alive and monster.is_alive:
        print(
            f"\nTurn {turn} | "
            f"{hero.name} HP: {hero.hp}/{hero.max_hp} | "
            f"{monster.name} HP: {monster.hp}"
        )
        action = input("Action — [a]ttack / [p]otion: ").strip().lower()

        if action == "p":
            if hero.use_potion():
                print(f"  Used potion. HP restored to {hero.hp}.")
                _append_log_row(battle_id, turn, hero, monster, "potion", 0, 0, "ongoing")
            else:
                print("  No potions left!")
            turn += 1
            continue

        # Hero attacks
        dice = random.randint(1, 6)
        dmg = compute_damage(hero.atk, monster.def_, dice)
        monster.take_damage(dmg)
        print(f"  You deal {dmg} damage (rolled {dice}). Monster HP: {monster.hp}")

        if not monster.is_alive:
            _append_log_row(battle_id, turn, hero, monster, "attack", dmg, 0, "win")
            print(f"\n✅ Victory! +{monster.gold} gold.")
            hero.gold += monster.gold
            hero.wins += 1
            return True

        # Monster attacks
        mdice = random.randint(1, 6)
        mdmg = compute_damage(monster.atk, hero.def_, mdice)
        hero.take_damage(mdmg)
        print(f"  {monster.name} deals {mdmg} damage. Your HP: {hero.hp}")

        result = "ongoing" if hero.is_alive else "loss"
        _append_log_row(battle_id, turn, hero, monster, "attack", dmg, mdmg, result)

        if not hero.is_alive:
            print("\n💀 You were defeated.")
            hero.losses += 1
            return False

        turn += 1

    return hero.is_alive


# ----- main loop --------------------------------------------------------------


def main() -> None:
    print("=== RPG Dungeon (Level 3 starter) ===\n")

    existing = load_game()
    if existing:
        ans = input(f"Continue as {existing.name}? [y/n]: ").strip().lower()
        hero = existing if ans == "y" else choose_hero()
    else:
        hero = choose_hero()

    monsters = load_monsters()
    battle_id = 1

    while True:
        print(
            f"\n--- Dungeon | HP: {hero.hp}/{hero.max_hp} | "
            f"Gold: {hero.gold} | Potions: {hero.potions} ---"
        )
        print("  [f] Fight   [s] Save   [q] Quit")
        cmd = input("> ").strip().lower()

        if cmd == "f":
            monster = random.choice(monsters)
            run_combat(hero, monster, battle_id)
            battle_id += 1
        elif cmd == "s":
            save_game(hero)
        elif cmd == "q":
            save_game(hero)
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
