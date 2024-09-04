from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    recommender = Column(String, nullable=True)

# class Referral(Base):
#     __tablename__ = 'referrals'
#     referral_id = Column(Integer, primary_key=True, index=True)
#     referrer_id = Column(Integer, ForeignKey('users.user_id'))
#     referee_id = Column(Integer, ForeignKey('users.user_id'))
#     referred_at = Column(DateTime)
