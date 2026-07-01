"""
RPG Legacy — a working game someone left you.

It runs. Don't break it. Understand it. Then fix it.
"""

import csv
import json
import os
import random


# ── Hero state — global variables ─────────────────────────────────────────────
# Everything the hero "is" lives here, at module level.

hero_name = ""
hero_class = ""     # "warrior" | "mage" | "rogue"
hero_hp = 0
hero_max_hp = 0
hero_atk = 0
hero_def = 0
potions = 0
gold = 0
wins = 0
losses = 0

# ── Combat log buffer ─────────────────────────────────────────────────────────

log_rows = []

# ── Monster table ─────────────────────────────────────────────────────────────

MONSTERS = [
    {"name": "Goblin",  "hp": 30,  "atk": 8,  "def": 2,  "gold": 10},
    {"name": "Orc",     "hp": 55,  "atk": 13, "def": 5,  "gold": 20},
    {"name": "Troll",   "hp": 80,  "atk": 18, "def": 8,  "gold": 35},
    {"name": "Dragon",  "hp": 120, "atk": 25, "def": 12, "gold": 60},
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def roll(sides):
    return random.randint(1, sides)


# ── Hero setup ────────────────────────────────────────────────────────────────

def choose_hero():
    global hero_name, hero_class, hero_hp, hero_max_hp, hero_atk, hero_def, potions, gold

    print("\n=== Welcome to RPG Legacy! ===\n")
    hero_name = input("Enter your hero's name: ").strip()
    if not hero_name:
        hero_name = "Hero"

    print("\nChoose your class:")
    print("  1. Warrior  — high HP, strong defense")
    print("  2. Mage     — low HP, powerful attacks")
    print("  3. Rogue    — balanced, many potions")

    while True:
        choice = input("\nYour choice (1/2/3): ").strip()
        if choice == "1":
            hero_class = "warrior"
            hero_hp    = 120
            hero_max_hp = 120
            hero_atk   = 15
            hero_def   = 8
            potions    = 2
            gold       = 20
            break
        elif choice == "2":
            hero_class = "mage"
            hero_hp    = 80
            hero_max_hp = 80
            hero_atk   = 24
            hero_def   = 3
            potions    = 1
            gold       = 30
            break
        elif choice == "3":
            hero_class = "rogue"
            hero_hp    = 100
            hero_max_hp = 100
            hero_atk   = 18
            hero_def   = 5
            potions    = 4
            gold       = 15
            break
        else:
            print("Please enter 1, 2, or 3.")

    print(f"\n{hero_name} the {hero_class.capitalize()} enters the dungeon!")


# ── Combat actions ────────────────────────────────────────────────────────────

def hero_attacks(monster):
    # Class-specific bonus — repeated in several places
    bonus = 0
    if hero_class == "warrior":
        bonus = 2
    elif hero_class == "rogue":
        bonus = roll(4)

    crit = roll(20)
    if crit == 20:
        dmg = (hero_atk + bonus) * 2 - monster["def"]
        if dmg < 1:
            dmg = 1
        print(f"  ⚡ CRITICAL HIT! {hero_name} deals {dmg} damage!")
    else:
        dmg = hero_atk + bonus + roll(6) - monster["def"]
        if dmg < 1:
            dmg = 1
        print(f"  ⚔  {hero_name} attacks for {dmg} damage.")

    monster["hp"] -= dmg
    log_rows.append([hero_name, hero_class, monster["name"], "attack", dmg, crit == 20])


def monster_attacks(monster):
    global hero_hp

    crit = roll(20)
    if crit == 20:
        dmg = monster["atk"] * 2 - hero_def
        if dmg < 1:
            dmg = 1
        print(f"  ⚡ CRITICAL HIT! {monster['name']} deals {dmg} damage!")
    else:
        dmg = monster["atk"] + roll(6) - hero_def
        if dmg < 1:
            dmg = 1
        print(f"  🐉 {monster['name']} attacks for {dmg} damage.")

    hero_hp -= dmg
    log_rows.append([hero_name, hero_class, monster["name"], "receive", dmg, crit == 20])


def use_potion(monster):
    global hero_hp, potions

    if potions <= 0:
        print("  No potions left!")
        return

    # Healing amount differs by class — magic numbers
    if hero_class == "warrior":
        heal = 25
    elif hero_class == "mage":
        heal = 35
    else:
        heal = 30

    hero_hp = min(hero_hp + heal, hero_max_hp)
    potions -= 1
    print(f"  🧪 {hero_name} drinks a potion (+{heal} HP). HP: {hero_hp}/{hero_max_hp}")
    log_rows.append([hero_name, hero_class, monster["name"], "heal", heal, False])


# ── Combat loop ───────────────────────────────────────────────────────────────

def run_combat(monster):
    global wins, losses, gold

    print(f"\n--- {monster['name']} appears! (HP: {monster['hp']}) ---")
    turn = 1

    while hero_hp > 0 and monster["hp"] > 0:
        print(f"\n  Turn {turn}")
        print(f"  {hero_name}: {hero_hp}/{hero_max_hp} HP  |  Potions: {potions}")
        print(f"  {monster['name']}: {monster['hp']} HP")
        print()
        print("  Actions:")
        print("    1. Attack")
        if potions > 0:
            print("    2. Use Potion")
        print("    3. Run")

        action = input("\n  > ").strip()

        if action == "1":
            hero_attacks(monster)
        elif action == "2" and potions > 0:
            use_potion(monster)
        elif action == "3":
            print(f"\n  {hero_name} flees from {monster['name']}!")
            losses += 1
            return
        else:
            print("  Unknown action — attacking instead.")
            hero_attacks(monster)

        if monster["hp"] <= 0:
            print(f"\n  🏆 {monster['name']} defeated!")
            wins += 1
            gold += monster["gold"]
            print(f"  You earned {monster['gold']} gold. Total: {gold}")
            return

        monster_attacks(monster)

        if hero_hp <= 0:
            print(f"\n  💀 {hero_name} has fallen!")
            losses += 1
            return

        turn += 1


# ── Persistence ───────────────────────────────────────────────────────────────

def save_log():
    if not log_rows:
        return

    filename = "combat_log.csv"
    write_header = not os.path.exists(filename)

    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["hero", "class", "monster", "action", "damage", "crit"])
        for row in log_rows:
            writer.writerow(row)

    log_rows.clear()
    print(f"  Log saved to {filename}.")


