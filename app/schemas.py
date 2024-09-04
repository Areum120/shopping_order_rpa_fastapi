# User 모델에 대한 Pydantic 스키마 정의.
# 생성, 업데이트, 조회에 필요한 스키마 정의.

from pydantic import BaseModel, EmailStr
from typing import Optional

# 기본 사용자 스키마 (공통 속성)
class UserBase(BaseModel):
    name: str
    username: str
    phone: Optional[str] = None
    email: EmailStr
    recommender: Optional[str] = None

# 사용자 생성 스키마
class UserCreate(UserBase):
    password: str

# 사용자 업데이트 스키마
class UserUpdate(UserBase):
    password: Optional[str] = None

# 사용자 조회 스키마 (읽기 전용)
class User(UserBase):
    user_id: int

    class Config:
        from_attributes = True #v2는 orm_mode->from_attributes로 변경
