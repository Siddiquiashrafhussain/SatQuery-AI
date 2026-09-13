from fastapi import APIRouter

router = APIRouter()

@router.get("/suggest")
async def suggest_queries():
    return {"suggestions": ["What objects are visible?"]}
