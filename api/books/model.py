from sqlalchemy import Column, Integer, String, Date, ForeignKey

from api import db


class BooksCategories(db.Model):
    __tablename__ = 'book_categories'
    id = Column(Integer, primary_key=True)
    category_name = Column(String(10), nullable=False)
    parent_id = Column(Integer, ForeignKey('book_categories.id'))


class Books(db.Model):
    __tablename__ = 'Books'
    id = Column(Integer, primary_key=True)
    title = Column(String(20), unique=True, nullable=False)
    author = Column(String(50), unique=True, nullable=False)
    publication_date = Column(Date)
    type = Column(Integer, ForeignKey(BooksCategories.id))
    description = Column(String(250))
