from flask import Flask, render_template, request
import requests, sys
from bs4 import BeautifulSoup
from colorama import init , Fore, Style
init(autoreset=True)

app = Flask(__name__)

@app.route("/")

def index():
    return render_template('index.html')

@app.route("/cards", methods=['POST'])

def cards():
    data = request.form['data']
    print(data)
    f_url = ""
    d_url = ""
    if request.method == "POST":
        f_url, d_url = initialize(data)

    print(f_url)
    print(d_url)
    f = []
    d = []
    if f_url != "":
        f = f2f_scrape(f_url)
        d = dolly_scrape(d_url)

    if len(f) > 10:
        f = f[:10]
    if len(d) > 10:
        d = d[:10]
    return render_template('cards.html', f_list = f, d_list = d)

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
    for row in content_table.findAll('tr'):
        for meta_td in row.findAll('td', attrs={'class': 'meta'}): 
            cell_list_raw = []
            cell_list = []
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

if __name__ == "__main__":
    app.run(debug=True)



