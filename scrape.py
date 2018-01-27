import requests
from bs4 import BeautifulSoup

####################################################
## We want to format our data like so:
## Name of card | Pack | Condition | Language | Price | Number
##      0       |  1   |    2      |   3      |   4   |   5
## eg: Maxx "C" Common     | Structure Deck: Machine Reactor | Near Mint | English | 7.99 | 2
##     Maxx "C" Super Rare | Collector Tin Promos            | -         | -       | 8.99 | 0
#################################################### 


#################################
## SCRAPING FACE TO FACE GAMES ##
#################################

url = 'http://www.facetofacegames.com/products/search?query=maxx+c'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'html.parser')
content_table = soup.find('table', attrs={'class': 'invisible-table products_table'})

f2f_res = []

#traverse each table row <tr>
for row in content_table.findAll('tr'):
    for meta_td in row.findAll('td', attrs={'class': 'meta'}): 
        cell_list_raw = []
        cell_list = []
        # For whatever reason f2f renders empty cells so we need to check
        if meta_td == '':
            continue;
        cell_list_raw = (meta_td.get_text(';', strip=True).split(';'))
	if cell_list_raw[2] == ' No conditions in stock.': 
	    cell_list = cell_list_raw[:2]
            cell_list.extend(['-', '-'])
            cell_list.append(cell_list_raw[3]
        else:
            cell_list = cell_list_raw[:6]
        f2f_res.append(cell_list)

print f2f_res

#####################
## SCRAPING DOLLYS ##
#####################

url = 'http://www.dollys.ca/products/search?q=deskbot+001'
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, 'html.parser')
content_list = soup.find('ul', attrs={'class': 'product-results'}) 

dollys_res = []

#sweet jesus unordered lists <ul> <li> <li> .....
for li in content_list.findAll('li'):
    li_list_raw = []
    li_list = []
    li_list_raw = li.get_text(';', strip=True).split(';')
    dollys_res.append(li_list_raw)

for row in f2f_res:
    print row

for row in dollys_res:
    print row
