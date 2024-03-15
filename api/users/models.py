from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, func, SmallInteger

from api import db


class Users(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50))
    email = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(25))
    last_name = Column(String(25))
    age = Column(SmallInteger, nullable=True)
    gender = Column(Enum('Male', 'Female', 'Other', name='gender'), nullable=True)
    registration_date = Column(TIMESTAMP, nullable=True)
    last_login = Column(TIMESTAMP, nullable=False, server_default=func.now())
    is_active = Column(SmallInteger, nullable=False)
    deleted_at = Column(TIMESTAMP, nullable=True)

    def to_dict(self, role):
        return {
            'id': str(self.id),
            'username': self.username,
            'role_id': role.id,
            'role_name': role.role_name
        }
