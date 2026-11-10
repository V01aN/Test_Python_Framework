import allure
import pytest

from playwright.sync_api import Page, expect

from pages.phones_catalog_page import PhonesCatalogPage
from pages.main_page import MainPage

pytestmark = [allure.epic('Onliner UI Tests'),
              allure.feature('Добавление в корзину', 'Сравнение товаров', 'Фильтрация')]

@pytest.fixture
def phones_catalog_page(logged_in_page: Page) -> PhonesCatalogPage:
    MainPage(logged_in_page).open_phones_catalog_page()
    return PhonesCatalogPage(logged_in_page)

@allure.title('OB-01: Фильтрация, сравние и добавление в корзину двух телефонов')
def test_buy_phone(phones_catalog_page: PhonesCatalogPage):
    phones_catalog_page.add_product_to_comparison_by_num(1)
    phones_catalog_page.add_product_to_comparison_by_num(5)

    first_screen = phones_catalog_page.get_phone_screen_size_by_num(1)
    second_screen = phones_catalog_page.get_phone_screen_size_by_num(5)

    first_price = phones_catalog_page.get_phone_price_by_num(1)
    second_price = phones_catalog_page.get_phone_price_by_num(5)

    first_name = phones_catalog_page.get_phone_name_by_num(1)
    second_name = phones_catalog_page.get_phone_name_by_num(5)

    first_spec = phones_catalog_page.get_phone_spec_by_num(1)
    second_spec = phones_catalog_page.get_phone_spec_by_num(5)

    phones_catalog_page.assert_comparison_flag_set(1)
    phones_catalog_page.assert_comparison_flag_set(5)
    phones_catalog_page.assert_compare_button_is_visible()

    phones_catalog_page.enter_price_filter(first_price, second_price)

    phones_catalog_page.enter_screen_size_filter(first_screen, second_screen)

    phones_catalog_page.assert_selected_phone_still_marked(first_name)
    phones_catalog_page.assert_selected_phone_still_marked(second_name)

    phone_page = phones_catalog_page.open_phone_page_by_name(first_name)

    phone_page.assert_specs_against_catalog(first_spec)

    comparison_page = phone_page.open_comparison_page()
    comparison_page.assert_there_are_different_phones()

    comparison_page.assert_specs_against_catalog(first_spec, 2)
    comparison_page.assert_specs_against_catalog(second_spec, 1)

    comparison_page.open_phone_page_by_name(first_name)

    phone_page.add_product_to_cart()
    cart_page = phone_page.go_to_cart()
    cart_page.assert_cart_has_product_name(first_name)
    cart_page.clear_cart()