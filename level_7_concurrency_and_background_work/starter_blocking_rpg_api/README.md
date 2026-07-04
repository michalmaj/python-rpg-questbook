# Starter: Blocking RPG Tournament API

A working RPG battle API that blocks on long simulations. This is the Level 7 starter — it demonstrates the problem that missions 01-08 teach you to fix.

## Purpose

This API lets you simulate battles between heroes and monsters. The `POST /tournaments` endpoint runs N battles synchronously, blocking the request thread the entire time. With a small number of battles this is fine, but at scale it becomes a serious problem.

## Run the CLI

```bash
uv run python cli.py --battles 100
```

## Run the API server

```bash
uv run fastapi dev api/main.py
```

## Run tests

From the `starter_blocking_rpg_api/` directory:

```bash
uv run pytest tests/ -q
```

## The Problem

Try `--battles 100000` and watch it hang:

```bash
uv run python cli.py --battles 100000
```

The tournament simulation runs entirely in the calling thread. While it runs, the server cannot handle any other requests. This is the blocking problem.

## What L7 Missions Fix

Level 7 missions introduce the `job_id` pattern: instead of blocking until done, the server immediately returns a job ID. The client polls a separate endpoint to check status and retrieve the result when ready. Missions use `asyncio`, thread pools, and process pools to implement this correctly.
