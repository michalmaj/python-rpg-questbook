"""FastAPI dependencies for the Background Report Queue.

Pre-implemented — do not modify this file.
The functions are replaced in check.py via dependency_overrides.
"""

from task.jobs import BackgroundWorker, InMemoryJobRepository

_repo = InMemoryJobRepository()


def get_repo() -> InMemoryJobRepository:
    return _repo


def get_worker() -> BackgroundWorker:
    return BackgroundWorker(_repo)
