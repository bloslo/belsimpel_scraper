from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import datetime

def write_to_file(filename: str, lines: list[str]):
    with open(filename, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write('{0}\n'.format(line))

if __name__ == '__main__':
    root_url = 'https://www.belsimpel.nl'

    r = requests.get(root_url)

    soup = BeautifulSoup(r.content, 'lxml')
    top_ten = soup.find('div', class_='js_user_topten')
    top_ten_tabs = top_ten.find_all('a', class_='ab_user_topten_tab')
    top_ten_links = top_ten.find_all('a', class_='product')

    tabs_index = 0
    lines = []
    for index, link in enumerate(top_ten_links):
        phone_name = link.find('h4', class_='prd_title')
        number_element = link.find('div', class_='prd_number')
        number_str = number_element.get_text(strip=True)
        number = int(number_str)

        driver = webdriver.Firefox()
        driver.get(root_url + link['href'])
        wait = WebDriverWait(driver, 15)
        price_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div:not([class]) > span[class*="Pricingstyle__StyledPricing-"]')))
        print(price_element.text)
        price = price_element.text
        driver.close()

        if int(number) == 1:
            categorie = top_ten_tabs[tabs_index].get_text(strip=True)
            lines.append(categorie)
            tabs_index += 1
        lines.append(number_str + ' - ' + phone_name.get_text(strip=True) + ' - \u20AC ' + price)
       
        last_index = len(top_ten_links) - 1
        if index != last_index:
            next_number_element = top_ten_links[index + 1].find('div', class_='prd_number')
            next_number_str = next_number_element.get_text(strip=True)
            print(next_number_str)

            if int(number) % 10 == 0 or int(next_number_str) == 1:
                lines.append('')
                time.sleep(10)

    filename = 'top_10_' + datetime.datetime.today().strftime('%d_%m_%Y_%H_%M_%S') + '.txt'
    write_to_file(filename, lines)
