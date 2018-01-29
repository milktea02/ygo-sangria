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

    card_name_query = card_init(data.lower())

    f = f2f_scrape(card_name_query)
    d = dolly_scrape(card_name_query)

    if len(f) > 10:
        f = f[:10]
    if len(d) > 10:
        d = d[:10]
    return render_template('cards.html', f_list = f, d_list = d)

def card_init(card_name):
    card_name_query = card_name.replace(' ', '+')
    return card_name_query


#################################
## SCRAPING FACE TO FACE GAMES ##
#################################
def f2f_scrape(card_name_query):
    f2f_res = []
    url = "http://www.facetofacegames.com/products/search?query={}".format(card_name_query)
    f2f_res, pages = f2f_scrape_helper(url, card_name_query)
    # Do we need to paginate?
    if pages > 0:
        for i in range(2, pages+1):
            url = "http://www.facetofacegames.com/products/search?page={}&query={}".format(i, card_name_query)
            f2f_res.extend(f2f_scrape_helper(url, card_name_query)[0])

    f2f_res.sort(key=itemgetter(3))
    return f2f_res

def f2f_scrape_helper(url, card_name_query):
    result_list = []
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    content_table = soup.find('table', attrs={'class': 'invisible-table products_table'})
    for row in content_table.findAll('tr'):
        for meta_td in row.findAll('td', attrs={'class': 'meta'}): 
            cell_list_raw = []
            cell_list = []
            # For whatever reason f2f renders empty cells so we need to check
            if meta_td == '':
                continue;
            cell_list_raw = (meta_td.get_text('%', strip=True).split('%'))
            if not (check_is_card(card_name_query, cell_list_raw[0])):
                continue;
            if cell_list_raw[2].lower() == 'no conditions in stock.': 
                cell_list = cell_list_raw[:2]
                if len(cell_list_raw) == 3:
                    cell_list.extend(['-', 0, '0'])
                else:
                    cell_list.extend(['-', remove_cad(cell_list_raw[3]), '0'])
            else:
                cell_list = cell_list_raw[:3]
                cell_list.append(remove_cad(cell_list_raw[3]))
                cell_list.append(keep_nums(cell_list_raw[4]))
            result_list.append(cell_list)

    pages = pagination(soup)
    return result_list, pages

#####################
## SCRAPING DOLLYS ##
#####################

def dolly_scrape(card_name_query):
    dollys_res = []
    url = "http://www.dollys.ca/products/search?q={}".format(card_name_query)
    dollys_res, pages = dolly_scrape_helper(url, card_name_query)

    if pages > 0:
        for i in range(2, pages+1):
            url = "http://www.dollys.ca/products/search?page={}&q={}".format(i, card_name_query)
            dollys_res.extend(dolly_scrape_helper(url, card_name_query)[0])
    
    dollys_res.sort(key=itemgetter(3))
    return dollys_res

def dolly_scrape_helper(url, card_name_query):
    result_list = []
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
        if not (check_is_card(card_name_query, li_list_raw[0])):
            continue;
        if li_list_raw[2] == 'Out of stock':
            li_list = li_list_raw[:2]
            li_list.extend(['-', remove_cad(li_list_raw[5]), '0'])
        else:
            li_list = li_list_raw[:2]
            li_list.extend([remove_trailing_comma(li_list_raw[4]), remove_cad(li_list_raw[2]), keep_nums(li_list_raw[5], False)])
        result_list.append(li_list)
    pages = pagination(soup)
    return result_list, pages

#############
## HELPERS ##
#############

def pagination(soup):
    pages = 0
    list_page_num = soup.select("div.pagination")[0].get_text(';', strip=True).split(';')
    if len(list_page_num) > 1:
        pages = int(soup.select("div.pagination")[0].get_text(';', strip=True).split(';')[-2])
    return pages

def check_is_card(query_card, result_card):
    query_card = query_card.replace("+", " ")
    result_card = result_card.lower().replace("\"", "")
    if query_card not in result_card:
        return False
    return True

#######################
## STUFF TO PRETTIFY ##
#######################

def remove_cad(cad):
    '''
    Remove the CAD$ from CAD$ 0.99
    '''
    return float(cad.replace('CAD$ ', ''))

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



