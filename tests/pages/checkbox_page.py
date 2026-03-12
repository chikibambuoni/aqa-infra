class CheckboxPage:
    URL = 'https://the-internet.herokuapp.com/checkboxes'
    CHECKBOX = 'input[type="checkbox"]'

    def __init__(self, page):
        self.page = page


    def open(self):
        self.page.goto(self.URL)


    def check(self, index):
        self.page.locator(self.CHECKBOX).nth(index).check()


    def uncheck(self, index):
        self.page.locator(self.CHECKBOX).nth(index).uncheck()


    def is_checked(self, index):
        return self.page.locator(self.CHECKBOX).nth(index).is_checked()
