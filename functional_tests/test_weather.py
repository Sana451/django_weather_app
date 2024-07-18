from pytest_django.fixtures import live_server
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from functional_tests.base import browser, wait_until_presence_of_element

TEST_CITY = "Геленджик"


class TestWeather:
    """Тест приложения погода."""

    def test_can_open_website(self, browser: webdriver.Chrome, live_server):
        """Тест: можно начать список для одного пользователя."""
        # Эдит слышала про крутое новое онлайн-приложение с прогнозами погоды
        # Она решает оценить его домашнюю страницу
        browser.get(live_server.url)
        # Она видит, что заголовок и шапка страницы говорят о прогнозе погоды
        assert "SuperWeather" in browser.title
        # Ей сразу же предлагается ввести город
        input_box = browser.find_element(By.ID, "id_city")
        assert input_box.get_attribute("placeholder") == "например: Москва"
        # Она набирает в текстовом поле "Санкт-Петербург"
        input_box.send_keys(TEST_CITY)
        # И нажимает клавишу ENTER
        input_box.send_keys(Keys.ENTER)
        # Когда она нажимает enter, страница обновляется, и теперь страница
        # содержит прогноз погоды для указанного города
        wait_until_presence_of_element(browser, f'//h1[contains(text(), "{TEST_CITY}")]', By.XPATH)
        wait_until_presence_of_element(browser, '//h2[contains(text(), "Текущая погода")]', By.XPATH)
        wait_until_presence_of_element(browser, '//h2[contains(text(), "В ближайшее время")]', By.XPATH)
        # она решает посмотреть прогноз погоды для другого города
        browser.find_element(By.XPATH, '//a[contains(text(), "Домашняя страница")]').click()
        # после чего случайно вводит значение несуществующего города
        input_box = browser.find_element(By.ID, "id_city")
        input_box.send_keys("Santa-Pitsburg")
        input_box.send_keys(Keys.ENTER)
        # появляется всплывающее сообщение о том, что введённый город не найден
        wait_until_presence_of_element(
            browser,
            '//div[contains(text(), "Город Santa-Pitsburg не найден, попробуйте ещё раз.")]',
            By.XPATH)
        # сайт автоматически перенаправляет её на домашнюю страницу
        wait_until_presence_of_element(browser, '//a[contains(text(), "Домашняя страница")]', By.XPATH)

