import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

def test_search_functionality(browser):
    page = browser.new_page()
    page.goto("https://theconnectedshop.com/")

link_search = page.locator('a.Heading.Link.Link--primary.Text--subdued.u-h8:has-text("Search")').nth(0)
assert link_search.is_visible()
assert link_search.get_attribute("href") == "/search"
link_search.click()
search_bar = page.locator('input["name=q"]')
assert search_bar.is_visible()
assert search_bar.get_attribute("placeholder") == "Search..."
search_text = "industrial"
search_bar.fill(search_text)
assert search_bar.input_value() == search_text