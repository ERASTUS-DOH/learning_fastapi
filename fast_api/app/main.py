from fastapi import FastAPI
from .database import engine
from . import models
from .routers import user as user, post as post, auth as auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# include router 
app.include_router(auth.router)
app.include_router(post.router)            
app.include_router(user.router)            

# home url
@app.get("/")
def root():
    return {"message" : "Hello World"}

# retrieve all posts


# Connection through sqlalchemy
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     queried_posts = db.query(models.Post).all()
#     print(queried_posts)
#     return {"data" : queried_posts}

