def test_unauthorized_user_vote(client,test_posts):
    data = {'post_id':test_posts[0].id,'dir':1}
    res = client.post('/vote/',json=data)
    assert res.status_code == 401

def test_vote_post_not_exist(authorized_client):
    data = {'post_id':8888,'dir':1}
    res = authorized_client.post('/vote/',json=data)
    assert res.status_code == 404

def test_vote_post_had_voted(authorized_client,test_user,test_vote):
    data = {'post_id':test_vote.post_id,'dir':1}
    res = authorized_client.post('/vote/',json=data)
    assert res.status_code == 409
    assert res.json().get('detail') == f"user {test_user['id']} has voted post {test_vote.post_id}"

def test_vote_successfully(authorized_client,test_posts):
    data = {'post_id':test_posts[0].id,'dir':1}
    res = authorized_client.post('/vote/',json=data)
    assert res.status_code == 201
    assert res.json().get('message') == 'Successfully voted'

def test_unvote_not_voted_post(authorized_client,test_posts):
    data = {'post_id':test_posts[0].id,'dir':0}
    res = authorized_client.post('/vote/',json=data)
    assert res.status_code == 404
    assert res.json().get('detail') == f'post {test_posts[0].id} has not been voted'

def test_unvote_successfully(authorized_client,test_vote):
    data = {'post_id':test_vote.post_id,'dir':0}
    res = authorized_client.post('/vote/',json=data)
    assert res.status_code == 201
    assert res.json().get('message') == 'Successfully unvoted'