class SecurePage:
    LOGOUT = 'a[href="/logout"]'

    def __init__(self, page):
        self.page = page


    def is_loaded(self):
        return self.page.url == 'https://the-internet.herokuapp.com/secure'


    def logout(self):
        self.page.click(self.LOGOUT)
