from typing import Any, Generator

import pytest
from playwright.sync_api import Page
from pages.main_page import MainPage
from pages.login_page import LoginPage
from config.test_config import get_base_url, get_login, get_password


CLEAN_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "channel": "chromium",
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
        ],
    }

@pytest.fixture
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "user_agent": CLEAN_UA,
        "locale": "ru-RU",
        "timezone_id": "Europe/Minsk",
        "viewport": {"width": 1600, "height": 900},
    }

@pytest.fixture
def page(context) -> Generator[Page, Any, None]:
    page: Page = context.new_page()
    page.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    yield page

@pytest.fixture
def logged_in_page(page: Page) -> Page:
    page.goto(get_base_url())
    page.locator('#submit-button').filter(has_text='Принять все cookie').click()
    #MainPage(page).open_login_page()
    #LoginPage(page).choose_email_nick_auth()
    #LoginPage(page).login_as(get_login(), get_password())
    return page