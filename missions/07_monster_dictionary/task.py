# Mission 07: Monster Dictionary

# TODO: Fill in the monster dictionary with these exact values:
# "name"   -> "Dragon"
# "hp"     -> 150
# "damage" -> 25
# "reward" -> 100

monster = {
    "name": None,
    "hp": None,
    "damage": None,
    "reward": None,
}

print(f"A wild {monster['name']} appears!")
print(f"HP:     {monster['hp']}")
print(f"Damage: {monster['damage']}")
print(f"Reward: {monster['reward']} gold")

# TODO: The hero deals 30 damage to the monster.
# Update monster["hp"] so it cannot go below 0.
# Hint: monster["hp"] = max(0, monster["hp"] - 30)
monster["hp"] = None

print()
print(f"After the hero strikes: {monster['name']} has {monster['hp']} HP remaining.")
