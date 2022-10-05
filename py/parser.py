import time
import sqlite3
import requests
import pandas as pd
from random import randint
from bs4 import BeautifulSoup
from openpyxl import Workbook
from selenium import webdriver
from openpyxl.styles import Font
from openpyxl import load_workbook
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC



HEADERS = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36', 
	'accept' : '*/*'
}

def check_element(driver):
	try:
		elem = driver.find_element_by_xpath("//div/li[contains(text(), 'Следующая')]")
		return True
	except NoSuchElementException:
		return False

def get_data(sql, db):
	count = len(sql.execute("""SELECT name FROM products""").fetchall())
	index = 1
	options = webdriver.ChromeOptions()
	options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36")
	options.add_argument("--start-maximized")
	while(index <= count):
		url = sql.execute("""SELECT url FROM products WHERE id == ?""", (index, )).fetchone()
		driver = webdriver.Chrome(
			executable_path="C:\\Users\\japo0\\Desktop\\Kaspi\\driver\\chromedriver.exe",
			options = options
		)
		try:
			driver.get(url[0])
			time.sleep(5)
			driver.find_element_by_xpath("//li/a[contains(text(), 'Нур-Султан')]").click() 
			time.sleep(5)
			with open("index_selenium.html", "w", encoding="utf-8") as file:
				file.write(driver.page_source)

			isTrue = check_element(driver)

			if (isTrue):
				nxt = driver.find_element_by_xpath("//div/li[contains(text(), 'Следующая')]")
				while (nxt.get_attribute('class') != 'pagination__el _disabled'):
					nxt.click()
					with open("index_selenium.html", "a", encoding="utf-8") as file:
						file.write(driver.page_source)

			with open("index_selenium.html", encoding="utf-8") as file:
				src = file.read()
			soup = BeautifulSoup(src, "html.parser")
			stores = soup.find("table").find("tbody").find_all("tr")
			store = []
			for x in stores:
				store.append({
					'name' : x.find('a').text.strip(),
					'price' : x.find('div', 'sellers-table__price-cell-text').text.replace(" ₸", "").replace("\xa0", "")
				})
			for i in range(len(store)):
				if (store[i]["name"] == 'Stratton'):
					ind = i
				elif (store[i]["name"] == 'Quattro'):
					quat = store[i]["name"]
			min_price = sql.execute("""SELECT min_price FROM products WHERE id == ?""", (index, )).fetchone()
			price = int(store[ind]['price'])
			if (ind != 0):
				oths = int(store[0]['price'])
				if (oths - 1 >= int(min_price[0]) and store[0]['name'] != quat):
					rec = oths - 1
				elif (oths == int(min_price[0]) and store[0]['name'] != quat):
					rec = oths
				elif (oths < int(min_price[0]) and store[0]['name'] != quat):
					rec = int(min_price[0])
				else:
					rec = price
			else:
				for i in range(len(store)):
					oths = int(store[i]['price'])
					if (price < oths and store[i]['name'] != quat and i != 0):
						rec = oths - 1
						break
					elif (price == oths and price != int(min_price[0]) and store[i]['name'] != quat and i != 0):
						rec = oths
						break
					elif (price == oths and price == int(min_price[0]) and store[i]['name'] != quat and i != 0):
						rec = price
						break
					elif (i != 0):
						rec = price
						break
					elif(len(store) == 1):
						rec = price

			print('-' * 30)
			print('-' * 30)
			print(price)
			query = """ UPDATE products SET price = ? WHERE id = ? """
			sql.execute(query, (price, index))
			print(rec)
			query = """ UPDATE products SET recommended_price = ? WHERE id = ? """
			sql.execute(query, (rec, index))
			print(oths)
			query = """ UPDATE products SET competitors_price = ? WHERE id = ? """
			sql.execute(query, (oths, index))
			db.commit()
			print(int(min_price[0]))
			print('-' * 30)
			print()
		except Exception as ex:
			print(ex)
		finally:
			driver.close()
			driver.quit()
			index = index + 1


def parse():
	with sqlite3.connect('db/parser.db') as db:
		sql = db.cursor()
		get_data(sql, db)
	esc = input("Нажмите ENTER чтобы закрыть консоль")
	db.close()


wb = load_workbook('products_list.xlsx')
parse()


