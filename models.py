from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Table
from sqlalchemy.orm import relationship

from database import Base


category_articles = Table('category_articles', Base.metadata,
                          Column('category_id', ForeignKey('category.id', primary_key=True)),
                          Column('articles_id', ForeignKey('article.id', primary_key=True)))


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    articles = relationship("Article", secondary="category_articles", back_populates="categories")


class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, index=True)
    date_modified = Column(String)
    date_published = Column(String)
    image_file = Column(String)
    link = Column(String)
    title = Column(String, index=True)
    categories = relationship("Category", secondary="category_articles", back_populates="articles")
