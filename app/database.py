from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import DB_USER,DB_PASSWORD,DB_PORT,DB_NAME,DB_HOST

# URL 설정
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(f"DATABASE_URL: {DATABASE_URL}")

# 데이터베이스 엔진과 세션 설정
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 데이터베이스 연결 테스트 함수
def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))  # SQL쿼리를 문자열로 작성할 때 사용
            print("Database connection successful:", result.fetchone())
    except Exception as e:
        print("Database connection error:", e)

# 함수 호출
test_connection()
