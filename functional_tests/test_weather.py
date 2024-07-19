from pytest_django.fixtures import live_server
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from functional_tests.base import browser, wait_until_presence_of_element

TEST_CITY = "Санкт-Петербург"


class TestWeather:
    """Тест приложения погода."""

    def test_can_open_website(self, browser: webdriver.Chrome, live_server):
        """Тест: можно начать список для одного пользователя."""
        # Эдит слышала про крутое новое онлайн-приложение с прогнозами погоды
        # Она решает оценить его домашнюю страницу
        browser.get(live_server.url)
        # Она видит, что заголовок и шапка страницы говорят о прогнозе погоды
        assert "SuperWeather" in browser.title
        # Ей сразу же предлагается ввести название города
        input_box = browser.find_element(By.ID, "city")
        assert input_box.get_attribute("placeholder") == "например: Москва"
        # Она набирает в текстовом поле название своего родного города
        input_box.send_keys(TEST_CITY)
        # И нажимает клавишу ENTER
        input_box.send_keys(Keys.ENTER)
        # Когда она нажимает enter, страница обновляется, и теперь страница
        # содержит прогноз погоды для указанного города
        wait_until_presence_of_element(browser, f'//h1[contains(text(), "{TEST_CITY}")]', By.XPATH)
        wait_until_presence_of_element(browser, '//h2[contains(text(), "Текущая погода")]', By.XPATH)
        wait_until_presence_of_element(browser, '//h2[contains(text(), "В ближайшее время")]', By.XPATH)
        # она решает попробовать посмотреть прогноз погоды для другого города
        browser.find_element(By.XPATH, '//a[contains(text(), "Домашняя страница")]').click()
        # однако случайно вводит значение несуществующего города
        input_box = browser.find_element(By.ID, "city")
        input_box.send_keys("Santa-Pitsburg")
        input_box.send_keys(Keys.ENTER)
        # появляется всплывающее сообщение о том, что введённый город не найден
        wait_until_presence_of_element(
            browser,
            '//div[contains(text(), "Город Santa-Pitsburg не найден, попробуйте ещё раз.")]',
            By.XPATH)
        # и сайт автоматически перенаправляет её на домашнюю страницу
        wait_until_presence_of_element(browser, '//a[contains(text(), "Домашняя страница")]', By.XPATH)
        # она решает повторно проверить погоду в своём городе
        input_box = browser.find_element(By.ID, "city")
        # как только она начинает вводить первую букву названия города появляется поле-подсказка,
        # позволяющее выбрать город из числа ранее запрашиваемых городов, начинающихся с этой буквы
        input_box.send_keys("С")
        help_field = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "ui-id-1")))
        # она выбирает свой город в поле подсказке
        help_field.click()
        # форма заполняется его полным названием
        input_box = browser.find_element(By.ID, "city")
        assert input_box.get_attribute("value") == TEST_CITY
        input_box.send_keys(Keys.ENTER)
        # Когда она нажимает enter, страница обновляется, и теперь страница
        # снова содержит прогноз погоды для указанного города
        wait_until_presence_of_element(browser, f'//h1[contains(text(), "{TEST_CITY}")]', By.XPATH)
        wait_until_presence_of_element(browser, '//h2[contains(text(), "Текущая погода")]', By.XPATH)
        # также она замечает ссылку количество просмотров прогноза погоды для этого города и переходит по ней
        link_to_count_api = browser.find_element(
            By.LINK_TEXT, "количество просмотров прогноза погоды для этого города")
        link_to_count_api.click()
        # на странице отображается JSON объект, содержащий количество общее количество просмотров прогноза погоды
        assert browser.find_element(By.TAG_NAME, "body").text == '{"count": 2}'
