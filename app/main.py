from fastapi import FastAPI
from app.routers import users, test

# main.py은 애플리케이션의 설정과 초기화를 관리
app = FastAPI()

# 라우터 등록
app.include_router(users.router)
app.include_router(test.router)
