import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

def test_connected_shop_title_and_url(browser):
    page = browser.new_page()
    page.goto("https://theconnectedshop.com/")

    assert page.title() == "The Connected Shop - Smart Locks, Smart Sensors, Smart Home & Office"
    assert page.url == "https://theconnectedshop.com/"

    logo_link = page.locator("a.Header__LogoLink")
    assert logo_link.is_visible()
    assert logo_link.get_attribute("href") == "/" 

    primary_logo = page.locator("img.Header__LogoImage--primary")
    assert primary_logo.is_visible()
    assert primary_logo.get_attribute("width") == "250"
    assert primary_logo.get_attribute("height") =="75px"
    assert primary_logo.get_attribute("alt") == "The Connected Shop Logo"
    assert primary_logo.get_attribute("src") == "//theconnectedshop.com/cdn/shop/files/The_Connected_Shop_250x.png?v=1705959137"

    transparent_logo = page.locator("img.Header__LogoImage--transparent")
    assert transparent_logo.is_visible()
    assert transparent_logo.get_attribute("width") == "250"
    assert transparent_logo.get_attribute("height") =="75px"
    assert transparent_logo.get_attribute("height") =="75px"
    assert transparent_logo.get_attribute("alt") == "The Connected Shop Logo White"
    assert transparent_logo.get_attribute("src") == "//theconnectedshop.com/cdn/shop/files/The_Connected_Shop_logo_250x.png?v=1705959163"

    account_link = page.locator('a.Heading.Link.Link--primary.Text--subdued.u-h8:has-text("Account")').nth(0)
    assert account_link.is_visible()
    assert account_link.get_attribute("href") == "/account"

    link_search = page.locator('a.Heading.Link.Link--primary.Text--subdued.u-h8:has-text("Search")').nth(0)
    assert link_search.is_visible()
    assert link_search.get_attribute("href") == "/search"

    link_cart = page.locator('a.Heading.u-h6[aria-label="Open cart"]')
    assert link_cart.is_visible()
    assert link_cart.get_attribute("href") == "/cart"
    assert link_cart.get_attribute("data-action") == "open-drawer"
    assert link_cart.get_attribute("data-drawer-id") == "sidebar-cart"
    assert link_cart.get_attribute("aria-label") == "Open cart"

    cart_count = link_cart.locator('span.Header__CartCount')
    assert cart_count.inner_text().strip() == "0"
    
    page.close()