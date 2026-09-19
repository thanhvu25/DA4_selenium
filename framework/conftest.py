import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config.config import BASE_URL, BROWSER, IMPLICIT_WAIT, EXPLICIT_WAIT


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    driver.get(BASE_URL)

    yield driver

    driver.quit()