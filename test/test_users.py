import pytest
from app import schema
from jose import jwt
from app.config import settings


# def test_root(client):
#     res = client.get('/')
#     print(res.json().get('message'))
#     assert(res.json().get('message')=='Welcome to my api!!')

def test_create_user(client):
    res = client.post('/users/',json={"email":"1234@gmail.com","password":'123456'})
    new_user = schema.UserOut(**res.json())
    assert new_user.email=='1234@gmail.com'
    assert res.status_code == 201

def test_login_user(client,test_user):
    res = client.post('/login/',data={"username":test_user['email'],"password":test_user['password']})
    login_res = schema.Token(**res.json())
    payload = jwt.decode(login_res.access_token,settings.secret_key,algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'Bearer'
    assert res.status_code == 200


@pytest.mark.parametrize('email, password, status_code',[
    ("1234@gmail.com",'wrongPassword',403),
    ('wrongEmail@gmail.com','123456',403),
    ('wrongEmail@gmail.com','wrongPassword',403),
    (None,'123456',422),
    ("1234@gmail.com",None,422)
])
def test_incorrect_login(client, test_user,email,password,status_code):
    res = client.post('/login/',data={"username":email,"password":password})
    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid Credential'