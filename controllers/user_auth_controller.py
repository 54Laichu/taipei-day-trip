from fastapi import APIRouter, Request, Body
from fastapi.responses import JSONResponse
from models.User import UserAuth

router = APIRouter()

@router.put("/user/auth/")
async def login(user_request: UserAuth = Body(...)):
    try:
        result = UserAuth.login(user_request)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})

@router.get("/user/auth/")
async def check_jwt(request: Request):
    try:
        result = UserAuth.check_jwt(request)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})
