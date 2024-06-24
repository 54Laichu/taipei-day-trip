from pydantic import BaseModel
import bcrypt
import jwt
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from db_connect import get_db_connection
import os

jwt_secret_key = os.environ['JWT_SECRET_KEY']
jwt_algorithm = os.environ['JWT_ALGORITHM']
jwt_expire_days = int(os.environ['JWT_EXPIRE_DAYS'])

class User(BaseModel):
    name: str
    email: str
    password: str

    @staticmethod
    def create(user: 'User'):
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

class UserAuth(BaseModel):
    email: str
    password: str

    @staticmethod
    def login(user_request: 'UserAuth'):
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

    @staticmethod
    def check_jwt(request):
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
