from rpg.domain import TournamentSummary
from rpg.repositories import MonsterRepository
from rpg.services import SimulationService
from pathlib import Path

_DATA = Path(__file__).parent.parent / "data"


def _svc() -> SimulationService:
    return SimulationService(MonsterRepository(_DATA / "monsters.json"))


def test_simulate_tournament_returns_summary() -> None:
    result = _svc().simulate_tournament(10)
    assert isinstance(result, TournamentSummary)
    assert result.total_battles == 10
    assert result.hero_wins + result.monster_wins == 10


def test_hero_win_rate_range() -> None:
    result = _svc().simulate_tournament(50)
    assert 0.0 <= result.hero_win_rate <= 1.0


def test_to_dict_has_all_keys() -> None:
    result = _svc().simulate_tournament(5)
    d = result.to_dict()
    for key in ("total_battles", "hero_wins", "monster_wins", "hero_win_rate"):
        assert key in d
