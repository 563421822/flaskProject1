from sqlalchemy import Column, Integer, ForeignKey, Enum, TIMESTAMP, Boolean

from api import db


class Lending(db.Model):
    __tablename__ = "lending"
    id = Column(Integer, primary_key=True)
    debtor_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer)
    lending_time = Column(TIMESTAMP, nullable=False)
    state = Column(Boolean)
