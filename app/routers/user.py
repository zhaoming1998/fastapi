from .. import model,schema,utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix='/users',tags=['Users'])

# create users
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.UserOut)
def create_user(user:schema.CreateUser, db:Session=Depends(get_db)):
    ExistUser = db.query(model.User).filter(model.User.email == user.email)
    if ExistUser.first() != None:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Email {user.email} already exists')
    
    # hash the password
    user.password = utils.hash_psw(user.password)

    new_user = model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}',response_model=schema.UserOut)
def get_user(id: int, db:Session=Depends(get_db)):
    user = db.query(model.User).filter(model.User.id==id).first()
    if user == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'user with id:{id} does not exist')
    return user