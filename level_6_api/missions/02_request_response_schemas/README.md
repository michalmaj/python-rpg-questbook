# Mission 02: Request/Response Schemas

## Goal

Define Pydantic models for your API's inputs and outputs — keeping API schemas
separate from your domain dataclasses.

## Game Problem

The `/monsters` endpoint currently returns a plain list of strings. A real API
client needs structured objects: name, HP, attack, defence, gold reward. And to
kick off a battle, the client must send a hero description and a monster name.
Without schemas, there is no contract — the API can return anything and the
client has to guess.

## Python Concept

**`BaseModel`** from Pydantic turns a class into a validated, serialisable
schema. FastAPI's **`response_model=`** parameter tells the framework which
schema to use when serialising the response and generating OpenAPI docs.

Key rule: **API schemas are always separate from domain dataclasses.** Your
`rpg.domain.Monster` is a game object; `MonsterOut` is the JSON contract you
expose to clients. They may look similar today, but they evolve independently.

### Minimal Example

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ItemOut(BaseModel):
    name: str
    value: int

@app.get("/items", response_model=list[ItemOut])
def list_items() -> list[ItemOut]:
    return [ItemOut(name="Sword", value=50)]
```

## Add It to the Game

Work through the six TODOs in `task.py`:

**Step 1 — Import BaseModel**
```python
from pydantic import BaseModel
```

**Step 2 — Define `MonsterOut`**
```python
class MonsterOut(BaseModel):
    name: str
    hp: int
    atk: int
    def_: int
    gold: int
```

**Step 3 — Define `BattleRequest`**
```python
class BattleRequest(BaseModel):
    hero_name: str
    hero_class: HeroClass
    monster_name: str
```

**Step 4 — Define `BattleResultOut`**
```python
class BattleResultOut(BaseModel):
    hero_name: str
    monster_name: str
    winner: str
    rounds: int
    gold_earned: int
```

**Step 5 — Update `GET /monsters`**

Add `response_model=list[MonsterOut]` to the decorator and return full objects:
```python
@app.get("/monsters", response_model=list[MonsterOut])
def list_monsters() -> list[MonsterOut]:
    return [MonsterOut(**vars(m)) for m in _service.get_available_monsters()]
```

**Step 6 — Add `POST /battle/simulate`**
```python
@app.post("/battle/simulate", response_model=BattleResultOut)
def simulate_battle(req: BattleRequest) -> BattleResultOut:
    hero = create_hero(req.hero_name, req.hero_class)
    result = _service.simulate(hero, req.monster_name)
    import dataclasses
    return BattleResultOut(**dataclasses.asdict(result))
```

## Try It Yourself

1. Start the server: `uvicorn task:app --reload`
2. Open the interactive docs: <http://127.0.0.1:8000/docs>
3. Try `GET /monsters` — you should see full monster objects in the response.
4. Try `POST /battle/simulate` with body:
   ```json
   {"hero_name": "Ada", "hero_class": "warrior", "monster_name": "Goblin"}
   ```
5. Try sending an invalid `hero_class` value — notice how FastAPI rejects it
   with a 422 Unprocessable Entity before your code even runs.

## Break It

- Remove `response_model=` from one decorator and reload. What changes in
  `/docs`?
- Add an extra field to `MonsterOut` that doesn't exist on `Monster`. What
  error do you see?
- Send `"hero_class": "knight"` (not a valid `HeroClass`). Read the 422 body.

## Fix It

- Restore `response_model=` — notice the docs schema snaps back.
- Remove the extra field.
- Fix the hero class to one of: `warrior`, `mage`, `rogue`.

## Side Quest

Add a `GET /hero-classes` endpoint that returns `list[str]` of available
classes. Use `_service.get_hero_classes()` — no new schema needed here.

## Real-World Translation

Every production REST API has explicit request/response schemas:

| Game concept | Real world |
|---|---|
| `MonsterOut` | `ProductResponse`, `UserOut` |
| `BattleRequest` | `CreateOrderRequest`, `LoginRequest` |
| `BattleResultOut` | `OrderConfirmation`, `AuthToken` |

Keeping schemas separate from domain objects lets you version your API
(`MonsterOutV2`) without touching game logic.

## Checklist

- [ ] `MonsterOut`, `BattleRequest`, `BattleResultOut` defined in `task.py`
- [ ] `GET /monsters` returns a list of `MonsterOut` objects with a `name` field
- [ ] `GET /monsters` decorator uses `response_model=list[MonsterOut]`
- [ ] `POST /battle/simulate` returns 200 with all `BattleResultOut` fields
- [ ] `POST /battle/simulate` decorator uses `response_model=BattleResultOut`
- [ ] `uv run python check.py` prints ✅ Mission 02 complete!
