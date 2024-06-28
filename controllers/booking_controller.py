from fastapi import APIRouter, Body, Header, HTTPException
from fastapi.responses import JSONResponse
from models.User import UserAuth
from models.Booking import Booking
from typing import Annotated

router = APIRouter()

@router.post("/booking/")
async def create(auth_header: Annotated[str, Header(alias="Authorization")], booking_info: Annotated[Booking, Body(...)]):
    try:
        user = UserAuth.check_jwt(auth_header)
        if not user:
            return JSONResponse(status_code=403, content={"error": True, "message": "Unauthorized User"})
        user_id = user['id']
        booking_info.user_id = user_id

        result = Booking.create(booking_info)
        if result != "Booking created!":
            return JSONResponse(status_code=400, content={"error": True, "message": result})
        else:
            return JSONResponse(status_code=200, content={"ok": True})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})

@router.get("/booking/")
async def show(auth_header: Annotated[str, Header(alias="Authorization")]):
    try:
        user = UserAuth.check_jwt(auth_header)
        if not user:
            return JSONResponse(status_code=403, content={"error": True, "message": "Unauthorized User"})

        user_id = user['id']
        booking_data = Booking.find(user_id)
        return JSONResponse(status_code=200, content={"data": booking_data})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})


@router.delete("/booking/")
async def destroy(auth_header: Annotated[str, Header(alias="Authorization")]):
    try:
        user = UserAuth.check_jwt(auth_header)
        if not user:
            return JSONResponse(status_code=403, content={"error": True, "message": "Unauthorized User"})

        user_id = user['id']
        result = Booking.destroy(user_id)
        if result != "Booking canceled!":
            return JSONResponse(status_code=400, content={"error": True, "message": result})
        else:
            return JSONResponse(status_code=200, content={"ok": True})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})




