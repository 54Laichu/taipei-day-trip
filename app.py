from fastapi import *
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from typing import List, Optional, Dict, Annotated
from db_connect import get_db_connection
import bcrypt
import jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

app= FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
    return FileResponse("./static/index.html", media_type="text/html")
@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
    return FileResponse("./static/attraction.html", media_type="text/html")
@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
    return FileResponse("./static/booking.html", media_type="text/html")
@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
    return FileResponse("./static/thankyou.html", media_type="text/html")

#api
@app.get("/api/attractions")
async def get_attractions(page: Annotated[int, Query(ge=0)] = 0, keyword: Annotated[str | None, Query()] = None):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    query = "SELECT * FROM attractions"
    params = []

    if keyword:
        query += " WHERE name LIKE %s OR mrt = %s"
        keyword_param = f"%{keyword}%"
        params.extend([keyword_param, keyword])

    query += " LIMIT %s OFFSET %s"
    limit = 12
    offset = page * limit
    params.extend([limit, offset])

    try:
        cursor.execute(query, tuple(params))
        attractions = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) as total FROM attractions")
        total_records = cursor.fetchone()["total"]
        total_pages = (total_records + limit - 1) // limit
        next_page = page + 1 if len(attractions) == limit and page + 1 < total_pages else None

        cursor.close()
        db.close()

        return {
            "nextPage": next_page,
            "data": attractions
        }
    except Exception as e:
        cursor.close()
        db.close()
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})

@app.get("/api/attraction/{attraction_id}")
async def get_attraction(attraction_id: int):
    if attraction_id <= 0:
        return JSONResponse(status_code=400, content={"error": True, "message": "景點編號不正確"})

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM attractions WHERE id = %s", (attraction_id,))
        attraction = cursor.fetchone()
        cursor.close()
        db.close()

        if attraction is None:
            return JSONResponse(status_code=404, content={"error": True, "message": "查無景點"})

        # 將 images 轉換為列表
        attraction['images'] = attraction['images'].split(',')

        return {"data": attraction}
    except Exception as e:
        cursor.close()
        db.close()
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})

@app.get("/api/mrts")
async def get_mrts():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
        SELECT mrt
        FROM attractions
        GROUP BY mrt
        ORDER BY COUNT(*) DESC
        """)
        mrt_tuple = cursor.fetchall()
        cursor.close()
        db.close()

        mrt_list = [mrt[0] for mrt in mrt_tuple if mrt[0] is not None]
        print(mrt_list)
        return {"data": mrt_list}

    except Exception as e:
        cursor.close()
        db.close()
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})

@app.post("/api/user")
async def create_user(name: Annotated[str, Form()],email: Annotated[str, Form()], password: Annotated[str, Form()]):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("INSERT INTO Users (name, email, password) VALUES (%s, %s, %s)",
                            (name, email, password))
        db.commit()
        cursor.close()
        db.close()
        return JSONResponse(status_code = 201, content= {"message": "User created!"})
    except Exception as e:
        cursor.close()
        db.close()
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})
        #註冊會員...


@app.get("api/user/auth")
async def get_user():
    pass
 # 取得當前登入會員資訊

@app.put("api/user/auth")
async def login_user():
    pass
