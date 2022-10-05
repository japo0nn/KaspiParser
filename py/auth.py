import time
import requests
import pandas as pd
from random import randint
from bs4 import BeautifulSoup
from openpyxl import Workbook
from selenium import webdriver
from openpyxl.styles import Font
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

headers = {
	'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
	'accept' : '*/*'
}

url = 'https://kaspi.kz/merchantcabinet/login'

datas = {
	'username' : 'flyingbear.kz@gmail.com',
	'password' : 'Kingster1993!'
}

def get_pages(src):
	soup = BeautifulSoup(src, "html.parser")
	pages = soup.find('td', class_='GLAINTQDLH')
	page_count = pages.text
	index = page_count.find('из ')
	index = index + 3
	print(index)
	print()
	page = page_count[index:]
	print(page)
	return page


def auth():
	options = webdriver.ChromeOptions()
	options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36")
	options.add_argument("--start-maximized")
	chk = False
	while(chk != True):
		try:
			driver = webdriver.Chrome(
				executable_path="C:\\Users\\japo0\\Desktop\\Kaspi\\driver\\chromedriver.exe",
				options = options
			)
			driver.get(url)
			login = driver.find_element_by_id('email')
			passwd = driver.find_element_by_id('password')
			login.send_keys('flyingbear.kz@gmail.com')
			passwd.send_keys('Kingster1993!')
			element = driver.find_element_by_class_name('button')
			element.click()
			time.sleep(randint(10, 30))
			element = driver.find_element_by_id('main-nav-offers')
			element.click()
			

			
			time.sleep(randint(20, 40))

			with open("pages.html", "w", encoding="utf-8") as file:
				file.write(driver.page_source)

			with open("pages.html", encoding="utf-8") as file:
				src = file.read()

			pages = int((int(get_pages(src)) / 10) + 1)

			

			for i in range(pages):
				with open("pages/page" + str(i + 1) + ".html", "w", encoding="utf-8") as file:
					file.write(driver.page_source)
				nexts = driver.find_elements_by_class_name('GLAINTQDJH')
				for i in range(4):
					if (nexts[i].find_element_by_class_name('gwt-Image').get_attribute("aria-label") == "Next page"):
						btn = nexts[i].find_element_by_class_name('gwt-Image')
						actions = ActionChains(driver);
						actions.move_to_element(btn).click().perform();
						print("Success")
				time.sleep(randint(10, 20))
			chk = True


		except Exception as ex:
			print(ex)
		finally:
			driver.close()
			driver.quit()


auth()