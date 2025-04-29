import pytest
import re
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

    search_bar = page.locator('input[name="q"]')
    assert search_bar.is_visible()
    assert search_bar.get_attribute("placeholder") == "Search..."

    search_text = "WIRELESS LABEL PRINTER"
    search_bar.fill(search_text)
    assert search_bar.input_value() == search_text

    results_span = page.locator('span.Heading.Text--subdued.u-h7', has_text="results")
    results_span.wait_for()  
    assert results_span.is_visible()

    results_text = results_span.inner_text()
    print("Результаты поиска:", results_text)

    match = re.search(r"(\d+)", results_text)
    assert match is not None, "Не найдено число в строке результатов"

    results_count = int(match.group(1))
    assert results_count > 0, f"Ожидалось больше 0 результатов, но найдено: {results_count}"

    product_link = page.locator('a[href*="/products/wireless-label-printer"]', has_text="Wireless Label Printer")
    product_link.wait_for()
    assert product_link.is_visible()
    link_text = product_link.inner_text()
    assert link_text == search_text

 # Прописываем негативные тесты

    search_errtext = ("12345678")
    search_bar.fill(search_errtext)
    assert search_bar.input_value() == search_errtext

    no_results_products = page.locator(".Segment__Content p").nth(0)
    no_results_products.wait_for()
    assert no_results_products.is_visible()

    no_results_journal = page.locator(".Segment__Content p").nth(1)
    no_results_journal.wait_for()
    assert no_results_journal.is_visible()

 #Вписываем пробелы, здесь тест должен упасть и это нормально!!! Так как почему то на тестовом сайте поиск 
 # с пробелами все равно работает

    search_empty = ("  ")
    search_bar.fill(search_empty)
    assert search_bar.input_value() == search_empty
    page.wait_for_timeout(4000)

    no_results_products = page.locator(".Segment__Content p").nth(0)
    no_results_products.wait_for()
    assert no_results_products.is_visible()

    no_results_journal = page.locator(".Segment__Content p").nth(1)
    no_results_journal.wait_for()
    assert no_results_journal.is_visible()







