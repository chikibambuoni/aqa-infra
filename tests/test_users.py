import pytest
import requests

from config import BASE_URL

def test_status_code(user):
    assert user.status_code == 200


def test_user_id(user):
    assert user.json()['id'] == 1


def test_user_has_email(user):
    assert 'email' in user.json()


def test_missing_user(missing_user):
    assert missing_user.status_code == 404


def test_posts():
    response = requests.get(f'{BASE_URL}/posts?userId=1')
    assert all(post['userId'] == 1 for post in response.json())


@pytest.mark.parametrize('user_id', [1, 2, 3])
def test_multiple_users(user_id):
    response = requests.get(f'{BASE_URL}/users/{user_id}')
    assert response.status_code == 200
    assert response.json()['id'] == user_id


def test_create_post(created_post):
    assert created_post.status_code == 201
    assert created_post.json()['title'] == 'The Post'
    assert created_post.json()['userId'] == 1


def test_create_post_response_shape(created_post):
    assert all(k in created_post.json() for k in ['title', 'body', 'userId', 'id']) 


def test_delete_post():
    response = requests.delete(f'{BASE_URL}/posts/1')
    assert response.status_code == 200


def test_delete_nonexistent_post():
    response = requests.delete(f'{BASE_URL}/posts/9999')
    assert response.status_code == 200


def test_update_post():
    updated_post = {
            'title': 'Updated Title',
            'body': 'Updated body',
            'userId': 1
    }
    response = requests.put(f'{BASE_URL}/posts/1', json=updated_post)
    assert response.status_code == 200
    assert response.json()['title'] == 'Updated Title'


def test_patch_post():
    patched_post = {'title': 'Patched Title'}
    response = requests.patch(f'{BASE_URL}/posts/1', json=patched_post)
    assert response.status_code == 200
    assert response.json()['title'] == 'Patched Title'


def test_user_response_time(user):
    assert user.elapsed.total_seconds() < 1.0


def test_response_content_type(user):
    assert user.headers['Content-Type'] == 'application/json; charset=utf-8'


def test_response_server_header(user):
    assert 'Express' in user.headers['x-powered-by']
