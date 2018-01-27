import requests
from bs4 import BeautifulSoup


## SCRAPING FACE TO FACE GAMES ##
url = 'http://www.facetofacegames.com/products/search?query=maxx+c'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'html.parser')
content_table = soup.find('table', attrs={'class': 'invisible-table products_table'})

f2f_res = []

#traverse each table row <tr>
for row in content_table.findAll('tr'):
    for meta_td in row.findAll('td', attrs={'class': 'meta'}): 
        cell_list = []
        if meta_td == '':
            continue;
        cell_list = meta_td.get_text(';', strip=True).split(';')
        f2f_res.append(cell_list[0:5])

## SCRAPING DOLLYS ##
url = 'http://www.dollys.ca/products/search?q=maxx+c'
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, 'html.parser')
content_list = soup.find('ul', attrs={'class': 'product-results'}) 

dollys_res = []

#sweet jesus unordered lists <ul> <li> <li> .....
for li in content_list.findAll('li'):
    print li.get_text(';', strip=True).split(';')



