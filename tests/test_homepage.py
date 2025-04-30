from email import header
import pytest
from playwright.sync_api import sync_playwright
from pages.homepage import Homepage
from pages.header import Header
from tests.pages.searchresults import SearchResults

# from pages.search_results import SearchResults


@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture
def homepage(browser):
    page = browser.new_page()
    homepage = Homepage(page)
    header = Header(page)
    search = SearchResults(page)

    homepage.navigate()
    yield homepage
    page.close()


@pytest.fixture
def search_results(homepage):
    homepage.header.open_search()
    return SearchResults(homepage.page)


def test_homepage_title_and_url(homepage):
    assert homepage.get_title() == "The Connected Shop - Smart Locks, Smart Sensors, Smart Home & Office"
    assert homepage.get_url() == "https://theconnectedshop.com/"


def test_header_ui_elements(homepage):
    header.verify_logo_link()
    header.verify_primary_logo()
    header.verify_transparent_logo()
    header.verify_account_link()
    header.verify_search_link()
    header.verify_cart_link()
    assert header.get_cart_count() == "0"


def test_search_functionality(search_results):
    search_results.verify_search_bar()
    search_text = "WIRELESS LABEL PRINTER"
    search_results.perform_search(search_text)
    assert search_results.get_results_count() > 0
    search_results.verify_product_link(search_text)


def test_search_negative_invalid_input(search_results):
    search_text = "12345678"
    search_results.perform_search(search_text)
    search_results.verify_no_results()


def test_search_negative_spaces(search_results):
    search_text = "  "
    search_results.perform_search(search_text)
    search_results.page.wait_for_timeout(4000)
    search_results.verify_no_results()