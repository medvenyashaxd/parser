import json
import random
import time
import requests
import xlsxwriter

def pars():
    page_number = 1 # Начальная страница
    count_pages = 0  # Счетчик страниц

    session = requests.Session() # Запуск сессии

    while count_pages != 2: # - Кол-во страниц для парсинга
        url = f"https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-2162196,-1257786&emp=0&lang=ru&locale=ru&page={page_number}&pricemarginCoeff=1.0&query=%D0%A1%D0%BC%D0%B0%D1%80%D1%82%D1%84%D0%BE%D0%BD%D1%8B&reg=0&regions=80,68,64,83,4,38,33,70,82,69,86,75,30,40,48,1,22,66,31,71&resultset=catalog&sort=popular&spp=0&suppressSpellcheck=false"
        headers = { #- Заголовок для get запроса
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7",
            "Connection": "keep-alive",
            "Host": "search.wb.ru",
            "Origin": "https://www.wildberries.ru",
            "Referer": f"https://www.wildberries.ru/catalog/0/search.aspx?page={page_number}&sort=popular&search=%D1%81%D0%BC%D0%B0%D1%80%D1%82%D1%84%D0%BE%D0%BD%D1%8B",
            "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        }

        response = session.get(url, headers=headers)
        data = response.json() # - Перевод ответа в словарь

        file_path_json = r"C:\Users\xmedv\PycharmProjects\parserBot\test.json"

        with open(file_path_json, "a", encoding="utf-8") as file: # Сохранение json файла
            json.dump(data, file, ensure_ascii=False, indent=3)
        file.close()
        print(data)

        file_path_txt = r"C:\Users\xmedv\PycharmProjects\parserBot\test.txt"

        for r in range(100): # Сохранение в текстовый документ
            with open(file_path_txt, "a", encoding="utf-8") as file:
                file.write(data["data"]["products"][r]["brand"])
                file.write(" ")
                file.write(data["data"]["products"][r]["name"])
                file.write(" ")
                file.write(str(data["data"]["products"][r]["id"]))
                file.write(" ")
                file.write(str(data["data"]["products"][r]["salePriceU"]))
                file.write("\n")
        file.close()

        page_number += 1
        count_pages += 1
        time.sleep(random.randint(12, 15))

        xl_file = xlsxwriter.Workbook(r"C:\Users\xmedv\PycharmProjects\parserBot\test.xlsx")
        page = xl_file.add_worksheet("Smartphones")
        row = 0
        column = 0

        page.set_column("A:A", 10)
        page.set_column("B:B", 45)
        page.set_column("C:C", 10)
        page.set_column("D:D", 10)

        for i in range(100): # Сохранение в xl документ
            page.write(row, column, data["data"]["products"][i]["brand"])
            page.write(row, column + 1, data["data"]["products"][i]["name"])
            page.write(row, column + 2, data["data"]["products"][i]["id"])
            page.write(row, column + 3, data["data"]["products"][i]["salePriceU"])
            row += 1
        xl_file.close()


if __name__ == '__main__':
    pars()
