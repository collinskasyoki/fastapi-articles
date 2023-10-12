from datetime import datetime
from pydantic import BaseModel
from typing import List


class Category(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Article(BaseModel):
    id: int
    content: str
    date_modified: str
    date_published: datetime.date
    image_file: str
    link: str
    title: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
    


# To avoid circular dependencies?
class CategorySchema(Category):
    articles: List[Article]


class ArticleSchema(Article):
    categories: List[Category]
