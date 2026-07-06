"""Project 01: Battle Preview API

Build a three-endpoint FastAPI app in a single file.
No APIRouter, no Depends — just routes calling logic directly.

Your task: implement the three endpoints below.
Run `uv run uvicorn task:app --reload` to start the server.
Run `uv run python check.py` to verify your work.
"""

from __future__ import annotations

import random
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

# ── Hardcoded monster catalog ─────────────────────────────────────────────────

MONSTERS: dict[str, dict] = {
    "goblin": {"name": "Goblin", "hp": 30,  "atk": 8,  "def_": 2},
    "orc":    {"name": "Orc",    "hp": 60,  "atk": 12, "def_": 4},
    "dragon": {"name": "Dragon", "hp": 200, "atk": 30, "def_": 10},
}

# ── Schemas ───────────────────────────────────────────────────────────────────

class HeroIn(BaseModel):
    name: str
    hp: int = Field(..., gt=0)
    atk: int = Field(..., gt=0)
    def_: int = Field(..., ge=0)


class HeroPreview(BaseModel):
    name: str
    hp: int
    atk: int
    def_: int
    power_rating: float   # atk / (def_ + 1), rounded to 2 decimal places


class BattleRequest(BaseModel):
    hero: HeroIn
    monster_name: Literal["goblin", "orc", "dragon"]  # validated by Pydantic — unknown names → 422


class BattleResult(BaseModel):
    winner: str           # "hero" or "monster"
    rounds: int
    hero_hp_remaining: int


# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(title="Battle Preview API")


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/health")
def health() -> dict:
    """Simple liveness check."""
    raise NotImplementedError


@app.post("/heroes/preview", response_model=HeroPreview)
def preview_hero(hero: HeroIn) -> HeroPreview:
    """Validate hero data and return computed stats.

    power_rating = round(hero.atk / (hero.def_ + 1), 2)
    """
    raise NotImplementedError


@app.post("/battle/simulate", response_model=BattleResult)
def simulate_battle(request: BattleRequest) -> BattleResult:
    """Simulate a battle between the hero and a monster from the catalog.

    - monster_name is validated by Pydantic (Literal) — unknown names return 422 automatically.
    - Look up the monster in MONSTERS using request.monster_name as the key.
    - Simulate round by round: each round hero attacks then monster attacks.
      Damage = max(attacker.atk - defender.def_, 1)
    - Return winner ("hero" or "monster"), rounds, and hero_hp_remaining.
    """
    raise NotImplementedError
