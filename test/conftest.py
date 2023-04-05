# pytest can run use the fixture in conftest.py automatically without importing 
import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.oauth2 import create_access_token
from app.config import settings
from app import model

#create a database for test only
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_user}:{settings.database_password}@{settings.database_host}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)   

@pytest.fixture
def session():
    # clean all the table before test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# run the api in test
@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    # replace the dependency of database with test database
    app.dependency_overrides[get_db]=override_get_db
    return TestClient(app)

@pytest.fixture
def test_user2(client):
    user_data = {"email":"4321@gmail.com","password":'123456'}
    res = client.post('/users/', json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']
    assert res.status_code == 201
    return new_user

@pytest.fixture
def test_user(client):
    user_data = {"email":"1234@gmail.com","password":'123456'}
    res = client.post('/users/', json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']
    assert res.status_code == 201
    return new_user

@pytest.fixture
def token(test_user):
    token = create_access_token({'user_id':test_user['id']})
    return token

@pytest.fixture
def authorized_client(client,token):
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token}'
    }
    return client

@pytest.fixture
def test_posts(test_user, session,test_user2):
    session.add_all([
        model.Post(title='first post',content='1st content',owner_id=test_user['id']),
        model.Post(title='second post',content='2nd content',owner_id=test_user['id']),
        model.Post(title='third post',content='3rd content',owner_id=test_user['id']),
        model.Post(title='third post',content='3rd content',owner_id=test_user2['id'])
    ])
    session.commit()
    posts = session.query(model.Post).all()
    return posts

@pytest.fixture
def test_vote(test_user,test_posts,session):
    session.add(model.Vote(post_id=test_posts[0].id,user_id=test_user['id']))
    session.commit()
    vote = session.query(model.Vote).first()
    return vote