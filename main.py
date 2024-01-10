import time
import requests
import selectorlib
import smtplib, ssl
import os
import sqlite3
from datetime import datetime

URL = 'https://www.premier1supplies.com/p/permanet-plus-48-inch-starter-kit?cat_id=190'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

connection = sqlite3.connect('price_database.db')
date = datetime.now().strftime("%y-%m-%d")


def scrape(url):
    """Scrape the page source from the url"""
    response = requests.get(url, headers=HEADERS)
    source_html = response.text
    return source_html


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
    price_value = extractor.extract(source)['price']
    # item_id_value = extractor.extract(source)['item_id']
    return price_value


def extract_item_id(source):
    extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
    item_id_value = extractor.extract(source)['item_id']
    return item_id_value


def send_email(message):
    host = 'smtp.gmail.com'
    port = 465

    sender = 'rbn.leona@gmail.com'

    password = os.getenv('PASSWORD_LEONA')
    receiver = 'rbn.leona@gmail.com'

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        # server.ehlo_or_helo_if_needed()
        server.login(sender, password)
        server.sendmail(sender, receiver, message)
    print('email sent')


def store(extracted):
    # scraped = scrape(URL)
    # extracted_price = extract(scraped)
    # extracted_item_id = extract_item_id(scraped)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO priceData VALUES(?,?,?)", (date, extracted_item_id, extracted_price))
    connection.commit()


def read(extracted):
    # date = datetime.now().strftime("%y-%m-%d")
    # scraped = scrape(URL)
    # extracted_price = extract(scraped)
    # extracted_item_id = extract_item_id(scraped)
    cursor = connection.cursor()
    # date, item_id, price = row
    cursor.execute("SELECT * FROM priceData WHERE date=? AND item_ID=? AND price=?",
                   (date, extracted_item_id, extracted_price))
    result_rows = cursor.fetchall()
    print(result_rows)
    return result_rows


# def read(extracted):
#     with open('data.txt', 'r') as file:
#         return file.read()


if __name__ == '__main__':
    while True:
        scraped = scrape(URL)
        extracted_price = extract(scraped)
        extracted_item_id = extract_item_id(scraped)
        print(extracted_price, extracted_item_id)

        if extracted_price != '$549.80':
            content = read(extracted_price)
            # content_id = read(extracted_item_id)
            if extracted_price not in content:
                store(extracted_price)
                send_email(message='new price')
                print('send')
        time.sleep(2)
