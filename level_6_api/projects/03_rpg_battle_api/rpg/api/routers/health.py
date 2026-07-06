"""Health check router."""
from fastapi import APIRouter

router = APIRouter()

# TODO: Add GET /health endpoint
# It should return: {"status": "ok", "version": "1.0"}
# No Depends() needed — this endpoint has no dependencies.
#
# Example:
#   @router.get("/health")
#   def health_check():
#       return {"status": "ok", "version": "1.0"}
