from battle_calculator import (
    get_hero_stats,
    calculate_damage,
    calculate_healing,
    summarize_battle,
)


class TestGetHeroStats:
    def test_warrior_stats(self):
        stats = get_hero_stats("warrior")
        assert stats["class"] == "Warrior"
        assert stats["hp"] == 120
        assert stats["damage"] == 15

    def test_mage_stats(self):
        stats = get_hero_stats("mage")
        assert stats["class"] == "Mage"
        assert stats["hp"] == 80
        assert stats["damage"] == 25

    def test_rogue_stats(self):
        stats = get_hero_stats("rogue")
        assert stats["class"] == "Rogue"
        assert stats["hp"] == 100
        assert stats["damage"] == 20

    def test_all_classes_include_gold(self):
        for hero_class in ("warrior", "mage", "rogue"):
            stats = get_hero_stats(hero_class)
            assert "gold" in stats, f"{hero_class} is missing the 'gold' key"

    def test_unknown_class_returns_none(self):
        assert get_hero_stats("wizard") is None


class TestCalculateDamage:
    def test_normal_damage(self):
        assert calculate_damage(100, 30) == 70

    def test_exact_zero(self):
        assert calculate_damage(100, 100) == 0

    def test_overkill_stops_at_zero(self):
        assert calculate_damage(20, 50) == 0

    def test_zero_damage(self):
        assert calculate_damage(100, 0) == 100


class TestCalculateHealing:
    def test_normal_healing(self):
        assert calculate_healing(70, 20, 100) == 90

    def test_healing_capped_at_max_hp(self):
        assert calculate_healing(90, 20, 100) == 100

    def test_healing_at_full_hp(self):
        assert calculate_healing(100, 20, 100) == 100

    def test_full_heal_from_low(self):
        assert calculate_healing(1, 999, 100) == 100


class TestSummarizeBattle:
    def test_hero_alive_mentions_class_and_hp(self):
        result = summarize_battle("Warrior", 65)
        assert "Warrior" in result
        assert "65" in result

    def test_hero_fallen_mentions_class(self):
        result = summarize_battle("Mage", 0)
        assert "Mage" in result

    def test_hero_fallen_indicates_defeat(self):
        result = summarize_battle("Mage", 0)
        assert "fallen" in result.lower() or "0" in result

    def test_rogue_alive(self):
        result = summarize_battle("Rogue", 1)
        assert "Rogue" in result
