from .. import model,schema,oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List,Optional
from ..database import get_db

router = APIRouter(prefix='/posts', tags=['Posts'])

# get all posts under an autherized user,response_model=List[schema.Post]
@router.get('/',response_model=List[schema.PostOut])
def get_posts(db: Session = Depends(get_db),current_user:dict=Depends(oauth2.get_current_user),
            limit:int=5,skip:int=0,search:Optional[str]=''):
    """
    cursor.execute('''SELECT * FROM posts''')
    posts = cursor.fetchall()

    posts = db.query(model.Post).filter(model.Post.owner_id==current_user.id)\
                .filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
    """
    result = db.query(model.Post,func.count(model.Vote.post_id).label('votes')).join(model.Vote,
                    model.Post.id == model.Vote.post_id,isouter=True).group_by(model.Post.id)\
                        .filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
    return result


# title str, content str.......
@router.post('/', status_code=status.HTTP_201_CREATED,response_model=schema.Post)
def create_post(post:schema.CreatePost,db:Session = Depends(get_db), 
                current_user: dict = Depends(oauth2.get_current_user)):
    """
    cursor.execute('''INSERT INTO posts (title, content, published) 
                    VALUES (%s, %s, %s) RETURNING *''', 
                    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    """
    new_post = model.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# be careful to the url orders
"""
@app.get('/posts/latest')
def get_latest_post():
    cursor.execute('''SELECT * FROM posts ORDER BY created_at DESC LIMIT 1''')
    latest_post = cursor.fetchone()
    return latest_post
"""

# get specific post
@router.get('/{id}',response_model=schema.PostOut)
def get_post(id:int, db: Session=Depends(get_db),
            current_user: dict = Depends(oauth2.get_current_user)):
    """
    cursor.execute('''SELECT * FROM posts WHERE id= %s''',(str(id)))
    post = cursor.fetchone()
    """
    get_owner = db.query(model.Post).filter(model.Post.id==id).first()
    post = db.query(model.Post,func.count(model.Vote.post_id).label('votes')).join(model.Vote,
                    model.Post.id == model.Vote.post_id,isouter=True)\
                        .group_by(model.Post.id).filter(model.Post.id==id).first()
    # report 404 if post is null
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id:{id} was not found")
    if current_user.id != get_owner.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action')
    
    """response.status_code = status.HTTP_404_NOT_FOUND
        return {'message':f"post with id:{id} was not found"}"""
    return post

# delete a post
@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db),
                current_user: dict = Depends(oauth2.get_current_user)):
    """
    cursor.execute('''DELETE FORM posts WHERE id = %s''', str(id))
    post = cursor.fetchone()
    """
    post = db.query(model.Post).filter(model.Post.id==id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} does not exist')
    if current_user.id != post.first().owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action')
    # conn.commit()
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# updated posts
@router.put('/{id}',response_model=schema.Post)
def update_posts(id:int, post:schema.CreatePost, db: Session = Depends(get_db),
                current_user: dict = Depends(oauth2.get_current_user)):
    """
    cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s
                    WHERE id = %s RETURNING *''', 
                    (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    """
    post_query = db.query(model.Post).filter(model.Post.id==id)
    current_post = post_query.first()
    if current_post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} does not exist')
    if current_user.id != current_post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action')
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()