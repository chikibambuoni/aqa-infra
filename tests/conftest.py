import allure
import pytest
import requests
from playwright.sync_api import sync_playwright

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


@pytest.fixture(scope='module')
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page()
        yield pg
        browser.close()


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page):
    yield
    if request.node.rep_call.failed:
        screenshot = page.screenshot()
        allure.attach(screenshot, name='screenshot', attachment_type=allure.attachment_type.PNG)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f'rep_{rep.when}', rep)
