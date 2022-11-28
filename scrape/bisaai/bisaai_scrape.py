from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

head_option = webdriver.FirefoxOptions()
head_option.add_argument("--headless")

driver = webdriver.Firefox(options=head_option)

url = "https://bisa.ai/course/all_course/1"

driver.implicitly_wait(5) # Implicitly wait for 5 seconds to find card element
driver.get(url)

cards = driver.find_elements(By.CSS_SELECTOR, ".card.shadow.box-shadow.pointer.mb-2")

course_names = []

for card in cards:
    course_name = card.find_element(By.CLASS_NAME, "card-title").text
    course_names.append(course_name)

df = pd.DataFrame({"course_name": course_names})
df.to_csv("free-course-bisaai.csv", encoding='utf-8', index=False)