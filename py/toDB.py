import time
import glob
import sqlite3
import os.path
import requests
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl import Workbook
from selenium import webdriver
from openpyxl.styles import Font
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

def to_db(sql, db):


	count = sum(os.path.isfile(f) for f in glob.glob('pages/*'))
	ind = 1
	for i in range(count):
		
		with open("pages/page" + str(i + 1) + ".html", encoding="utf-8") as file:
			src = file.read()
		soup = BeautifulSoup(src, "html.parser")
		table = soup.find("table", class_ = ('GLAINTQDBR')).find("tbody").find_all("tr")
		items = []
		for x in table:
			name = x.find('a', class_ = 'offer-managment__product-cell-link').text
			link = x.find('a', class_ = 'offer-managment__product-cell-link')['href']
			sql.execute(""" INSERT OR IGNORE INTO products VALUES (?, ?, ?, ?, ?, ?, ?)""", (ind, name, link, 0, 0, 0, 0))
			db.commit()
			ind = ind + 1

with sqlite3.connect('db/parser.db') as db:
	sql = db.cursor()
	sql.execute("""CREATE TABLE IF NOT EXISTS products(
		id INTEGER,
		name TEXT,
		url TEXT,
		price TEXT,
		min_price TEXT,
		recommended_price TEXT,
		competitors_price TEXT
	)""")
	db.commit()
	print('Success')
	to_db(sql, db)

db.close()	
