from pydoc import text

import allure
from playwright.sync_api import Page, Locator, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_nick_auth_button = page.locator('a', has_text='e-mail, нику')
        self.email_nick_box = page.get_by_placeholder('Ник или e-mail')
        self.password_box = page.get_by_placeholder('Пароль')
        self.enter_button = page.get_by_role('button', name='Войти')

    @allure.step('Выбрать авторизацию через e-mail/ник')
    def choose_email_nick_auth(self):
       self.email_nick_auth_button.click()

    @allure.step('Ввести {user} в поле "e-mail/ник"')
    def email_nick_fill(self, user):
        self.email_nick_box.fill(user)

    @allure.step('Ввести {password} в поле "пароль"')
    def password_fill(self, password):
        self.password_box.fill(password)

    @allure.step('Кликнуть на кнопку "Войти"')
    def enter_button_click(self):
        self.enter_button.click()

    @allure.step('Выполнить авторизцию под ником {user}')
    def login_as(self, user: str, password: str):
        self.email_nick_fill(user)
        self.password_fill(password)
        self.enter_button_click()