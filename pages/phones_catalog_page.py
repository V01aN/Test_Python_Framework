import re

import allure
from playwright.sync_api import Page, Locator, expect
from pytest_playwright.pytest_playwright import page

from pages.phone_page import PhonePage
from utils import parser
from utils.phone_specs import PhoneSpecs


class PhonesCatalogPage:
    def __init__(self, page: Page):
        self.page = page
        self.phone_cart = page.locator('.catalog-form__offers-flex')
        self.phone_price = page.locator('a[href].catalog-form__link_font-weight_bold')
        self.phone_name = page.locator('h3')
        self.phone_main_spec = page.locator('.catalog-form__parameter-part_1')
        self.phone_screen_size = self.phone_main_spec.locator('div').nth(1)
        self.add_to_comparison_button = page.locator('label[title="К сравнению"]')
        self.delete_from_comparison_button = page.locator('label[title="В сравнении"]')
        self.compare_button = page.locator('.catalog-interaction__inner-container_visible')
        self.price_filter_section = page.locator('.catalog-form__group', has_text='Цена')
        self.lowest_price_filter_form = self.price_filter_section.get_by_placeholder('От')
        self.highest_price_filter_form = self.price_filter_section.get_by_placeholder('До')
        self.screen_size_filter_section = page.locator('.catalog-form__group', has_text='Размер экрана')
        self.minimum_screen_size_filter_dropdown = self.screen_size_filter_section.get_by_role('combobox').nth(0)
        self.maximum_screen_size_filter_dropdown = self.screen_size_filter_section.get_by_role('combobox').nth(1)


    def phone_cart_by_num(self, num: int) -> Locator:
        return self.phone_cart.nth(num - 1)

    def phone_name_by_num(self, num: int) -> Locator:
        return self.phone_cart_by_num(num).locator(self.phone_name)

    def phone_spec_by_num(self, num: int) -> Locator:
        return self.phone_cart_by_num(num).locator(self.phone_main_spec)

    def phone_price_by_num(self, num: int) -> Locator:
        return self.phone_cart_by_num(num).locator(self.phone_price)

    def phone_screen_size_by_num(self, num: int) -> Locator:
        return self.phone_cart_by_num(num).locator(self.phone_screen_size)

    def dropdown_option_by_text(self, text: str) -> Locator:
        return self.page.locator('option', has_text=text)


    def get_phone_name_by_num(self, num: int) -> str:
        return self.phone_name_by_num(num).inner_text()

    def get_phone_spec_by_num(self, num: int) -> PhoneSpecs:
        return parser.parse_specs(self.phone_spec_by_num(num).inner_text())

    def get_phone_price_by_num(self, num: int) -> float:
        return parser.parse_price(self.phone_price_by_num(num).inner_text())

    def get_phone_screen_size_by_num(self, num: int) -> float:
        return parser.parse_screen_size(self.phone_screen_size_by_num(num).inner_text())


    @allure.step('Добавить телефон №{num} в сравнение')
    def add_product_to_comparison_by_num(self, num: int):
        (self.phone_cart_by_num(num)
         .locator(self.add_to_comparison_button).click())

    @allure.step('Ввести {price} в нижнюю границу фильтра цены')
    def enter_lowest_price_filter(self, price: str):
        with self.page.expect_response('https://catalog.onliner.by/sdapi/api/catalog.api/seo'):
            self.lowest_price_filter_form.fill(price)

    @allure.step('Ввести {price} в верхнюю границу фильтра цены')
    def enter_highest_price_filter(self, price: str):
        with self.page.expect_response('https://catalog.onliner.by/sdapi/api/catalog.api/seo'):
            self.highest_price_filter_form.fill(price)

    @allure.step('Заполнить фильтр по цене')
    def enter_price_filter(self, first_price: float, second_price: float):
        min_value = min(first_price, second_price)
        max_value = max(first_price, second_price)
        self.enter_lowest_price_filter(parser.format_price(min_value))
        self.enter_highest_price_filter(parser.format_price(max_value))

    @allure.step('Выбрать {screen_size} как нижнюю границу размера экрана')
    def choose_minimum_screen_size_filter(self, screen_size: str):
        with self.page.expect_response('https://catalog.onliner.by/sdapi/api/catalog.api/seo'):
            self.minimum_screen_size_filter_dropdown.click()
            self.minimum_screen_size_filter_dropdown.select_option(label=screen_size)

    @allure.step('Выбрать {screen_size} как верхнюю границу размера экрана')
    def choose_maximum_screen_size_filter(self, screen_size: str):
        with self.page.expect_response('https://catalog.onliner.by/sdapi/api/catalog.api/seo'):
            self.maximum_screen_size_filter_dropdown.click()
            self.maximum_screen_size_filter_dropdown.select_option(screen_size)

    def enter_screen_size_filter(self, first_size: float, second_size: float):
        min_value = min(first_size, second_size)
        max_value = max(first_size, second_size)
        self.choose_minimum_screen_size_filter(parser.format_screen_size(min_value))
        self.choose_maximum_screen_size_filter(parser.format_screen_size(max_value))

    @allure.step('Открыть страницу {name}')
    def open_phone_page_by_name(self, name: str) -> PhonePage:
        self.phone_cart.locator(self.phone_name).filter(has_text=name).click()
        return PhonePage(self.page)


    @allure.step('Проверить наличие флага сравнение у телефона №{num}')
    def assert_comparison_flag_set(self, num: int):
        expect(self.phone_cart_by_num(num)
               .locator(self.delete_from_comparison_button)).to_be_visible()

    @allure.step('Проверить наличие кнопки перехода в сравнение')
    def assert_compare_button_is_visible(self):
        expect(self.compare_button).to_be_visible()

    @allure.step('Проверить, что {name} все ещё отображется после фильтрации')
    def assert_selected_phone_still_marked(self, name: str):
        expect(self.phone_cart.filter(has=self.delete_from_comparison_button).filter(has_text=name)).to_be_visible()
