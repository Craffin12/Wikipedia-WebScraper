from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


def headingChoice(heading, html):
    if heading == "Overview":
        paragraph = html.find(id="mw-content-text").contents[0].contents[0]
    else:
        paragraph = html.find(id=heading).parent

    return paragraph


def paragraphScraper(paragraph):
    collection = {}
    count = 1
    while paragraph.find_next_sibling().name != "h2":
        paragraph = paragraph.find_next_sibling()
        if paragraph.name == "p" and paragraph.text != '\n':
            collection["paragraph{}".format(count)] = paragraph.text
            count += 1

    return collection


def wikipediaScraper(title, heading):
    url = 'https://en.wikipedia.org/wiki/' + title.replace(" ", "_")
    heading = heading.replace(" ", "_")
    res = requests.get(url)

    html = BeautifulSoup(res.text, "html.parser")

    paragraph = headingChoice(heading, html)

    paragraphCollection = paragraphScraper(paragraph)

    return paragraphCollection


print(wikipediaScraper("Black pepper", "History"))


@app.route('/')
def hello_world():  # put application's code here
    return jsonify(message='Hello World!')


if __name__ == '__main__':
    app.run()
