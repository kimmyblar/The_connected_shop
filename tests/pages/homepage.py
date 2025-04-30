from playwright.sync_api import Page
from config.config import BASE_URL


class Homepage:
    def __init__(self, page: Page):
        self.page = page


    def navigate(self):
        """Navigate to the homepage."""
        self.page.goto(BASE_URL)

    def get_title(self):
        """Return the page title."""
        return self.page.title()

    def get_url(self):
        """Return the current URL."""
        return self.page.url