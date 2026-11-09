import allure
from playwright.sync_api import Page, Locator, expect

from utils.phone_specs import PhoneSpecs


class ComparisonPage:
    def __init__(self, page: Page):
        self.page = page
        self.table_top_header = page.locator('#product-table tbody .product-table__row_top')
        self.header_product_name = self.table_top_header.locator('.product-summary')
        self.table_row = page.locator('tr.product-table__row_parameter')
        self.table_row_content = page.locator('span.value__text')

    def table_row_by_name(self, name: str) -> Locator:
        return self.table_row.filter(has_text=name)

    def table_row_content_by_num(self, content: str, num: int) -> Locator:
        return self.table_row_by_name(content).locator(self.table_row_content).nth(num - 1)

    def header_product_name_by_text(self, text: str) -> Locator:
        return self.header_product_name.filter(has_text=text)


    def get_phone_name_by_num(self, num: int) -> str:
        return self.header_product_name.nth(num - 1).inner_text()

    def get_table_row_content_by_num(self, content: str, num: int) -> str:
        return self.table_row_content_by_num(content, num).inner_text().strip()


    @allure.step('Открыть страницу телефона {name}')
    def open_phone_page_by_name(self, name: str):
        self.header_product_name_by_text(name).click()


    @allure.step('Проверить, что в сравнении находятся разные телефоны')
    def assert_there_are_different_phones(self):
        assert self.get_phone_name_by_num(1) != self.get_phone_name_by_num(2)

    @allure.step('Сверить ОС {os} с отображаемым текстом')
    def assert_phone_os(self, os: str, num: int):
        assert self.get_table_row_content_by_num('Операционная система', num) == os

    @allure.step('Сверить размер экрана {diagonal} с отображаемым текстом')
    def assert_phone_diagonal(self, diagonal: str, num: int):
        assert self.get_table_row_content_by_num('Размер экрана', num) == diagonal

    @allure.step('Сверить разрешение экрана {resolution} с отображаемым текстом')
    def assert_phone_resolution(self, resolution: str, num: int):
        assert self.get_table_row_content_by_num('Разрешение экрана', num) == resolution

    @allure.step('Сверить объем ОЗУ {ram} с отображаемым текстом')
    def assert_phone_ram(self, ram: str, num: int):
        assert self.get_table_row_content_by_num('Объем оперативной памяти', num) == ram

    @allure.step('Сверить параметры спецификации из каталога с отображаемым текстом телефона №{num}')
    def assert_specs_against_catalog(self, phone_specs: PhoneSpecs, num: int):
        self.assert_phone_os(phone_specs.os, num)
        self.assert_phone_diagonal(phone_specs.diagonal_str, num)
        self.assert_phone_resolution(phone_specs.resolution, num)
        self.assert_phone_ram(phone_specs.ram_str, num)