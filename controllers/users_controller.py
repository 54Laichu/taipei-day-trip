from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from models.User import User

router = APIRouter()

@router.post("/user/")
async def create(user: User = Body(...)):
    try:
        result = User.create(user)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})
