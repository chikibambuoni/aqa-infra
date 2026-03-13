import pytest
from playwright.sync_api import sync_playwright, Page
from tests.pages.checkbox_page import CheckboxPage
from tests.pages.login_page import LoginPage
from tests.pages.secure_page import SecurePage
from tests.pages.dropdown_page import DropdownPage

@pytest.fixture(scope='module')
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page()
        yield pg
        browser.close()


def test_successful_login(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login('tomsmith', 'SuperSecretPassword!')
    secure_page = SecurePage(page)
    assert secure_page.is_loaded()


def test_logout(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login('tomsmith', 'SuperSecretPassword!')
    secure_page = SecurePage(page)
    secure_page.logout()
    assert page.url == 'https://the-internet.herokuapp.com/login'


def test_dropdown_select_option_1(page: Page):
    dropdown_page = DropdownPage(page)
    dropdown_page.open()
    dropdown_page.select_option('1')
    assert dropdown_page.get_selected_value() == '1'


def test_dropdown_select_option_2(page: Page):
    dropdown_page = DropdownPage(page)
    dropdown_page.open()
    dropdown_page.select_option('2')
    assert dropdown_page.get_selected_value() == '2'


def test_checkbox_check(page: Page):
    checkbox_page = CheckboxPage(page)
    checkbox_page.open()
    checkbox_page.check(0)
    assert checkbox_page.is_checked(0)


def test_checkbox_uncheck(page: Page):
    checkbox_page = CheckboxPage(page)
    checkbox_page.open()
    checkbox_page.uncheck(1)
    assert not checkbox_page.is_checked(1)


