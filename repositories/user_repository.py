from config.database import db
from models.user_model import User
from sqlalchemy import select


class UserRepository:
    def __init__(self, db_session=None):
        self.db_session = db_session or db.session
    
    def save(self, user):
        """Save a user to the database"""
        try:
            self.db_session.add(user)
            self.db_session.commit()
            return user, None
        except Exception as e:
            self.db_session.rollback()
            return None, str(e)

    def find_by_id(self, user_id):
        """Find a user by ID"""
        return self.db_session.get(User, user_id)

    def find_by_username(self, username):
        """Find a user by username"""
        stmt = db.select(User).where(User.username == username)
        return self.db_session.scalars(stmt).first()
    
    def find_by_email(self, email):
        """Find a user by email"""
        stmt = db.select(User).where(User.email == email)
        return self.db_session.scalars(stmt).first()
    
    def find_all(self):
        """Find all users"""
        stmt = db.select(User)
        return self.db_session.scalars(stmt).all()
    
    def delete(self, user):
        """Delete a user"""
        try:
            self.db_session.delete(user)
            self.db_session.commit()
            return True, None
        except Exception as e:
            self.db_session.rollback()
            return False, str(e)
