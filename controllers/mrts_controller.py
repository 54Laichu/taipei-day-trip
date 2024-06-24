from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from models.Attraction import Attraction

router = APIRouter()

@router.get("/mrts/")
async def index():
    try:
        mrt_list = Attraction.get_mrt_list()
        return {"data": mrt_list}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})
