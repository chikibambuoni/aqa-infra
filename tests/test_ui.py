import pytest
from playwright.sync_api import Page, sync_playwright

def login(page):
    page.goto('https://the-internet.herokuapp.com/login')
    page.fill('#username', 'tomsmith')
    page.fill('#password', 'SuperSecretPassword!')
    page.click('button[type="submit"]')


def test_browser_opens(page: Page):
    page.goto('https://example.com')
    assert page.title() == 'Example Domain'


def test_login_page_loads(page: Page):
    page.goto('https://the-internet.herokuapp.com/login')
    assert page.title() == 'The Internet'


def test_succesful_login(page: Page):
    login(page)
    assert page.url == 'https://the-internet.herokuapp.com/secure'


def test_failed_login(page: Page):
    page.goto('https://the-internet.herokuapp.com/login')
    page.fill('#username', 'nonexistent_user')
    page.fill('#password', 'SuperSecretPassword!')
    page.click('button[type="submit"]')
    assert page.locator('text=Your username is invalid!').is_visible()


def test_login_redirect_wait(page: Page):
    login(page)
    page.wait_for_url('https://the-internet.herokuapp.com/secure')
    assert 'secure' in page.url


def test_logout_button_appears(page: Page):
    login(page)
    page.wait_for_selector('a[href="/logout"]')
    assert page.locator('a[href="/logout"]').is_visible()


def test_page_fully_loaded(page: Page):
    page.goto('https://the-internet.herokuapp.com')
    page.wait_for_load_state('networkidle')
    assert page.title() == 'The Internet'


def test_full_login_flow(page: Page):
    login(page)
    page.wait_for_url('https://the-internet.herokuapp.com/secure')
    page.wait_for_selector('a[href="/logout"]')
    assert page.locator('a[href="/logout"]').is_visible()


def test_dropdown_select_option_1(page: Page):
    page.goto('https://the-internet.herokuapp.com/dropdown')
    page.select_option('#dropdown', '1')
    assert page.locator('#dropdown').input_value() == '1'


def test_dropdown_select_option_2(page: Page):
    page.goto('https://the-internet.herokuapp.com/dropdown')
    page.select_option('#dropdown', '2')
    assert page.locator('#dropdown').input_value() == '2'


def test_checkbox_check(page: Page):
    page.goto('https://the-internet.herokuapp.com/checkboxes')
    page.locator('input[type="checkbox"]').nth(0).check()
    assert page.locator('input[type="checkbox"]').nth(0).is_checked()


def test_checkbox_uncheck(page: Page):
    page.goto('https://the-internet.herokuapp.com/checkboxes')
    page.locator('input[type="checkbox"]').nth(1).uncheck()
    assert not page.locator('input[type="checkbox"]').nth(1).is_checked()


def test_file_upload(page: Page):
    page.goto('https://the-internet.herokuapp.com/upload')
    page.set_input_files('input[type="file"]', '/app/test_upload.txt')
    page.click('#file-submit')
    assert page.locator('text=File Uploaded').is_visible()


def test_file_upload_shows_filename(page: Page):
    page.goto('https://the-internet.herokuapp.com/upload')
    page.set_input_files('input[type="file"]', '/app/test_upload.txt')
    page.click('#file-submit')
    assert page.locator('text=test_upload.txt').is_visible()


@pytest.mark.skip(reason='TinyMCE loads readonly in headless Chromium')
def test_iframe_input(page: Page):
    page.goto('https://the-internet.herokuapp.com/iframe')
    page.wait_for_load_state('networkidle')
    frame = page.frame_locator('#mce_0_ifr')
    frame.locator('body#tinymce').fill('new text')
    assert 'new text' in frame.locator('body#tinymce').inner_text()
