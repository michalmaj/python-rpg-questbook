from rpg.domain import TournamentSummary


def test_hero_win_rate_zero_battles() -> None:
    s = TournamentSummary(total_battles=0, hero_wins=0, monster_wins=0)
    assert s.hero_win_rate == 0.0


def test_hero_win_rate_calculation() -> None:
    s = TournamentSummary(total_battles=10, hero_wins=7, monster_wins=3)
    assert abs(s.hero_win_rate - 0.7) < 0.001


def test_to_markdown_contains_report_header() -> None:
    s = TournamentSummary(total_battles=5, hero_wins=3, monster_wins=2)
    md = s.to_markdown()
    assert "## Tournament Report" in md


def test_to_dict_keys() -> None:
    s = TournamentSummary(total_battles=5, hero_wins=3, monster_wins=2)
    d = s.to_dict()
    assert set(d.keys()) == {"total_battles", "hero_wins", "monster_wins", "hero_win_rate"}
