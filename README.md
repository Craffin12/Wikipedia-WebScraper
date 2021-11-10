# Wikipedia-WebScraper
Wikipedia Webscraper

Request:

Send 'Get' request in the form 'http://127.0.0.1:5000/wikiScraper/title/heading' where http://127.0.0.1:5000 is replaced by 
wherever you are running the app locally.
Also, title and heading are the title of the Wikipedia page you would like scraped and heading is the h2 heading you would like all of the paragraphs from.

Response:
Keep in mind that the app will return ALL paragraph elements on the page between that h2 tag and the next h2 tag.

{
"paragraph1" : "text",
"paragraph2" : "text",
"paragraph3" : "text",
             .
             .
             .
  "err" : "error text" ----> only appears if there is an error, either you have requested a page that doesn't exist or you have requested a heading that doesn't exist on 
  the title page
}
