from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import model, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credential: OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    # OAuth2PasswordRequestForm: {'username':'xxx','password':'xxx'}
    user = db.query(model.User).filter(model.User.email == user_credential.username).first()
    # check email address
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid Credential')
    # check password
    if not utils.verify_psw(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid Credential')

    # create token
    access_token = oauth2.create_access_token(data={'user_id':user.id})
    # return token
    return {'access_token':access_token, 'token_type': 'Bearer'}