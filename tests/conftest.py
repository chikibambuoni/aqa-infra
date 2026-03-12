import pytest
import requests

from config import BASE_URL

@pytest.fixture(scope='module')
def user():
    response = requests.get(f'{BASE_URL}/users/1')
    return response


@pytest.fixture(scope='module')
def missing_user():
    response = requests.get(f'{BASE_URL}/users/9999')
    return response


@pytest.fixture(scope='module')
def created_post():
    new_post = {
            'title': 'The Post',
            'body': 'This is a test',
            'userId': 1
    }
    response = requests.post(f'{BASE_URL}/posts', json=new_post)
    return response


from playwright.sync_api import sync_playwright

@pytest.fixture(scope='module')
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page()
        yield pg
        browser.close()
