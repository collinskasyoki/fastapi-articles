from fastapi import FastAPI, Depends, HTTPException
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

import models, schemas
from database import SessionLocal, engine

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods =["*"],
    allow_headers=["*"],
)

app.mount("/thumbnails", StaticFiles(directory="media/thumbnails"))
app.mount("/images", StaticFiles(directory="media/images"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"Articles API"}

@app.get("/categories", response_model=list[schemas.Category])
async def categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    
    return categories

@app.get("/categories/{id}", response_model=schemas.Category)
async def one_category(id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.get("/categories/{id}/articles", response_model=Page[schemas.Article])
async def one_category_articles(id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    articles = (
        select(models.Article)
        .join(models.Article.categories, isouter=False)
        .filter(models.Category.id == id)
        .distinct(models.Article.id)
        .order_by(models.Article.id, models.Article.date_published.desc()))

    return paginate(db, articles)

@app.get("/articles", response_model=Page[schemas.Article])
async def articles(request: Request, db: Session = Depends(get_db)):
    query = select(models.Article).order_by(models.Article.date_published.desc())
    articles = paginate(db, query)
    for article in articles.items:
        article.image_thumbnail_url = str(request.base_url) + article.image_thumbnail_url
    return articles

@app.get("/articles/{id}", response_model=schemas.ArticleSchema)
async def one_article(request: Request, id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == id).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    article_data = {
        "id": article.id,
        "content": article.content,
        "date_modified": article.date_modified,
        "date_published": article.date_published,
        "link": article.link,
        "title": article.title,
        "image_url": str(request.base_url) + article.image_url if article.image_url else None,
        "image_thumbnail_url": str(request.base_url) + article.image_thumbnail_url if article.image_thumbnail_url else None,
        "categories": article.categories
    }

    return article_data

add_pagination(app)
