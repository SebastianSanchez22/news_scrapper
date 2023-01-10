import requests
import lxml.html as html
import os
import datetime

# Link to news website
HOME_URL = 'https://www.larepublica.co'

XPATH_LINK_TO_ARTICLE = '//text-fill[not(@class)]/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]//span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class = "html-content"]/p[not (@class)]/text()'


def parse_news(link, today):
    try:
        # Get info from the news page
        response = requests.get(link)
        if response.status_code == 200:
            news = response.content.decode('utf-8')
            # Turning into HTML the news response from the website
            parsed = html.fromstring(news)

            try:
                # XPATH_TITLE returns two elements, titles are contained in the second value
                title = parsed.xpath(XPATH_TITLE)[1]
                # In case there are others backslash, remove them
                title = title.replace('\"', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            # Since there are many pages in the website that may not have summaries, return to ignore
            except IndexError:
                return
            # Writing in file all news from the current day 
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as file:
                file.write(title)
                file.write('\n\n')
                file.write(summary)
                file.write('\n\n')
                for p in body:
                    file.write(p)
                    file.write('\n')
        else:
            # If response.statuscode throws as error, e.j 404 not found
            raise ValueError(F'Error: {response.status_code}')
    except ValueError as error:
        print(error)


def parse_home():
    try:
        # Get info from the main page
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            # Turning into HTML the news response from the website
            parsed = html.fromstring(home)
            # Applying xpath to return links
            links_to_news = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            today = datetime.date.today().strftime('%d-%m-%Y')
            # Creating a directory to save the scrapped info if it's not already created
            if not os.path.isdir(today):
                os.mkdir(today)

            # Apllying parse_news method to write each news into the directory
            for link in links_to_news:
                parse_news(link, today)
        else:
            # If response.statuscode throws as error, e.j 404 not found
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as error:
        print(error)


def run():
    parse_home()


if __name__ == '__main__':
    run()