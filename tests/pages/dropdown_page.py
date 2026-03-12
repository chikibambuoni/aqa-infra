class DropdownPage:
    URL = 'https://the-internet.herokuapp.com/dropdown'
    DROPDOWN = '#dropdown'

    def __init__(self, page):
        self.page = page


    def open(self):
        self.page.goto(self.URL)


    def select_option(self, value):
        self.page.select_option(self.DROPDOWN, value)
    

    def get_selected_value(self):
        return self.page.locator(self.DROPDOWN).input_value()
