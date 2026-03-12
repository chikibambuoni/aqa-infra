class LoginPage:
    USERNAME = '#username'
    PASSWORD = '#password'
    SUBMIT = 'button[type="submit"]'

    def __init__(self, page):
        self.page = page


    def open(self):
        self.page.goto('https://the-internet.herokuapp.com/login')


    def login(self, username, password):
        self.page.fill(self.USERNAME, username)
        self.page.fill(self.PASSWORD, password)
        self.page.click(self.SUBMIT)
