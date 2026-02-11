from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# --- 1. 資料庫連線設定 ---
# 修正：SQLAlchemy 連接 PostgreSQL 時，網址開頭必須是 postgresql://
# Supabase 有時給的是 postgres://，如果是的話要在 Render 環境變數手動改成 postgresql://
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 2. 定義資料庫模型 ---
class MessageDB(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    content = Column(String)

# --- 3. 定義 Pydantic 模型 (前端傳進來的格式) ---
class UserInput(BaseModel):
    name: str
    content: str

# --- 4. 初始化 FastAPI ---
# 修正：app 只能定義一次！
app = FastAPI()

# 設定 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 取得資料庫連線的工具
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 5. API 路由 ---

@app.get("/")
def read_root():
    return {"status": "success", "message": "Render 後端與資料庫已連動"}

# 儲存訊息到資料庫
@app.post("/api/send")
def save_message(user: UserInput, db: Session = Depends(get_db)):
    new_msg = MessageDB(name=user.name, content=user.content)
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg) # 更新一下，確保拿到 ID
    return {"status": "success", "message": f"已存入資料庫：{user.name}"}

# 從資料庫抓取所有訊息
@app.get("/api/messages")
def get_all_messages(db: Session = Depends(get_db)):
    msgs = db.query(MessageDB).all()
    return msgs

# 保留你之前的測試路由
@app.get("/api/hello")
def say_hello():
    return {"data": "Hello from Python with DB!"}