def save_game():
    data = {
        "hero_name":   hero_name,
        "hero_class":  hero_class,
        "hero_hp":     hero_hp,
        "hero_max_hp": hero_max_hp,
        "hero_atk":    hero_atk,
        "hero_def":    hero_def,
        "potions":     potions,
        "gold":        gold,
        "wins":        wins,
        "losses":      losses,
    }
    with open("save.json", "w") as f:
        json.dump(data, f, indent=2)
    print("  Game saved to save.json.")


def load_game():
    global hero_name, hero_class, hero_hp, hero_max_hp, hero_atk, hero_def
    global potions, gold, wins, losses

    if not os.path.exists("save.json"):
        print("  No save file found.")
        return False

    with open("save.json") as f:
        data = json.load(f)

    hero_name   = data["hero_name"]
    hero_class  = data["hero_class"]
    hero_hp     = data["hero_hp"]
    hero_max_hp = data["hero_max_hp"]
    hero_atk    = data["hero_atk"]
    hero_def    = data["hero_def"]
    potions     = data["potions"]
    gold        = data["gold"]
    wins        = data["wins"]
    losses      = data["losses"]
    print(f"  Loaded save: {hero_name} the {hero_class.capitalize()}.")
    return True


# ── Stats display ─────────────────────────────────────────────────────────────

def show_stats():
    print(f"\n  {hero_name} the {hero_class.capitalize()}")
    print(f"  HP:  {hero_hp}/{hero_max_hp}")
    print(f"  ATK: {hero_atk}  DEF: {hero_def}")
    print(f"  Potions: {potions}  Gold: {gold}  W/L: {wins}/{losses}")


# ── Main loop ─────────────────────────────────────────────────────────────────

def main():
    print("\n=== RPG Legacy ===\n")
    print("  1. New Game")
    print("  2. Load Game")
    choice = input("\n  > ").strip()

    if choice == "2":
        if not load_game():
            choose_hero()
    else:
        choose_hero()

    while True:
        if hero_hp <= 0:
            print("\n💀 Your hero is dead. Game over.")
            break

        print("\n=== Dungeon Menu ===")
        print("  1. Fight a monster")
        print("  2. Show stats")
        print("  3. Save game")
        print("  4. Quit")

        action = input("\n  > ").strip()

        if action == "1":
            monster = dict(random.choice(MONSTERS))
            run_combat(monster)
            save_log()
        elif action == "2":
            show_stats()
        elif action == "3":
            save_game()
        elif action == "4":
            print(f"\nFarewell, {hero_name}!")
            break
        else:
            print("  Unknown command.")


if __name__ == "__main__":
    main()
