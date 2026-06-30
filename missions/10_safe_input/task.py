# Mission 10: Safe Input

print("Monster HP challenge!")
print("Enter the monster's starting HP:")

raw = input("> ")

monster_hp = None

# TODO: Try to convert raw to an integer and assign it to monster_hp.
# If the player typed something that is not a number (ValueError),
# set monster_hp to 100 instead.
#
# try:
#     monster_hp = int(raw)
# except ValueError:
#     monster_hp = 100

print(f"Monster HP: {monster_hp}")
