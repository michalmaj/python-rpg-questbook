# Mission 06: Hero Inventory

inventory = ["sword", "health potion"]

print("=== Starting Inventory ===")
for item in inventory:
    print(f"  - {item}")

# TODO: The hero finds three more items. Add them to inventory using append():
#   "shield"
#   "magic scroll"
#   "gold coin"

print()
print("=== Updated Inventory ===")
# TODO: Loop over inventory and print each item as "  - {item}"

print()
# TODO: Print f"Items carried: {len(inventory)}"

# --- Reading specific items ---

# TODO: Get the first item in inventory. Index 0 is always the first position.
first_item = None

# TODO: Get the last item in inventory. Negative indices count from the end,
# so index -1 is always the last item — no matter how long the list is.
last_item = None

# TODO: Get the first two items as a new list.
# Slicing: inventory[start:stop] — stop is not included.
first_two = None

# TODO: Check whether "shield" is in inventory. Use the `in` operator.
has_shield = None

print()
print(f"First item:  {first_item}")
print(f"Last item:   {last_item}")
print(f"First two:   {first_two}")
print(f"Has shield:  {has_shield}")
