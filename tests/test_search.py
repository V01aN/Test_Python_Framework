import allure
import pytest

from playwright.sync_api import Page, expect
from pages.search_page import SearchPage
from pages.main_page import MainPage
from config.test_config import get_base_url

pytestmark = [allure.epic('Duckduckgo UI Tests'), allure.feature('Поиск')]

@pytest.fixture
def search_page(page: Page) -> SearchPage:
    return SearchPage(page)

@pytest.fixture
def results_page(search_page: SearchPage) -> SearchPage:
    search_page.open()
    search_page.search_content('Onliner')
    return search_page

@allure.title('DDG-01: Результат поиска отображается на странице')
def test_onliner_find_search(search_page: SearchPage):
    search_page.open()
    search_page.search_content('Onliner')
    search_page.assert_search_result('onliner.by - Onlíner')

@allure.title('DDG-02: Результат поиска открывается')
def test_onliner_page_opened(results_page: SearchPage):
    results_page.open_result_by_text('onliner.by - Onlíner')

    main_page = MainPage(results_page.page)
    main_page.assert_page_url(get_base_url())