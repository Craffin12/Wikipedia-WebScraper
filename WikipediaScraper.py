from flask import Flask, jsonify
from bs4 import BeautifulSoup
from flask_cors import CORS
import requests

app = Flask(__name__)

CORS(app)  # Prevents the raising of restrictions due to CORS

"""
Used the official documentation 
https://beautiful-soup-4.readthedocs.io/en/latest/
to research general beautifulsoup 4 methods. All code is my own.
"""

def headingChoice(heading, html):
    """
    Navigates html object to heading, if "Overview" is passed navigated to text
    under title on Wikipedia Page and if no paragraph is found returns None.
    """
    if heading == "Overview":
        paragraph = html.find(id="mw-content-text")  # Find text right under title
        return None if paragraph is None else paragraph.contents[0].contents[0]
    else:
        paragraph = html.find(id=heading)
        return None if paragraph is None else paragraph.parent

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
            # label paragraph numbers
            collection["paragraph{}".format(count)] = paragraph.text
            count += 1
    return collection

def handleNoPageError():
    """Handles if there is not wikipedia page found"""
    paragraphDict = {}
    paragraphDict["err"] = "Title doesn't exist for a Wikipedia Page"
    return paragraphDict

def handleNoHeadingError():
    """Handles if there is no heading on current wikipedia page"""
    paragraphDict = {}
    paragraphDict["err"] = "Heading Not Found On Requested Page"
    return paragraphDict

def wikipediaScraper(title, heading):
    """
    Takes in a title for an ingredient and a heading (Overview/History), scrapes text
    off of Wikipedia page that corresponds to title/headign combo and returns text in a dictionary.
    """
    url = 'https://en.wikipedia.org/wiki/' + \
        title.replace(" ", "_")  # Change spaces to _ for url
    heading = heading.replace(" ", "_")
    resp = requests.get(url)  # get content of page
    if resp.status_code == 404:
        return handleNoPageError()  # If wiki page doesnt exist
    # Set up html object to parse
    htmlContent = BeautifulSoup(resp.text, "html.parser")
    # Target h2 tag on page for heading
    paragraph = headingChoice(heading, htmlContent)
    # If no paragraph returned, handle "error" else scrape all paragraphs under heading
    return handleNoHeadingError() if paragraph is None else paragraphScraper(paragraph)

@app.route('/wikiScraper/<string:title>/<string:heading>', methods=['Get'])
def wikiScraper(title: str, heading: str):
    response = wikipediaScraper(title, heading)
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=3021)
