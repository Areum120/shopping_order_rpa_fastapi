from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, crud
from ..dependencies import get_db

# 클라이언트의 요청을 적절한 처리 함수와 연결
router = APIRouter()

# URL 경로 맵핑, HTTP 메서드 맵핑, 요청 파라미터 처리, 응답 반환
router = APIRouter(
    prefix="/users",# 이 라우터에 정의된 모든 경로의 앞에 /users를 자동으로 추가
    tags=["users"],# 공통 코드 반복 줄이고, 모든 엔드포인트에서 설정 자동 상속
    responses={404: {"description": "Not found"}},
)

# 사용자 생성
@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    # 사용자 중복
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    # 이메일 중복
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db=db, user=user)


# 사용자 조회 (모든 사용자)
@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# 사용자 조회 (ID로 조회)
@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# 사용자 업데이트
@router.put("/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.update_user(db=db, user_id=user_id, user_update=user)


# 사용자 삭제
@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.delete_user(db=db, user_id=user_id)
