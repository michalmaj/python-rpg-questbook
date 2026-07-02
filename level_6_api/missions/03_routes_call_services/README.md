# Mission 03: Routes Call Services

## Goal

Thin routes — all business logic belongs in the service layer.
The endpoint in `task.py` has a smell: combat logic lives directly inside the
function. Refactor it so the route only calls `_service.simulate()`.

## Game Problem

The `/battle/simulate` endpoint currently runs the full combat loop itself:
it deep-copies the monster, rolls dice, tracks hit points, and decides the
winner. That works, but it means combat logic is spread across two places. If
you later change how damage is calculated, you have to update both the route
and the service. Routes should be thin — they translate HTTP in/out. Services
own the rules.

## Python Concept

**Thin controller, fat service** (also called *separation of concerns*):

- **Route function** — receives the request, validates input, delegates to a
  service, returns a response. Zero business logic.
- **Service** — owns all domain rules: combat, damage calculation, gold rewards.

This makes services independently testable (no HTTP involved) and routes trivial
to read at a glance.

### Minimal Example

```python
# BAD — logic in the route
@app.post("/battle")
def battle(req: BattleRequest) -> dict:
    rounds = 0
    while hero.hp > 0 and monster.hp > 0:
        rounds += 1
        ...
    return {"winner": winner, "rounds": rounds}

# GOOD — route delegates to service
@app.post("/battle")
def battle(req: BattleRequest) -> BattleResultOut:
    hero = create_hero(req.hero_name, req.hero_class)
    result = _service.simulate(hero, req.monster_name)
    return BattleResultOut(**dataclasses.asdict(result))
```

## Add It to the Game

**Step 1 — Import what you need**

Add these imports at the top of `task.py`:

```python
import dataclasses
from rpg.services import BattleService, create_hero
```

Remove `import copy` and `import random` — those belong in the service, not here.

**Step 2 — Replace the endpoint body**

Delete everything inside `simulate_battle` and replace it with:

```python
@app.post("/battle/simulate", response_model=BattleResultOut)
def simulate_battle(req: BattleRequest) -> BattleResultOut:
    hero = create_hero(req.hero_name, req.hero_class)
    try:
        result = _service.simulate(hero, req.monster_name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return BattleResultOut(**dataclasses.asdict(result))
```

`create_hero` looks up the right HP/ATK/DEF for the chosen class — you no
longer need to hard-code `hp=120`. `_service.simulate` handles all combat and
returns a `BattleResult` dataclass; `dataclasses.asdict` turns it into a dict
that `BattleResultOut` can unpack.

## Try It Yourself

1. Start the server: `uvicorn task:app --reload`
2. Open <http://127.0.0.1:8000/docs>
3. Try `POST /battle/simulate` with:
   ```json
   {"hero_name": "Ada", "hero_class": "mage", "monster_name": "Dragon"}
   ```
4. Try all three hero classes and compare their outcomes.
5. Try a monster name that does not exist — you should get a 404.

## Break It

- Leave `copy.deepcopy` in the endpoint and run `check.py`. Read the error.
- Remove the `try/except` block and send an invalid monster name. What HTTP
  status do you get? (Without the guard, FastAPI returns a 500.)
- Call `_service.simulate(hero, "goblin")` with a lower-case name that does not
  match any monster. Does the service find it?

## Fix It

- Restore the `try/except ValueError` block to return a clean 404.
- Remove any remaining `random` or `copy` references from the route.
- Run `uv run python check.py` until it prints ✅.

## Side Quest

Add a `GET /hero-classes` endpoint that returns the list of available hero
classes. Use `_service.get_hero_classes()` — no new schema needed:

```python
@app.get("/hero-classes")
def list_hero_classes() -> list[str]:
    return _service.get_hero_classes()
```

## Real-World Translation

| Game concept | Real world |
|---|---|
| `_service.simulate(hero, monster_name)` | `order_service.place(user_id, cart)` |
| `create_hero(name, class)` | `user_factory.build(signup_dto)` |
| Route as thin translator | Controller in MVC, handler in Clean Architecture |

In every production codebase you will see this split: HTTP layer delegates
immediately to a service that knows nothing about HTTP. That boundary makes
your services reusable from CLI tools, background jobs, or tests — not just
from API routes.

## Checklist

- [ ] `import random` and `import copy` removed from `task.py`
- [ ] `create_hero()` called inside `simulate_battle` to build the hero
- [ ] `_service.simulate(hero, req.monster_name)` called in the endpoint
- [ ] `BattleResultOut` constructed from the returned `BattleResult`
- [ ] `POST /battle/simulate` returns 200 with a `winner` field
- [ ] `GET /monsters` still returns 200
- [ ] `uv run python check.py` prints ✅ Mission 03 complete!
