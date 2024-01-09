import time
import requests
import selectorlib
import smtplib, ssl
import os

URL = 'https://www.premier1supplies.com/p/permanet-plus-48-inch-starter-kit?cat_id=190'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    """Scrape the page source from the url"""
    response = requests.get(url, headers=HEADERS)
    source_html = response.text
    return source_html


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
    value = extractor.extract(source)['price']
    return value


def send_email(message):
    host = 'smtp.gmail.com'
    port = 465

    sender = 'rbn.leona@gmail.com'

    password = os.getenv('PASSWORD_LEONA')
    print(password)
    receiver = 'rbn.leona@gmail.com'

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        # server.ehlo_or_helo_if_needed()
        server.login(sender, password)
        server.sendmail(sender, receiver, message)
    print('email sent')


def store(extracted):
    with open('data.txt', 'a') as file:
        file.write(extracted + '\n')


def read(extracted):
    with open('data.txt', 'r') as file:
        return file.read()


if __name__ == '__main__':
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        # print(extracted)
        content = read(extracted)

        if extracted != '$539.80':
            if extracted not in content:
                store(extracted)
                send_email(message='new price')
        time.sleep(86400)
