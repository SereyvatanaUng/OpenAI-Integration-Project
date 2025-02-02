from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:
    async def get_all_users(self, db: Session):
        return db.query(User).all()

    async def get_user_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    async def get_user_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    async def create_user(self, db: Session, user_data: dict):
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user