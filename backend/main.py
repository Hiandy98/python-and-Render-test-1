from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# 設定 CORS：允許你的前端存取（開發時先開放所有來源）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "success", "message": "Render 後端已啟動"}

@app.get("/api/hello")
def say_hello():
    return {"data": "Hello from Python!"}

class UserInput(BaseModel):
    name: str

@app.post("/api/greet")
def greet_user(user: UserInput):
    return {"data": f"你好 {user.name}！這是來自 Python 的雲端問候 🐍"}