import pytest
from app import schema

# def test_get_all_posts(authorized_client,test_posts):
#     res = authorized_client.get('/posts/')
#     def validation(post):
#         return schema.PostOut(**post)
#     post_map = map(validation,res.json())
#     assert len(res.json())==len(test_posts)
#     assert res.status_code == 200

# def test_unauthorized_user_get_posts(client,test_posts):
#     res = client.get('/posts/')
#     assert res.status_code == 401

# def test_unauthorized_user_get_one_posts(client,test_posts):
#     res = client.get(f'/posts/{test_posts[0].id}')
#     assert res.status_code == 401

# def test_get_one_posts_not_exist(authorized_client,test_posts):
#     res = authorized_client.get('/posts/8888')
#     assert res.status_code == 404

# def test_get_one_posts(authorized_client,test_posts):
#     res = authorized_client.get(f'/posts/{test_posts[0].id}')
#     post = schema.PostOut(**res.json())
#     assert res.status_code == 200
#     assert post.Post.id == test_posts[0].id

# @pytest.mark.parametrize('title,content,published',[
#     ('test1','content1',True),
#     ('test2','content2',False)
# ])
# def test_create_post(authorized_client,test_user,title,content,published):
#     res = authorized_client.post('/posts/',json={'title':title,'content':content,'published':published})
#     post = schema.Post(**res.json())
#     assert post.title == title
#     assert post.content == content
#     assert post.published == published
#     assert post.owner_id == test_user['id']

# def test_unauthorized_user_delete_post(client,test_user,test_posts):
#     res = client.delete(f'/posts/{test_posts[0].id}')
#     assert res.status_code == 401

# def test_delete_post(authorized_client,test_posts,test_user):
#     res = authorized_client.delete(f'/posts/{test_posts[0].id}')
#     assert res.status_code == 204

# def test_delete_post_not_exist(authorized_client,test_posts,test_user):
#     res = authorized_client.delete('/posts/8888')
#     assert res.status_code == 404

# def test_wrongUser_delete_post(authorized_client,test_posts):
#     res = authorized_client.delete(f'/posts/{test_posts[-1].id}')
#     assert res.status_code == 403
#     assert res.json().get('detail') == 'Not authorized to perform requested action'

def test_unauthorized_user_update_post(client,test_posts,test_user):
    data = {'title':'updated title','content':'updated content'}
    res = client.put(f'/posts/{test_posts[0].id}', json=data)
    assert res.status_code == 401

def test_update_post_not_exist(authorized_client,test_posts,test_user):
    data = {'title':'updated title','content':'updated content'}
    res = authorized_client.put('/posts/8888', json=data)
    assert res.status_code == 404

def test_update_post(authorized_client,test_posts,test_user):
    data = {'title':'updated title','content':'updated content'}
    res = authorized_client.put(f'/posts/{test_posts[0].id}', json=data)
    updated_post = schema.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert updated_post.id == test_posts[0].id
    assert updated_post.owner_id == test_user['id']

def test_update_another_user_post(authorized_client,test_posts,test_user2):
    data = {'title':'updated title','content':'updated content'}
    res = authorized_client.put(f'/posts/{test_posts[-1].id}', json=data)
    assert res.status_code == 403

