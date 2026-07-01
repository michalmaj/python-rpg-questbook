# Mission 12: Save Game

import json

hero = {
    "name": "Ada",
    "class": "Warrior",
    "hp": 52,
    "max_hp": 120,
    "level": 1,
    "gold": 75,
}

# TODO: Save hero to "save_game.json".
# Use json.dump() to write the dict to a file.
#
# with open("save_game.json", "w") as f:
#     json.dump(hero, f, indent=2)

print("Game saved to save_game.json")

loaded_hero = None

# TODO: Load the save file back into loaded_hero.
# Use json.load() to read the dict from the file.
#
# with open("save_game.json", "r") as f:
#     loaded_hero = json.load(f)

if loaded_hero:
    print(f"Loaded: {loaded_hero['name']} the {loaded_hero['class']}")
    print(f"HP: {loaded_hero['hp']}/{loaded_hero['max_hp']}  |  Gold: {loaded_hero['gold']}")
else:
    print("(loaded_hero not set yet)")
