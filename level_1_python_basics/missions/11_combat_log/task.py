# Mission 11: Combat Log
#
# This data comes from the Mission 04 battle: Hero (100 HP) vs Goblin (60 HP).

combat_log = [
    {"round": 1, "hero_hp": 88, "monster_hp": 45, "hero_dmg": 15, "monster_dmg": 12},
    {"round": 2, "hero_hp": 76, "monster_hp": 30, "hero_dmg": 15, "monster_dmg": 12},
    {"round": 3, "hero_hp": 64, "monster_hp": 15, "hero_dmg": 15, "monster_dmg": 12},
    {"round": 4, "hero_hp": 52, "monster_hp":  0, "hero_dmg": 15, "monster_dmg": 12},
]

# TODO: Write combat_log to "combat_log.csv".
# Use a with statement so the file closes automatically.
#
# Step 1: Open the file for writing:
#   with open("combat_log.csv", "w") as f:
#
# Step 2: Write the header line:
#   f.write("round,hero_hp,monster_hp,hero_dmg,monster_dmg\n")
#
# Step 3: Loop over combat_log and write one line per entry:
#   for entry in combat_log:
#       f.write(f"{entry['round']},{entry['hero_hp']},{entry['monster_hp']},"
#               f"{entry['hero_dmg']},{entry['monster_dmg']}\n")

print("Combat log written to combat_log.csv")
