import allure
from playwright.sync_api import Page, Locator, expect

class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart_unit = page.locator('.cart-form__offers-unit')

    @allure.step('Проверить наличие товара {name} на странице')
    def assert_cart_has_product_name(self, name: str):
        expect(self.cart_unit).to_contain_text(name, timeout=20_000)