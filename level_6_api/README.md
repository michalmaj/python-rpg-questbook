# Level 6: API Interface with FastAPI

**Prerequisite:** Level 5 complete.

**Central thesis:** The RPG engine works — now expose it to the world.
FastAPI turns Python functions into documented, type-safe HTTP endpoints in minutes.

## Starter: `starter_service_ready_rpg/`

A working RPG battle engine with domain, repositories, and `BattleService`.
Run it first — these are the files your API will call.

```bash
cd starter_service_ready_rpg
uv run python main.py
uv run pytest tests/ -q
```

## Missions

| # | Mission | Skill |
|---|---------|-------|
| 01 | [First FastAPI App](missions/01_first_fastapi_app/README.md) | FastAPI, uvicorn, /docs |
| 02 | [Request/Response Schemas](missions/02_request_response_schemas/README.md) | Pydantic schemas for HTTP layer |
| 03 | [Routes Call Services](missions/03_routes_call_services/README.md) | Thin routes, no logic in endpoints |
| 04 | [API Routers](missions/04_api_routers/README.md) | APIRouter, file split |
| 05 | [Dependencies and Repositories](missions/05_dependencies_and_repositories/README.md) | Depends(), DI factories |
| 06 | [API Errors and Status Codes](missions/06_api_errors_and_status_codes/README.md) | HTTPException, 404/422/500 |
| 07 | [API Tests](missions/07_api_tests/README.md) | TestClient, dependency_overrides |
| 08 | [OpenAPI and API Polish](missions/08_openapi_and_api_polish/README.md) | Tags, descriptions, /docs |

## Boss Fight

[RPG Battle API](projects/01_rpg_battle_api/README.md) — wire all 8 concepts into a
fully tested 7-endpoint battle API with JSON session persistence.

## How to start

Run from the repo root:

```bash
uv run python tools/course_status.py
```

To check your progress on a mission, run from its folder:

```bash
cd level_6_api/missions/01_first_fastapi_app
uv run python check.py
```
