# Mission 13: Split the Game

# TODO: Import apply_damage, apply_healing, and is_alive from the combat module.
# from combat import apply_damage, apply_healing, is_alive

hero_hp = 100
monster_hp = 60

hero_hp = apply_damage(hero_hp, 30)
monster_hp = apply_damage(monster_hp, 15)
hero_hp = apply_healing(hero_hp, 20, 100)

print(f"Hero HP:      {hero_hp}")
print(f"Monster HP:   {monster_hp}")
print(f"Hero alive:   {is_alive(hero_hp)}")
print(f"Monster alive:{is_alive(monster_hp)}")
