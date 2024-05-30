import psycopg2
import time
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI


from .database import engine

from . import models
from .routers import user as user
from .routers import post as post

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


my_posts = [
    {
        "title" : "title of post 1",
        "content" : "content of post 1",
        "publish" : True, 
        "rating" : 4,
        "id" : 1,
    }, 
    {
        "title" : "favorite foods",
        "content" : "I like Pizza",
        "publish" : False,
        "rating" : 5,
        "id" : 2
    }
]
while True:
    try:
        conn = psycopg2.connect(host = "localhost", database = "fastapi", user = "postgres", password = "Me@Eli24", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!!!!!!!!!!!!!!")
        break
    except Exception as e:
        print("Connection to db failed......")
        print(e)
        time.sleep(2)



def find_post_by_id(id):
    for post in my_posts:
        if post["id"] == id: 
            return post
        
def find_post_index(id):
    for index, p in enumerate(my_posts):
        if p["id"] == id:
            return index 

# include router 
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

