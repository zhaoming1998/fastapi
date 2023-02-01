from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schema,model, oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix='/vote', tags=['Vote'])

@router.post('/',status_code=status.HTTP_201_CREATED)
def vote(vote:schema.Vote, db:Session=Depends(get_db),
        current_user:dict=Depends(oauth2.get_current_user)):
    #check if the post exist
    post = db.query(model.Post).filter(model.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post {vote.post_id} does not exist')
    #check if the vote exist
    vote_query = db.query(model.Vote).filter(vote.post_id==model.Vote.post_id,
                        model.Vote.user_id==current_user.id)
    found_query = vote_query.first()

    if vote.dir == 1:
        if found_query:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'user {current_user.id} has voted post {vote.post_id}')
        new_vote = model.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message':'Successfully voted'}

    if vote.dir == 0:
        if not found_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'post {vote.post_id} has not been voted')
        db.delete(found_query)
        db.commit()
        return {'message':'Successfully unvoted'}