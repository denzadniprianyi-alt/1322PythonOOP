import requests

html = requests.get('http://books.toscrape.com').text

parsed_text = html.split('<p class="price_color">')

prices = []

for text in parsed_text:
    if "£" in text:
        price_text = text.split('</p>')
        for price in price_text:
            if "£" in price:
                prices.append(price[1:])

print(prices)