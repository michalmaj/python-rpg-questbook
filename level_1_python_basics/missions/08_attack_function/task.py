# Mission 08: Attack Function

# TODO: Define a function called apply_damage.
# It takes two parameters: hero_hp and damage.
# It returns hero_hp minus damage, but never below 0.
#
# def apply_damage(hero_hp, damage):
#     ...


# TODO: Define a function called apply_healing.
# It takes three parameters: hero_hp, heal_amount, max_hp.
# It returns hero_hp plus heal_amount, but never above max_hp.
#
# def apply_healing(hero_hp, heal_amount, max_hp):
#     ...


# --- Use your functions ---
hp = 100
max_hp = 100

hp = apply_damage(hp, 30)
print(f"After 30 damage:    {hp}")   # 70

hp = apply_healing(hp, 20, max_hp)
print(f"After healing 20:   {hp}")   # 90

hp = apply_damage(hp, 200)
print(f"After overkill:     {hp}")   # 0
