from config.config import BASE_URL


def test_open_homepage(driver):
    driver.get(BASE_URL)
    assert driver.title == "Swag Labs"  