from fastapi import status, HTTPException, Depends, APIRouter, Response
from ..database import SessionLocal, get_db
from .. import utils, schemas, models, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func

from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)



# @router.get('/', )

@router.get('/')
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts """)
    # post =   cursor.fetchall()

    post = db.query(models.Posts,  func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Posts.id, isouter = True ).group_by(models.Posts.id).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    # post = list(map(lambda x:x._mapping,result))
    
    return  post

@router.get('/{id}')
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""SELECT * from posts WHERE id = %s """,(str(id),))
    # post = cursor.fetchone()  
    post = db.query(models.Posts,  func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Posts.id, isouter = True ).group_by(models.Posts.id).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    return  post

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *""",( post.title, post.content))
    # new_post = cursor.fetchall()
    # conn.commit()
    
    new_post = models.Posts(user_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return  new_post


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s , published = %s where id = %s RETURNING * """, (post.title, post.content, post.published, str(id) ))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the requested action")


    post_query.update(updated_post.model_dump(), synchronize_session=False)
    
    db.commit()

    return  post_query.first() 

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the requested action")

    post_query.delete(synchronize_session = False)
    db.commit()

   
    return Response(status_code=status.HTTP_204_NO_CONTENT)