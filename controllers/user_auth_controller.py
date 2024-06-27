from fastapi import APIRouter, Body, Header
from fastapi.responses import JSONResponse
from models.User import UserAuth
from typing import Annotated

router = APIRouter()

@router.put("/user/auth/")
async def login(user_request: Annotated[UserAuth, Body(...)]):
    try:
        result = UserAuth.login(user_request)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})

@router.get("/user/auth/")
async def check_jwt(auth_header: Annotated[str, Header(alias="Authorization")]):
    try:
        user_data = UserAuth.check_jwt(auth_header)
        return JSONResponse(status_code=200, content={"data": user_data})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})
