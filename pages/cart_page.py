import allure
from playwright.sync_api import Page, Locator, expect

class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart_unit = page.locator('.cart-form__offers-unit')
        self.clear_cart_button = page.locator('.cart-form__link_nowrap')

    @allure.step('Удалить все товары из корзины, кликнув на кнопку "Удалить N товаров"')
    def clear_cart(self):
        self.clear_cart_button.click()

    @allure.step('Проверить наличие товара {name} в корзине')
    def assert_cart_has_product_name(self, name: str):
        expect(self.cart_unit,
               f'Товар {name} отсутствует в корзине').to_contain_text(name, timeout=20_000)