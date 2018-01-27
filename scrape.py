import requests
from bs4 import BeautifulSoup

url = 'http://www.facetofacegames.com/products/search?query=maxx+c'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'html.parser')
content_table = soup.find('table', attrs={'class': 'invisible-table products_table'})

res = []

#traverse each table row <tr>
for row in content_table.findAll('tr'):
    cell_list = []
    for meta_td in row.findAll('td', attrs={'class': 'meta'}): 
        if meta_td == '':
            continue;
        print meta_td.get_text(";", strip=True)
