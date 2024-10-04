import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROMEDRIVER_PATH = r"C:\Users\Ваше_Имя\Downloads\chromedriver.exe"

@pytest.fixture(scope="module")
def setup():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_check_pet_cards(setup):
    driver = setup
    driver.get("https://petfriends.skillfactory.ru/all_pets")

    pet_cards = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "card"))
    )

    assert len(pet_cards) > 0, "Нет карточек питомцев на странице"

    for card in pet_cards:
        assert card.is_displayed(), "Карточка питомца не отображается"

        name = WebDriverWait(card, 10).until(
            EC.visibility_of(card.find_element(By.CLASS_NAME, "card-title"))
        )
        age = WebDriverWait(card, 10).until(
            EC.visibility_of(card.find_element(By.CLASS_NAME, "card-text"))
        )
        photo = WebDriverWait(card, 10).until(
            EC.visibility_of(card.find_element(By.CLASS_NAME, "card-img-top"))
        )

        assert name.text, "Имя питомца отсутствует"
        assert age.text, "Возраст питомца отсутствует"
        assert photo.get_attribute("src"), "Фото питомца отсутствует"

def test_check_pet_table(setup):
    driver = setup
    driver.get("https://petfriends.skillfactory.ru/all_pets")

    table = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "table"))
    )

    assert table.is_displayed(), "Таблица питомцев не отображается"

    rows = table.find_elements(By.TAG_NAME, "tr")
    assert len(rows) > 1, "Нет питомцев в таблице"

    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, "td")
        assert len(cells) > 0, "Нет данных в строке питомца"
        assert cells[0].text, "Имя питомца отсутствует"
        assert cells[1].text, "Вид питомца отсутствует"
        assert cells[2].text, "Возраст питомца отсутствует"