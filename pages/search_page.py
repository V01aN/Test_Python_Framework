import allure
from playwright.sync_api import Page, Locator, expect

class SearchPage:
    def __init__(self, page: Page):
        self.page = page
        self.search_bar = page.get_by_role('combobox')
        self.search_result = page.get_by_role('link')

    def result_with_text(self, text: str) -> Locator:
        return self.search_result.filter(has_text=text)

    def open(self):
        self.page.goto('https://www.duckduckgo.com')

    @allure.step('Ввести в поисковую строку {content} и нажать enter')
    def search_content(self, content: str):
        self.search_bar.fill(content)
        self.search_bar.press('Enter')

    @allure.step('Окрыть результат поиска с текстом {text}')
    def open_result_by_text(self, text: str):
        self.result_with_text(text).click()


    @allure.step('Проверить что результат поиска с текстом {content} отображается')
    def assert_search_result(self, content: str):
        expect(self.result_with_text(content),
               f'В результатах поиска отсутствует искомый текст: {content}').to_be_visible(timeout=20_000)