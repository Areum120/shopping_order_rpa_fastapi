from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

# 사용자 생성
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        username=user.username,
        password=user.password,  # 실제로는 해싱된 비밀번호를 저장해야 합니다.
        phone=user.phone,
        email=user.email,
        recommender=user.recommender
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# 사용자 조회 (ID로 조회)
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


# 사용자 조회 (username으로 조회)
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


# 모든 사용자 조회
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# 사용자 업데이트
def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

# 사용자 삭제
def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}
