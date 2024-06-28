from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from models.Attraction import Attraction
from typing import Annotated

router = APIRouter()

@router.get("/attractions/")
async def index(page: Annotated[int, Query(ge=0)] = 0, keyword: Annotated[str | None, Query()] = None):
    try:
        result = Attraction.all(page, keyword)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})

@router.get("/attraction/{attraction_id}")
async def show(attraction_id: int):
    if attraction_id <= 0:
        return JSONResponse(status_code=400, content={"error": True, "message": "景點編號不正確"})

    try:
        attraction = Attraction.find(attraction_id)
        if attraction is None:
            return JSONResponse(status_code=404, content={"error": True, "message": "查無景點"})
        return {"data": attraction}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})
