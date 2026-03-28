from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import User
import security

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, email: str, plain_password: str) -> User | None:
        hashed_pass = security.get_password_hash(plain_password)
        db_user = User(email=email, password=hashed_pass)
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            self.db.rollback()
            return None
