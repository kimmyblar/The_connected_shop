import re
from playwright.sync_api import Page

# Тестовый комментарий
class SearchResults:
    def __init__(self, page: Page):
        self.page = page
        self.search_bar = page.locator('input[name="q"]')
        self.results_span = page.locator('span.Heading.Text--subdued.u-h7', has_text="results")
        self.no_results_products = page.locator(".Segment__Content p").nth(0)
        self.no_results_journal = page.locator(".Segment__Content p").nth(1)

    def verify_search_bar(self):
        """Verify search bar visibility and placeholder."""
        assert self.search_bar.is_visible()
        assert self.search_bar.get_attribute("placeholder") == "Search..."

    def perform_search(self, search_text: str):
        """Fill the search bar with text and wait for results."""
        self.search_bar.fill(search_text)
        assert self.search_bar.input_value() == search_text
        self.results_span.wait_for()

    def get_results_count(self):
        """Return the number of search results."""
        results_text = self.results_span.inner_text()
        match = re.search(r"(\d+)", results_text) 
        assert match is not None, "No number found in results text"
    
        count = int(match.group(1))
        assert count > 0, f"Expected results count > 0, but got {count}"
    
        return count

    def verify_product_link(self, product_name: str):
        """Verify a product link is visible and matches the expected text."""
        product_link = self.page.locator(f'a[href*="/products/wireless-label-printer"]', has_text=product_name)
        product_link.wait_for()
        assert product_link.is_visible()
        assert product_link.inner_text() == product_name

    def verify_no_results(self):
        """Verify no results messages are displayed."""
        self.no_results_products.wait_for()
        assert self.no_results_products.is_visible()
        self.no_results_journal.wait_for()
        assert self.no_results_journal.is_visible()