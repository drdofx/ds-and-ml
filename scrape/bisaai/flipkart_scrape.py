from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Firefox()

url = "https://www.flipkart.com/laptops/~buyback-guarantee-on-laptops-/pr?sid=6bo%2Cb5g&uniqBStoreParam1=val1&wid=11.productCard.PMU_V2"

driver.get(url)

content = driver.page_source

soup = BeautifulSoup(content)
products = []

for a in soup.findAll('a', {'class', '_1fQZEK'}):
    name = a.find('div', {'class': '_4rR01T'}).text
    price = a.find('div', {'class': '_30jeq3 _1_WHN1'}).text
    rating = a.find('div', {'class': '_3LWZlK'}).text
    
    product = {
        'productName': name,
        'price': price,
        'rating': rating
    }

    products.append(product)

print(products)
df = pd.DataFrame(products)
df.to_csv("flipkart_products.csv", encoding='utf-8', index=False)