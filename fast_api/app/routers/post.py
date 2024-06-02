from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from ..models import Post
from ..schema import PostCreate, PostResponse
from ..database import get_db
from ..oauth2 import get_current_user


router = APIRouter(prefix="/posts", tags=["Posts"])  #tags used to categorize api documentation.


@router.get("/", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Sql query before.
    # query = "SELECT * FROM post"
    # cursor.execute(query=query)
    # posts = cursor.fetchall()
    posts = db.query(Post).all()
    return posts

# add a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post:PostCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    # fetching from a static file 
    # post_dict = dict(post)
    # post_dict["id"] = randrange(1, 10000)
    # my_posts.append(dict(post_dict))

    # feteching from my local postgress db:
    # cursor.execute(""" INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.publish))
    # mypost = cursor.fetchone()
    # conn.commit()

    print(current_user.email)

    # creating a new post through SQL_Alchemy
    post_dict = dict(post)
    # print(post_dict["publish"])
    new_created_post = Post(**post_dict)
    db.add(new_created_post)
    db.commit()
    db.refresh(new_created_post)
    return  new_created_post

@router.get("/{id}", response_model=PostResponse)
def get_post_with_id(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # post = find_post_by_id(id = id)
    # Raw SQL
    # cursor.execute(""" SELECT * from post WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    # conn.commit()

    # using sql alchemy.
    queried_post = db.query(Post).filter(Post.id ==  id).first()

    if not queried_post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return f"post with id {id} was not found."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return queried_post


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    # cursor.execute("""DELETE FROM post WHERE id = %s RETURNING * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # print(deleted_post)

    post_to_be_deleted = db.query(Post).filter(Post.id == id).first()

    if post_to_be_deleted == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} does not exist")
    
    db.delete(instance=post_to_be_deleted)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model = PostResponse)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    # Running raw query.
    # cursor.execute(""" UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (str(post.title), str(post.content), str(post.publish), str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    # index = find_post_index(id = id)
    # if index is None:

    post_query = db.query(Post).filter(Post.id == id)

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
    return  updated_post