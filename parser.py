import requests
from requests import Session
from bs4 import BeautifulSoup
import xlsxwriter


#//////// Авторизация на сайте, пример:

headers = {"user-agent":
			"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

# work = Session() # Сохраняет куки для сессии 

# work.get("https://quotes.toscrape.com/", headers=headers)

# response = work.get("https://quotes.toscrape.com/login", headers=headers)

# soup = BeautifulSoup(response.text, "lxml") # Подключаем парсер к переменной response 

# token = soup.find("form").find("input").get("value") 

# data = {"csrf_token":token, "username":"123", "password":"123"}

# result = work.post("https://quotes.toscrape.com/login", headers=headers, data=data, allow_redirects=True) # allow_redirects - Разрешить перенаправление

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#/// Работа с найденой информацией и скачивание файлов, пример:
def array():
 	for card_url in get_url():
 		response = requests.get(card_url, headers=headers)

 		soup = BeautifulSoup(response.text, 'lxml')

 		data = soup.find("div", class_="card mt-4 my-4")

 		name = data.find("h3", class_="card-title").text

 		price = data.find("h4").text

 		card_text = data.find("p", class_="card-text").text

 		card_img = "https://scrapingclub.com" + data.find("img", class_="card-img-top img-fluid").get("src")

 		download(card_img)

 		yield name, price, card_text, card_img


#//// Перелистывание страниц, пример:
def get_url():
 	for count in range(1, 8):

 		url = f"https://scrapingclub.com/exercise/list_basic/?page={count}"

 		response = requests.get(url, headers=headers)

 		soup = BeautifulSoup(response.text, 'lxml')

 		data = soup.find_all("div", class_="col-lg-4 col-md-6 mb-4")

 		for i in data:

 			card_url = "https://scrapingclub.com" + i.find("a").get("href")

 			yield card_url


#/////////Скачивание фотографий, пример:
def download(url): 

 	resp = requests.get(url, stream=True)

 	r = open("C:\\Users\\xmedv\\Desktop\\test\\" + url.split("/")[-1], "wb")

 	for value in resp.iter_content(1024*1024):

 		r.write(value)

 	r.close()
 	

######################## Пример записи в эксель
def writer(parament):
	book = xlsxwriter.Workbook("C:\\Users\\xmedv\\Desktop\\data.xlsx")
	page = book.add_worksheet("Одежда")


	row = 0
	column = 0

	page.set_column("A:A", 20)
	page.set_column("B:B", 10)
	page.set_column("C:C", 30)
	page.set_column("D:D", 50)


	for item in parament():
		page.write(row, column, item[0])
		page.write(row, column+1, item[1])
		page.write(row, column+2, item[2])
		page.write(row, column+3, item[3])
		row +=1

	book.close()


writer(array)
