import json
from pathlib import Path

from .domain import BattleResult, Monster


class MonsterRepository:
    def __init__(self, data_file: Path) -> None:
        self._data_file = data_file

    def list_all(self) -> list[Monster]:
        raw = json.loads(self._data_file.read_text())
        return [Monster(**entry) for entry in raw["monsters"]]

    def get(self, name: str) -> Monster | None:
        for m in self.list_all():
            if m.name.lower() == name.lower():
                return m
        return None


class SessionRepository:
    def __init__(self, sessions_dir: Path) -> None:
        self._dir = sessions_dir
        self._dir.mkdir(parents=True, exist_ok=True)

    def save(self, session_id: str, result: BattleResult) -> None:
        path = self._dir / f"{session_id}.json"
        path.write_text(json.dumps({
            "hero_name": result.hero_name,
            "monster_name": result.monster_name,
            "winner": result.winner,
            "rounds": result.rounds,
            "gold_earned": result.gold_earned,
        }))

    def get(self, session_id: str) -> BattleResult | None:
        path = self._dir / f"{session_id}.json"
        if not path.exists():
            return None
        data = json.loads(path.read_text())
        return BattleResult(**data)
