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
import mysql.connector
from pydantic import BaseModel

app= FastAPI()

jwt_secret_key = os.environ['JWT_SECRET_KEY']
jwt_algorithm = os.environ['JWT_ALGORITHM']
jwt_expire_days = int(os.environ['JWT_EXPIRE_DAYS'])

class UserCreateRequest(BaseModel):
    name: str
    email: str
    password: str

class UserLoginRequest(BaseModel):
    email: str
    password: str

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
        return {"data": mrt_list}

    except Exception as e:
        cursor.close()
        db.close()
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})

@app.post("/api/user")
async def create_user(user: Annotated[UserCreateRequest, Body()]):
    try:
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("INSERT INTO Users (name, email, password) VALUES (%s, %s, %s)",
                        (user.name, user.email, hashed_password))
        db.commit()

        cursor.execute("SELECT id FROM Users WHERE email = %s", (user.email,))
        user_data = cursor.fetchone()
        cursor.close()
        db.close()

        payload = {
            "user_id": user_data['id'],
            "exp": datetime.utcnow() + timedelta(days=jwt_expire_days)
        }
        token = jwt.encode(payload, jwt_secret_key, algorithm=jwt_algorithm)
        return JSONResponse(status_code=200, content={"token": token})
    except mysql.connector.errors.IntegrityError as e:
        if e.errno == 1062:  # MySQL 重複資料錯誤代碼
            cursor.close()
            db.close()
            return JSONResponse(status_code=400, content={"error": True, "message": "email已註冊"})
        else:
            cursor.close()
            db.close()
            return JSONResponse(status_code=500, content={"error": True, "message": str(e)})
    except Exception as e:
        cursor.close()
        db.close()
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})


@app.put("/api/user/auth")
async def login_user(user_request: Annotated[UserLoginRequest, Body()]):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE email = %s", (user_request.email,))
        user_data = cursor.fetchone()
        cursor.close()
        db.close()
        if user_data and bcrypt.checkpw(user_request.password.encode('utf-8'), user_data['password'].encode('utf-8')):
            payload = {
                "user_id": user_data['id'],
                "exp": datetime.utcnow() + timedelta(days=jwt_expire_days)
            }
            token = jwt.encode(payload, jwt_secret_key, algorithm=jwt_algorithm)
            return JSONResponse(status_code=200, content={"token": token})
        else:
            return JSONResponse(status_code=400, content={"error": True, "message": "帳號或密碼錯誤"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})


@app.get("/api/user/auth")
async def check_user_jwt(request: Request):
    try:
        auth_header = request.headers.get("Authorization")
        if auth_header is None or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=200, content=None)

        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, jwt_secret_key, algorithms=[jwt_algorithm])

        user_id = payload.get("user_id")
        if user_id is None:
            return JSONResponse(status_code=200, content=None)

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email FROM Users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user is None:
            return JSONResponse(status_code=200, content=None)

        return JSONResponse(status_code=200, content={"data": user})

    except jwt.ExpiredSignatureError:
        return JSONResponse(status_code=200, content=None)
    except jwt.InvalidTokenError:
        return JSONResponse(status_code=200, content=None)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": True, "message": str(e)})
