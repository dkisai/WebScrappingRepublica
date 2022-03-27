from genericpath import isdir
from importlib.resources import path
import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//h2/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/h2/span/text()'
XPATH_SUMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]]/text()'


def parse_notices(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                summary = parsed.xpath(XPATH_SUMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                print('No se encontraron elementos')
                return
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as file:
                file.write(title)
                file.write('\n\n')
                file.write(summary)
                file.write('\n\n')
                for p in body:
                    file.write(p)
                    file.write('\n')
        else:
            raise ValueError(f'Error al obtener la pagina {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links)
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            for link in links:
                parse_notices(link, today)
        else:
            raise ValueError(f'Error al obtener la pagina {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()