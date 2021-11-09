from flask import Flask, jsonify
from bs4 import BeautifulSoup
from flask_cors import CORS
import requests

app = Flask(__name__)

cors = CORS(app)  # Prevents the raising of restrictions due to CORS

"""
Used the official documentation 
https://beautiful-soup-4.readthedocs.io/en/latest/
to research general beautifulsoup 4 methods. All code is my own.
"""


def headingChoice(heading, html):
    """
    Navigates html object to heading. Allows for the choice of an overview
    section. This is the paragraph/s right under page title. If a user provides
    a heading that doesn't exist returns None.
    """
    if heading == "Overview":
        paragraph = html.find(id="mw-content-text")
        if paragraph is None:
            return paragraph
        paragraph = paragraph.contents[0].contents[0]
    else:
        paragraph = html.find(id=heading)
        if paragraph is None:
            return paragraph
        paragraph = paragraph.parent

    return paragraph


def paragraphScraper(paragraph):
    """
    Creates a dictionary that holds each paragraph between heading (h2 tag)
    and next heading (h2 tag).
    """
    collection = {}
    count = 1
    while paragraph.find_next_sibling().name != "h2":
        paragraph = paragraph.find_next_sibling()
        if paragraph.name == "p" and paragraph.text != '\n':
            collection["paragraph{}".format(count)] = paragraph.text
            count += 1

    return collection


def wikipediaScraper(title, heading):
    """
    Takes in a title that is associated with a Wikipedia page. Takes
    in a heading for an h2 heading on that page. Returns an error if heading
    doesn't exist, a collection of paragraphs if not.
    """
    # Change spaces to _ which is used url
    url = 'https://en.wikipedia.org/wiki/' + title.replace(" ", "_")
    heading = heading.replace(" ", "_")

    res = requests.get(url)

    paragraphCollection = {}  # Will hold response for user

    if res.status_code == 404:
        paragraphCollection["err"] = "Title doesn't exist for a Wikipedia Page"
        return paragraphCollection

    html = BeautifulSoup(res.content,
                         "html.parser")  # Set up html object to parse

    paragraph = headingChoice(heading, html)

    if paragraph is None:
        paragraphCollection["err"] = "Heading Not Found On Requested Page"
        return paragraphCollection
    else:
        paragraphCollection = paragraphScraper(paragraph)
        return paragraphCollection


@app.route('/wikiScraper/<string:title>/<string:heading>', methods=['Get'])
def wikiScraper(title: str, heading: str):
    response = wikipediaScraper(title, heading)
    return jsonify(response)


if __name__ == '__main__':
    app.run()
