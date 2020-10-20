import requests
import bs4
import csv

links = []

def getNextPage(URL):
    response = requests.get(URL)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    next = soup.find("li", {"class": "next"})
    if next is not None:
        next_link = next.find("a")['href']
        links.append(f"http://quotes.toscrape.com/{next_link}")
        return getNextPage(f"http://quotes.toscrape.com/{next_link}")

def extract(URL):
    response = requests.get(URL)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    quote_box = soup.find("div", {"class": "quote"})
    quote = quote_box.find("span", {"class": "text"})
    
    author = quote_box.find("small", {"class": "author"})

    return {
        "quote": quote.text,
        "author": author.text
    }

URL = "http://quotes.toscrape.com/"

links.append(URL)
getNextPage(URL)

quotes = []
for i in range(0,len(links)):
    quote = extract(links[i])
    quotes.append(list(quote.values()))

with open("quote.csv", 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Quote", "Author"])

    for i in range(0,len(quotes)):
        writer.writerow(quotes[i])