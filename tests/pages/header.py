from playwright.sync_api import Page


class Header:
    def __init__(self, page: Page):
        self.page = page
        self.logo_link = page.locator("a.Header__LogoLink")
        self.primary_logo = page.locator("img.Header__LogoImage--primary")
        self.transparent_logo = page.locator("img.Header__LogoImage--transparent")
        self.account_link = page.locator('a.Heading.Link.Link--primary.Text--subdued.u-h8:has-text("Account")').nth(0)
        self.search_link = page.locator('a.Heading.Link.Link--primary.Text--subdued.u-h8:has-text("Search")').nth(0)
        self.cart_link = page.locator('a.Heading.u-h6[aria-label="Open cart"]')
        self.cart_count = self.cart_link.locator('span.Header__CartCount')

    def verify_logo_link(self):
        """Verify logo link visibility and href."""
        assert self.logo_link.is_visible()
        assert self.logo_link.get_attribute("href") == "/"

    def verify_primary_logo(self):
        """Verify primary logo attributes."""
        assert self.primary_logo.is_visible()
        assert self.primary_logo.get_attribute("width") == "250"
        assert self.primary_logo.get_attribute("height") == "75px"
        assert self.primary_logo.get_attribute("alt") == "The Connected Shop Logo"
        assert self.primary_logo.get_attribute("src") == "//theconnectedshop.com/cdn/shop/files/The_Connected_Shop_250x.png?v=1705959137"

    def verify_transparent_logo(self):
        """Verify transparent logo attributes."""
        assert self.transparent_logo.is_visible()
        assert self.transparent_logo.get_attribute("width") == "250"
        assert self.transparent_logo.get_attribute("height") == "75px"
        assert self.transparent_logo.get_attribute("alt") == "The Connected Shop Logo White"
        assert self.transparent_logo.get_attribute("src") == "//theconnectedshop.com/cdn/shop/files/The_Connected_Shop_logo_250x.png?v=1705959163"

    def verify_account_link(self):
        """Verify account link visibility and href."""
        assert self.account_link.is_visible()
        assert self.account_link.get_attribute("href") == "/account"

    def verify_search_link(self):
        """Verify search link visibility and href."""
        assert self.search_link.is_visible()
        assert self.search_link.get_attribute("href") == "/search"

    def verify_cart_link(self):
        """Verify cart link attributes."""
        assert self.cart_link.is_visible()
        assert self.cart_link.get_attribute("href") == "/cart"
        assert self.cart_link.get_attribute("data-action") == "open-drawer"
        assert self.cart_link.get_attribute("data-drawer-id") == "sidebar-cart"
        assert self.cart_link.get_attribute("aria-label") == "Open cart"

    def get_cart_count(self):
        """Return the cart item count."""
        return self.cart_count.inner_text().strip()

    def open_search(self):
        """Click the search link to open the search bar."""
        self.search_link.click()