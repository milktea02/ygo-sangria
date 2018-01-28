from __future__ import print_function

import requests, sys
from bs4 import BeautifulSoup
from colorama import init , Fore, Style
init(autoreset=True)

####################################################
## We want to format our data like so:
## Name of card | Pack | Language | Price | Number
##      0       |  1   |   2      |   3   |   4
## eg: Maxx "C" Common     | Structure Deck: Machine Reactor | Near Mint, English | 7.99 | 2
##     Maxx "C" Super Rare | Collector Tin Promos            | -                  | 8.99 | 0
#################################################### 
## LIMITATIONS:
## A lot
## Currently only checks the first condition available - eg, if a card has nm, and moderatly playe
## it'll only list the near mint one
## - currently cannot support pagination - only looks at first page results (rip MST)
####################################################

def initialize(card_name):
    query = card_name.replace(' ', '+')
    f2f_query = 'http://www.facetofacegames.com/products/search?query='+query
    dolly_query = 'http://www.dollys.ca/products/search?q='+query
    print("Using queries:\n", f2f_query, "\n", dolly_query)

    return(f2f_query, dolly_query)


#################################
## SCRAPING FACE TO FACE GAMES ##
#################################
def f2f_scrape(f2f_query):
    response = requests.get(f2f_query)
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
    	    if cell_list_raw[2] == 'No conditions in stock.': 
                cell_list = cell_list_raw[:2]
                cell_list.extend(['-', cell_list_raw[3], '0'])
            else:
                cell_list = cell_list_raw[:5]
            f2f_res.append(cell_list)
    return f2f_res

#####################
## SCRAPING DOLLYS ##
#####################

def dolly_scrape(dolly_query):
    response = requests.get(dolly_query)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    content_list = soup.find('ul', attrs={'class': 'product-results'}) 
    dollys_res = []
    #sweet jesus unordered lists <ul> <li> <li> .....
    for li in content_list.findAll('li'):
        li_list_raw = []
        li_list = []
        li_list_raw = li.get_text(';', strip=True).split(';')
        if li_list_raw[2] == 'Out of stock':
            li_list = li_list_raw[:2]
            li_list.extend(['-', li_list_raw[5], '0'])
        else:
            li_list = li_list_raw[:2]
            li_list.extend([li_list_raw[4], li_list_raw[2], li_list_raw[5]])
        dollys_res.append(li_list)
    return dollys_res

if __name__ == '__main__':
    print("Starting", sys.argv[0], "...")
    print("...")

    if len(sys.argv) < 2:
        print("Usage: python scrape.py 'card name'")
        print("\twhere the card name should not have any special characters")
        print("teg. $ python scrape.py 'maxx c'")
        print("exiting....")
        exit()

    card_name = sys.argv[1]
    print("Searching for:", card_name)
    f, d = initialize(card_name)
    f2f = f2f_scrape(f)
    dolly = dolly_scrape(d)

    print() 
    print("NAME | PACK |\nCONDITION | PRICE | STOCK")
    print(Fore.CYAN + "=========== SHOWING RESULTS FOR FACE TO FACE GAMES ==============")
    for row in f2f:
        print(row[0] + "\t|" + row[1])
        print(row[2] + "\t|" + row[3] + "\t|" + row[4] + "\n")

    print(Fore.CYAN + "\n=========== SHOWING RESULTS FOR DOLLYS TOYS & GAMES ==============")
    for row in dolly:
        print(row[0] + "\t|" + row[1])
        print(row[2] + "\t|" + row[3] + "\t|" + row[4] + "\n")


