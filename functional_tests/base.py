import sys

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def browser():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument('--start-maximized')
    browser = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
    yield browser
    browser.quit()


def wait_until_presence_of_element(browser: webdriver.Chrome, selector: str, by=By.CSS_SELECTOR):
    """Подождать пока элемент появится на странице."""
    error_element = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((by, selector))
    )
    return error_element


def wait_until_NOT_presence_of_element(browser: webdriver.Chrome, selector: str, by=By.CSS_SELECTOR):
    """Подождать пока элемент не исчезнет со страницы."""
    error_element = WebDriverWait(browser, 5).until_not(
        EC.presence_of_element_located((by, selector))
    )
    return error_element


if __name__ == "__main__":
    sys.exit(pytest.main(["-qq"]))
