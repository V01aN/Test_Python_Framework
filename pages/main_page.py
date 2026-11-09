import allure
from playwright.sync_api import Page, Locator, expect

class MainPage:
    def __init__(self, page: Page):
        self.page = page
        self.login_button = page.locator('a', has_text='Вход')
        self.user_context_button = page.locator('div.b-top-profile__image')
        self.user_context_menu = page.locator('div.b-top-profile__dropdown_user')
        self.phones_catalog_button = page.get_by_role('link', name='Мобильные телефоны')

    def get_url(self) -> str:
        return self.page.url

    @allure.step('Открыть страницу авторизации')
    def open_login_page(self):
        self.login_button.click()

    @allure.step('Открыть контекстное меню пользователя')
    def open_user_context(self):
        self.user_context_button.click()

    @allure.step('Открыть каталог "Мобильные телефоны"')
    def open_phones_catalog_page(self):
        self.phones_catalog_button.click()
        self.page.wait_for_load_state('networkidle')

    @allure.step('Проверить нахождение на сайте: {expected_url}')
    def assert_page_url(self, expected_url: str):
        assert expected_url == self.get_url()

    @allure.step('Проверить успешную авторизацию, путем проверки логина в контекстном меню')
    def assert_user_context_has_login(self, expected_login: str):
        expect(self.user_context_menu).to_contain_text(expected_login)