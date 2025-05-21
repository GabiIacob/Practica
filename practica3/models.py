from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False) 
    
    meals = relationship("Meal", backref="user", lazy=True)

class Meal(Base):
    __tablename__ = "meals"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    food_name = Column(String(255), nullable=False)
    calories = Column(Float, nullable=False)
    proteins = Column(Float, nullable=False)
    fats = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

DATABASE_URL = "sqlite:///users.db"  

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
   
    from sqlalchemy.orm import Session

    Base.metadata.create_all(bind=engine)

    db_generator = get_db()
    db: Session = next(db_generator) 
    print("Database connection successful!")

    try:
        new_user = User(name="testuser", email="test@example.com", password="hashed_password")
        db.add(new_user)
        db.commit()
        print("User created successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {e}")
    finally:
        db.close()
