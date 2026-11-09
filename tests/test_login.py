import allure
import pytest

from playwright.sync_api import Page, expect
from pages.main_page import MainPage
from pages.login_page import LoginPage
from config.test_config import get_base_url, get_login, get_password

pytestmark = [allure.epic('Onliner UI Tests'), allure.feature('Авторизация')]

@pytest.fixture
def main_page(page: Page) -> MainPage:
    page.goto(get_base_url())
    return MainPage(page)

@allure.title('OL-01: После авторизации появляется контектное меню пользователя')
def test_successful_login(main_page: MainPage):
    main_page.open_login_page()

    login_page = LoginPage(main_page.page)
    login_page.choose_email_nick_auth()
    login_page.login_as(get_login(), get_password())

    main_page = MainPage(login_page.page)
    main_page.assert_user_context_has_login(get_login())