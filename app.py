from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from controllers import attractions_controller, mrts_controller, users_controller, user_auth_controller, booking_controller

app = FastAPI()

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

app.include_router(attractions_controller.router, prefix="/api", tags=["attraction"])
app.include_router(mrts_controller.router, prefix="/api", tags=["mrt"])
app.include_router(users_controller.router, prefix="/api", tags=["user"])
app.include_router(user_auth_controller.router, prefix="/api", tags=["user_auth"])
app.include_router(booking_controller.router, prefix="/api", tags=["booking"])
