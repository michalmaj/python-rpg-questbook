# Mission 08: OpenAPI and API Polish

## Goal

Give the RPG Battle API a proper identity — title, description, and version — and
organise its endpoints into tagged groups so `/docs` is a pleasure to navigate.

## Game Problem

Your API works, but when a teammate opens `/docs` they see an unnamed app with all
endpoints thrown together in one unordered list. There's no description of what the
API does, no version number, and no way to tell which endpoints belong together.

OpenAPI metadata is how you turn a working API into a *documented* API. FastAPI
generates the OpenAPI schema automatically — your job is to supply the information
that makes it useful.

## Python Concept: OpenAPI Metadata

### Title, description, and version

Pass them directly to `FastAPI()`:

```python
app = FastAPI(
    title="RPG Battle API",
    description="Fight monsters, track sessions, and explore hero classes.",
    version="1.0",
)
```

FastAPI writes these into `/openapi.json` under the `"info"` key. Swagger UI
(`/docs`) displays the title as a heading and the description as formatted Markdown.

### Tags — grouping endpoints in /docs

Tags let you cluster related endpoints under a named section. Add `tags=` to
`include_router()`:

```python
app.include_router(monsters.router, tags=["Monsters"])
app.include_router(battles.router,  tags=["Battles"])
```

Every endpoint registered on that router inherits the tag. In `/docs` you'll see
collapsible sections: **Monsters**, **Battles**, and so on.

### Summaries and descriptions on individual endpoints

For finer control, annotate each route decorator:

```python
@router.get(
    "/monsters",
    response_model=list[MonsterOut],
    summary="List all monsters",
    description="Returns every monster in the catalog with stats and gold reward.",
)
def list_monsters(...):
    ...
```

`summary` is the one-line label shown next to the HTTP method in `/docs`.
`description` is expanded Markdown shown when you open the endpoint panel.

## Minimal Example

```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="Does cool things.",
    version="0.1",
)
```

```
GET /openapi.json  →  {"info": {"title": "My API", "version": "0.1", ...}}
GET /docs          →  Swagger UI with your title and description
```

## Add It to the Game — Your Tasks

Open `task/main.py` and the router files in `task/routers/`.

**Step 1 — Add metadata to `FastAPI()`** in `task/main.py`:

```python
app = FastAPI(
    title="RPG Battle API",
    description="Fight monsters, track sessions, and explore hero classes.",
    version="1.0",
)
```

**Step 2 — Add `tags=` to every `include_router()` call** in `task/main.py`:

```python
app.include_router(monsters.router, tags=["Monsters"])
app.include_router(battles.router,  tags=["Battles"])
app.include_router(sessions.router, tags=["Sessions"])
app.include_router(heroes.router,   tags=["Heroes"])
```

**Step 3 — Add `summary=` to at least 3 endpoints** across the router files.
For example, in `task/routers/monsters.py`:

```python
@router.get("/monsters", response_model=list[MonsterOut], summary="List all monsters")
```

**Step 4 — Open `/docs`** and admire the result:

```bash
uv run fastapi dev task/main.py
# then visit http://127.0.0.1:8000/docs
```

Run the checker when you're done:

```bash
uv run python check.py
```

## Try It Yourself

After the checker passes, try:

- Adding a `description=` (multi-line Markdown) to one endpoint — see how it
  renders in `/docs` when you expand the panel.
- Adding `deprecated=True` to an endpoint — watch it appear with a strikethrough
  in the UI.
- Visiting `/redoc` for the alternative ReDoc documentation view.

## Break It

Remove `description=` from `FastAPI()` and run `check.py`. You'll see:

```
❌ FastAPI() missing description= — add it to app = FastAPI(...)
```

Add it back. This is how you know the checker is enforcing the metadata.

## Fix It

If check.py says **"No tags found in OpenAPI schema"**:

- Make sure `tags=` is on the `include_router()` calls in `task/main.py`,
  not inside the router files.
- Tags on `include_router()` apply to all routes on that router — you only
  need to set them once per router, not on every `@router.get(...)`.

## Side Quest

FastAPI can also set a global `tags` list at the app level with extra metadata
(external docs URL, description) for each tag:

```python
app = FastAPI(
    ...,
    openapi_tags=[
        {"name": "Monsters", "description": "Browse the monster catalog."},
        {"name": "Battles",  "description": "Simulate combat between hero and monster."},
    ],
)
```

Add this and see how `/docs` gains a tag description panel at the top.

## Real-World Translation

Every serious FastAPI service ships with `title`, `description`, and `version`.
CI pipelines often snapshot the OpenAPI schema (`GET /openapi.json`) and diff it
between releases to catch accidental breaking changes. Tags and summaries are how
API consumers discover what an endpoint does without reading source code.

## Checklist

- [ ] `FastAPI()` has `title=`, `description=`, and `version=`
- [ ] `include_router()` calls in `main.py` have `tags=`
- [ ] At least 3 endpoints have `summary=`
- [ ] `GET /openapi.json` returns `info.description` (non-empty)
- [ ] `GET /docs` returns 200
- [ ] `uv run python check.py` prints `✅ Mission 08 complete!`
