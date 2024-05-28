import psycopg2
import time

from psycopg2.extras import RealDictCursor

from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

from sqlalchemy.orm import Session

from .database import engine, get_db

from . import models

from typing import Optional

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



class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None




def find_post_by_id(id):
    for post in my_posts:
        if post["id"] == id: 
            return post
        
def find_post_index(id):
    for index, p in enumerate(my_posts):
        if p["id"] == id:
            return index 

# home url
@app.get("/")
def root():
    return {"message" : "Hello World"}

# retrieve all posts
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # Sql query before.
    # query = "SELECT * FROM post"
    # cursor.execute(query=query)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {
        "data" : posts
    }

# add a post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:Post, db: Session = Depends(get_db)):

    # fetching from a static file 
    # post_dict = dict(post)
    # post_dict["id"] = randrange(1, 10000)
    # my_posts.append(dict(post_dict))

    # feteching from my local postgress db:
    # cursor.execute(""" INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.publish))
    # mypost = cursor.fetchone()
    # conn.commit()

    # creating a new post through SQL_Alchemy
    post_dict = dict(post)
    # print(post_dict["publish"])
    new_created_post = models.Post(**post_dict)
    db.add(new_created_post)
    db.commit()
    db.refresh(new_created_post)
    return {"data" : new_created_post}

@app.get("/posts/{id}")
def get_post_with_id(id: int, db: Session = Depends(get_db)):
    # post = find_post_by_id(id = id)
    # Raw SQL
    # cursor.execute(""" SELECT * from post WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    # conn.commit()

    # using sql alchemy.
    queried_post = db.query(models.Post).filter(models.Post.id ==  id).first()

    if not queried_post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return f"post with id {id} was not found."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail" : queried_post}


@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute("""DELETE FROM post WHERE id = %s RETURNING * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # print(deleted_post)

    post_to_be_deleted = db.query(models.Post).filter(models.Post.id == id).first()

    if post_to_be_deleted == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} does not exist")
    
    db.delete(instance=post_to_be_deleted)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):

    # Running raw query.
    # cursor.execute(""" UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (str(post.title), str(post.content), str(post.publish), str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    # index = find_post_index(id = id)
    # if index is None:

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post_to_be_updated = post_query.first()
    if post_to_be_updated == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} does not exist")
    
    update_post_dict = dict(post)
    post_query.update(values = {"title" : update_post_dict["title"], "content" : update_post_dict["content"], "published" : update_post_dict["published"]}, synchronize_session=False)
    db.commit()

    updated_post = post_query.first()
    
    # post_dict = dict(post)
    # post_dict["id"] = id

    # my_posts[index] = post_dict
    return {"data" : updated_post}

# Connection through sqlalchemy
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    queried_posts = db.query(models.Post).all()
    print(queried_posts)
    return {"data" : queried_posts}