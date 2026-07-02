# Mission 07: API Tests with TestClient

## Goal

Write a full pytest test suite for the RPG Battle API using FastAPI's `TestClient`
and `app.dependency_overrides` — no patching, no mocking, just clean dependency
substitution.

## Game Problem

You have a working API. But how do you know it actually works correctly after every
change? Manual `curl` testing doesn't scale. You need automated tests that spin up
the app in-process, send real HTTP requests, and assert the responses.

FastAPI ships with `TestClient` — a synchronous HTTP client backed by `httpx` that
runs your app in the same process. No network port needed.

## Python Concept: TestClient and dependency_overrides

### TestClient

```python
from fastapi.testclient import TestClient
from task.main import app

client = TestClient(app)
response = client.get("/health")
assert response.status_code == 200
```

`TestClient` wraps your `app` and lets you call any endpoint directly in a test.

### The isolation problem

The session endpoints write JSON files to `data/sessions/`. If tests use the real
`SessionRepository`, they pollute each other and leave files on disk.

You already know the fix: `Depends()`. Each dependency can be replaced for testing:

```python
app.dependency_overrides[get_session_repo] = lambda: SessionRepository(tmp_path)
```

`tmp_path` is a pytest built-in fixture — a fresh temporary directory per test.
`dependency_overrides` is a plain dict on the `app` object. Assign a new callable,
and FastAPI uses it instead of the real dependency for every request during that
test.

### The fixture pattern

```python
@pytest.fixture
def client(tmp_path):
    app.dependency_overrides[get_session_repo] = lambda: SessionRepository(tmp_path)
    yield TestClient(app)
    app.dependency_overrides.clear()   # always clean up!
```

`yield` separates setup (before) from teardown (after). The `clear()` ensures the
override doesn't leak into the next test.

## Minimal Example

```python
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

## Add It to the Game — Your Task

Open `task/tests/test_api.py`. The `client` fixture is pre-written — **do not
modify it**. Implement the 6 test stubs:

1. **`test_health_check`** — GET `/health` → 200, body `{"status": "ok"}`
2. **`test_get_monsters_returns_list`** — GET `/monsters` → 200, non-empty list,
   first item has `"name"` key
3. **`test_simulate_battle`** — POST `/battle/simulate` (warrior vs Goblin) → 200,
   `"winner"` in response
4. **`test_simulate_battle_invalid_monster`** — POST with `"FakeMonster"` → 404
5. **`test_post_session_then_get`** — POST `/sessions` → 201, extract
   `session_id`, GET `/sessions/{session_id}` → 200, `"winner"` present
6. **`test_get_session_not_found`** — GET `/sessions/nonexistent` → 404

Run the checker:

```bash
uv run python check.py
```

## Try It Yourself

After the 6 tests pass, try adding:

- A test for `GET /monsters/Goblin` → 200 with `name == "Goblin"`
- A test for `GET /monsters/FakeMonster` → 404
- A test that checks `gold_earned` is 0 when the monster wins

## Break It

Change `def test_health_check` to assert `status_code == 201` — watch it fail.
Then fix it back. This is how you know the test is actually testing something.

## Fix It

If `test_post_session_then_get` fails with a 404 on the GET:
- Check the `session_id` is extracted from the POST response JSON correctly.
- Remember: the fixture clears `dependency_overrides` after each test, but the
  same `client` object is shared within one test — so both requests go to the
  same temporary `SessionRepository`.

## Side Quest

What happens if you do `app.dependency_overrides[get_session_repo] = ...` in the
test body instead of a fixture? Try it — notice the test passes but the override
leaks into the next test if you forget `.clear()`. The fixture teardown is safer.

## Real-World Translation

`dependency_overrides` is FastAPI's built-in test seam. In production code you
use it to swap databases, external APIs, auth validators — anything injected via
`Depends()`. No `unittest.mock`, no `@patch`, no monkey-patching. The app stays
clean; the test decides what gets injected.

## Checklist

- [ ] `test_api.py` has at least 6 test functions
- [ ] `app.dependency_overrides` used in the `client` fixture
- [ ] `client.get()` / `client.post()` calls with assertions on `status_code`
- [ ] Session round-trip test (POST then GET) passes
- [ ] `uv run python check.py` prints `✅ Mission 07 complete!`
