from flask import Flask, render_template, request
import requests, sys
from bs4 import BeautifulSoup
from operator import itemgetter

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])

def cards():
    if request.method == "GET":
        return render_template('cards.html', f_list=[], d_list=[])
    
    ## POST
    data = request.form['data']
    print(data)
    f_url = ""
    d_url = ""
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
                cell_list.extend(['-', remove_cad(cell_list_raw[3]), '0'])
            else:
                cell_list = cell_list_raw[:3]
                cell_list.append(remove_cad(cell_list_raw[3]))
                cell_list.append(keep_nums(cell_list_raw[4]))
            f2f_res.append(cell_list)
    f2f_res.sort(key=itemgetter(3))
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
            li_list.extend([remove_trailing_comma(li_list_raw[4]), remove_cad(li_list_raw[2]), keep_nums(li_list_raw[5], False)])
        dollys_res.append(li_list)
    dollys_res.sort(key=itemgetter(3))
    return dollys_res

def remove_cad(cad):
    '''
    Remove the CAD$ from CAD$ 0.99
    '''
    return cad.replace('CAD$ ', '')

def keep_nums(stock, f = True):
    '''
    Only keep the quanity number
    f: x 5 -> 5
    d: 1 in-stock -> 1
    '''
    if f:
        return stock.replace('x ', '')
    return stock.replace(' in-stock', '')

def remove_trailing_comma(string):
    if len(string) > 0:
        return string[:-1]
    return ""

if __name__ == "__main__":
    app.run(debug=True)



