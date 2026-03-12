import pytest
import requests

from config import BASE_URL


@pytest.fixture(scope='module')
def post():
    response = requests.get(f'{BASE_URL}/posts/1')
    return response


def test_post_fetching(post):
    assert post.status_code == 200


def test_post_has_all_fields(post):
    assert all(el in post.json() for el in ['userId', 'id', 'title', 'body'])


def test_post_response_time(post):
    assert post.elapsed.total_seconds() < 1


def test_post_content_type(post):
    assert post.headers['Content-Type'] == 'application/json; charset=utf-8'


def test_nonexistent_post():
    response = requests.get(f'{BASE_URL}/posts/9999')
    assert response.status_code == 404


@pytest.mark.parametrize('postId', [1, 5, 10])
def test_multiple_posts_fetching(postId):
    response = requests.get(f'{BASE_URL}/posts/{postId}')
    assert response.status_code == 200


@pytest.mark.skip(reason="JSONPlaceholder doesn't persist created resources")
def test_created_post_is_fetchable(created_post):
    post_id = created_post.json()['id']
    response = requests.get(f'{BASE_URL}/posts/{post_id}')
    assert response.status_code == 200 and response.json()['title'] == 'The Post'


def test_filter_posts_by_user():
    response = requests.get(f'{BASE_URL}/posts', params={'userId':2})
    assert all(post['userId'] == 2 for post in response.json())


def test_post_field_types(post):
    data = post.json()
    expected_types = {'id': int,
                      'userId': int,
                      'title': str,
                      'body': str
    }
    assert all(isinstance(data[field], expected_types[field]) for field in expected_types)


def test_posts_list():
    response = requests.get(f'{BASE_URL}/posts')
    data = response.json()
    assert isinstance(data, list)
    assert 0 < len(data) == 100


def test_filter_posts_by_nonexistent_user():
    response = requests.get(f'{BASE_URL}/posts', params={'userId':9999})
    assert response.status_code == 200 and response.json() == []
