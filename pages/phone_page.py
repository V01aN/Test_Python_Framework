import allure
from playwright.sync_api import Page, Locator, expect

from pages.cart_page import CartPage
from pages.comparison_page import ComparisonPage
from utils.phone_specs import PhoneSpecs


class PhonePage:
    def __init__(self, page: Page):
        self.page = page
        self.phone_spec = page.locator('.offers-description__specs')
        self.compare_button = page.locator('a.catalog-interaction__sub_main')
        self.add_to_cart = page.locator('.bbx__itm .cbx a.but_sm', has_text='Купить')
        self.go_to_cart_button = page.get_by_text('Перейти в корзину')

    @allure.step('Открыть страницу сравнения товаров')
    def open_comparison_page(self) -> ComparisonPage:
        self.compare_button.click()
        return ComparisonPage(self.page)

    @allure.step('Добавить товар в корзину')
    def add_product_to_cart(self):
        self.add_to_cart.first.click()

    @allure.step('Перейти в корзину')
    def go_to_cart(self) -> CartPage:
        self.go_to_cart_button.click()
        return CartPage(self.page)

    @allure.step('Найти ОС {os} в отображаемой спецификации')
    def assert_phone_os(self, os: str):
        expect(self.phone_spec).to_contain_text(os)

    @allure.step('Найти диагональ {diagonal} в отображаемой спецификации')
    def assert_phone_diagonal(self, diagonal: str):
        expect(self.phone_spec).to_contain_text(diagonal)

    @allure.step('Найти разрешение {resolution} в отображаемой спецификации')
    def assert_phone_resolution(self, resolution: str):
        expect(self.phone_spec).to_contain_text(resolution)

    @allure.step('Найти объем ОЗУ {ram} в отображаемой спецификации')
    def assert_phone_ram(self, ram: str):
        expect(self.phone_spec).to_contain_text(ram)

    @allure.step('Проверить наличие параметров спецификации из каталога на странице телефона')
    def assert_specs_against_catalog(self, catalog_spec: PhoneSpecs):
        self.assert_phone_os(catalog_spec.os)
        self.assert_phone_diagonal(catalog_spec.diagonal_str)
        self.assert_phone_resolution(catalog_spec.resolution)
        self.assert_phone_ram(catalog_spec.ram_str)