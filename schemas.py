from datetime import datetime
from pydantic import BaseModel
from typing import List


class Category(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Site(BaseModel):
    id: int
    link: str
    description: str

    class Config:
        orm_mode = True


class Article(BaseModel):
    id: int
    date_published: datetime.date
    title: str
    image_thumbnail_url: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
    
class OneArticle(BaseModel):
    id: int
    content: str
    date_modified: str
    date_published: datetime.date
    link: str
    title: str
    image_url: str
    image_thumbnail_url: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True    


# To avoid circular dependencies?
class CategorySchema(Category):
    articles: List[Article]


class ArticleSchema(OneArticle):
    categories: List[Category]
