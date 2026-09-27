# Mission 09: Shared Inventory

# --- Part 1: Watch the bug happen (already complete — just run it) ---

starter_kit = ["dagger", "torch", "rations"]
recruit_kit = starter_kit  # looks like a copy — it isn't

recruit_kit.append("shield")  # the recruit finds a shield

print("Starter kit:", starter_kit)  # uh oh — the shield shows up here too
print("Recruit kit:", recruit_kit)


def add_item(kit, item):
    """Add an item to a kit. Notice: no return — and none is needed."""
    kit.append(item)


add_item(starter_kit, "map")
print()
print("Starter kit after add_item():", starter_kit)

# starter_kit changed twice, even though the code never wrote
# "starter_kit = ..." a second time. recruit_kit and starter_kit are two
# names for the SAME list, and add_item() received that same list as its
# `kit` parameter — mutating `kit` inside the function mutates the
# caller's list too. Compare with apply_damage() from Mission 08: that
# function returns a new value instead of mutating its argument, which
# is why calling it never surprised you like this.

# --- Part 2: Fix it ---
#
# TODO: Repeat the scenario, but give the recruit an INDEPENDENT copy of
# the kit this time, so adding to one never touches the other.
# .copy() works here because starter_kit is a flat list of strings —
# list(fixed_starter_kit) and fixed_starter_kit[:] work just as well.
fixed_starter_kit = ["dagger", "torch", "rations"]
fixed_recruit_kit = fixed_starter_kit  # <- fix this line

fixed_recruit_kit.append("shield")

print()
print("Fixed starter kit:", fixed_starter_kit)
print("Fixed recruit kit:", fixed_recruit_kit)

# --- One more contrast: plain numbers don't have this problem ---
hero_hp = 100
hp_copy = hero_hp
hp_copy -= 10
print()
print(f"hero_hp:  {hero_hp}")  # still 100
print(f"hp_copy:  {hp_copy}")  # 90 — hp_copy is a brand-new int, not a shared one
