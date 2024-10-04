from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

CHROMEDRIVER_PATH = r"C:\Users\sania\OneDrive\Рабочий стол\chromedriver.exe"

service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)

driver.implicitly_wait(10)

try:
    driver.get("https://petfriends.skillfactory.ru/all_pets")

    cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card"))
    )

    for card in cards:
        try:
            photo = WebDriverWait(card, 10).until(
                EC.visibility_of(card.find_element(By.CLASS_NAME, "card-img-top"))
            )
            name = WebDriverWait(card, 10).until(
                EC.visibility_of(card.find_element(By.CLASS_NAME, "card-title"))
            )
            age = WebDriverWait(card, 10).until(
                EC.visibility_of(card.find_element(By.CLASS_NAME, "card-text"))
            )

            print(f"Имя: {name.text}, Возраст: {age.text}, Фото: {photo.get_attribute('src')}")
        except Exception as e:
            print("Ошибка при получении информации о питомце:", e)

except Exception as e:
    print("Произошла ошибка:", e)

finally:

    time.sleep(2)
    driver.quit()
