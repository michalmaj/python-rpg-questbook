def get_hero_stats() -> dict:
    # TODO: Return a dict with these exact keys and values:
    #   "name"   → "Ada"
    #   "hp"     → 100
    #   "damage" → 15
    #   "gold"   → 50
    pass


if __name__ == "__main__":
    stats = get_hero_stats()
    if stats:
        print("=== Hero Stats ===")
        print(f"Name:   {stats['name']}")
        print(f"HP:     {stats['hp']}")
        print(f"Damage: {stats['damage']}")
        print(f"Gold:   {stats['gold']}")
