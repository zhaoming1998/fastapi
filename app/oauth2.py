from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schema, model
from .config import settings
from .database import get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

# SECRETE_KEY
# Algorithm
# Expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_min

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})

    #signature: header(algorithm), payload(to_encode), secrete(SECRETE_KEY)
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credential_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data = schema.TokenData(id=id)
    except JWTError:
        raise credential_exception
    return token_data

def get_current_user(token: str=Depends(oauth2_schema), db:Session=Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail=f'Could not validate credentials',
                                        headers={'WWW_Authenticate':'Bearer'})
    token = verify_access_token(token,credential_exception)
    user = db.query(model.User).filter(model.User.id == token.id).first()
    return user
