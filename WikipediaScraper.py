from flask import Flask, jsonify
from bs4 import BeautifulSoup
from flask_cors import CORS
import requests

application = Flask(__name__)

CORS(application)  # Prevents the raising of restrictions due to CORS

"""
Used the official documentation 
https://beautiful-soup-4.readthedocs.io/en/latest/
to research general beautifulsoup 4 methods. All code is my own.

Used the offical documentation
https://docs.python-requests.org/en/latest/user/quickstart/
to learn how to use requests and to learn about response.text.
All code is my own.
"""

def headingChoice(heading, html):
    """Navigates html object to heading, if "Overview" is passed navigated to text
    under title on Wikipedia Page and if no paragraph is found returns None."""
    if heading == "Overview":
        # Find text right under title
        paragraph = html.find(id="mw-content-text")
        return None if paragraph is None else paragraph.contents[0].contents[0]
    else:
        paragraph = html.find(id=heading)
        return None if paragraph is None else paragraph.parent

def paragraphScraper(paragraph):
    """ Creates a dictionary that holds each paragraph between heading (h2 tag)
    and next heading (h2 tag). Returns dictionary."""
    collection = {}
    count = 1
    while paragraph.find_next_sibling().name != "h2":
        paragraph = paragraph.find_next_sibling()
        if paragraph.name == "p" and paragraph.text != '\n':
            # label paragraph numbers
            collection["paragraph{}".format(count)] = paragraph.text
            count += 1
    return collection

def handleNoHeadingOrPageError():
    """Handles if there is no heading on current wikipedia page or the page doesn't exist"""
    paragraphDict = {}
    paragraphDict["err"] = "Heading or Page Not Found!"
    return paragraphDict

def requestPageGetHtml(url):
    """Requests text information from url page and returns None if status code is 404 or 
    an Beautiful soup object that contains page's html"""
    resp = requests.get(url)
    return None if resp.status_code == 404 else BeautifulSoup(resp.text, "html.parser")

def wikipediaScraper(title, heading):
    """Takes in a title for an ingredient and a heading (Overview/History), scrapes text
    off Wikipedia page that corresponds to title/headign combo and returns text in dictionary."""
    url = "https://en.wikipedia.org/wiki/" + title.replace(" ", "_")  # Change spaces to _ for url
    heading = heading.replace(" ", "_")
    htmlContent = requestPageGetHtml(url)
    # Target h2 tag on page for heading or None if BeautifulSoup object was None
    paragraph = headingChoice(heading, htmlContent) if htmlContent is not None else htmlContent
    # If no paragraph returned, handle "error" else scrape all paragraphs under heading
    return handleNoHeadingOrPageError() if paragraph is None else paragraphScraper(paragraph)

@application.route("/wikiScraper/<string:title>/<string:heading>", methods=["Get"])
def wikiScraper(title: str, heading: str):
    toSend = wikipediaScraper(title, heading)
    return jsonify(toSend)

if __name__ == "__main__":
    application.run("127.0.0.1", 3021)
