from flask import Flask, render_template, request
import requests, sys, time
from bs4 import BeautifulSoup
from operator import itemgetter
from multiprocessing import Pool
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])

def cards():
<<<<<<< HEAD
<<<<<<< HEAD

=======
    hide_zero = request.form.getlist('hide_zero')
    app.logger.info("Should hide zero? ", repr(hide_zero))
>>>>>>> wip
=======

>>>>>>> add flag to no display out of stock cards
    if request.method == "GET":
        return render_template('cards.html', f_list=[], d_list=[], card_name='', time=0)
    
    ## POST
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> add flag to no display out of stock cards
    hide_zero = False
    if request.form.get('hide_zero'):
        hide_zero = True
    app.logger.info("Should hide zero? " + repr(hide_zero))
<<<<<<< HEAD
=======
>>>>>>> wip
=======
>>>>>>> add flag to no display out of stock cards
    data = request.form.get('data')
    card_name_query = card_init(data.lower())
    app.logger.info("Searching: " + data + " using query: " + card_name_query)
    start = time.time()
    f = f2f_scrape(card_name_query, hide_zero)
    d = dolly_scrape(card_name_query, hide_zero)

    if len(f) > 10:
        f = f[:10]
    if len(d) > 10:
        d = d[:10]
    end = time.time()
    load_time = repr(round(end-start,2))
    app.logger.info("Time: " + load_time)
    return render_template('cards.html', f_list = f, d_list = d, card_name=data, time=load_time)

def card_init(card_name):
    card_name_query = card_name.replace(' ', '+').replace('&', '%26').strip()
    return card_name_query


#################################
## SCRAPING FACE TO FACE GAMES ##
#################################
def f2f_scrape(card_name_query, hide_zero):
    f2f_res = []
    url = "http://www.facetofacegames.com/products/search?query={}".format(card_name_query)
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    content_table = soup.find('table', attrs={'class': 'invisible-table products_table'})
    if content_table == None:
        return f2f_res
    pages = pagination(soup)
    # Do we need to paginate?
    if pages > 0:
        p = Pool(pages)
        args = []
        cards = []
        for i in range(1, pages + 1):
            url = "http://www.facetofacegames.com/products/search?page={}&query={}".format(i, card_name_query)
            args.append((url, card_name_query, hide_zero))
        results = p.starmap(f2f_scrape_helper, args)
        p.terminate()
        p.join()
        for x in results:
            f2f_res.extend(x)
    else:
        f2f_res = f2f_scrape_helper(url, card_name_query, hide_zero)
    
    f2f_res.sort(key=itemgetter(3))
    return f2f_res

def f2f_scrape_helper(url, card_name_query, hide_zero):
    result_list = []
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    content_table = soup.find('table', attrs={'class': 'invisible-table products_table'})
    for content_row in content_table.findAll('tr'):
        for meta_td in content_row.findAll('td', attrs={'class': 'meta'}): 
            cell_list_raw = []
            row = []
            # For whatever reason f2f renders empty cells so we need to check
            if meta_td == '':
                continue; # skip this row
<<<<<<< HEAD
            card_link = "http://www.facetofacegames.com/" + meta_td.a.get('href')
            app.logger.info("Link for this card: " + str(card_link))
=======
>>>>>>> add flag to no display out of stock cards
            cell_list_raw = (meta_td.get_text('@', strip=True).split('@'))
            card_name = cell_list_raw[0]
            card_set = cell_list_raw[1]
            card_cond = cell_list_raw[2]
            card_price = 0
            card_quantity = 0
            if not (check_is_card(card_name_query, card_name)):
                continue;
            if card_cond.lower() == 'no conditions in stock.': 
                if hide_zero:
                    continue; # skip this card
                row = [card_name, card_set]
                if len(cell_list_raw) == 3:
                    row.extend(['-', 0, '0'])
                else:
                    card_price = remove_cad(cell_list_raw[3])
                    row.extend(['-', card_price, '0'])
            else:
                card_cond = cell_list_raw[2]
                card_price = (remove_cad(cell_list_raw[3]))
                card_quantity = (keep_nums(cell_list_raw[4]))
                row = [card_name, card_set, card_cond, card_price, card_quantity]
<<<<<<< HEAD
            row.append(card_link)
=======
>>>>>>> add flag to no display out of stock cards
            result_list.append(row)
    return result_list

#####################
## SCRAPING DOLLYS ##
#####################

def dolly_scrape(card_name_query, hide_zero):
    dollys_res = []
    url = "http://www.dollys.ca/products/search?q={}".format(card_name_query)
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    content_list = soup.find('ul', attrs={'class': 'product-results'})
    if content_list == None:
        return dollys_res
    pages = pagination(soup)

    if pages > 0:
        p = Pool(pages)
        args = []
        for i in range(1, pages+1):
            url = "http://www.dollys.ca/products/search?page={}&q={}".format(i, card_name_query)
            args.append((url, card_name_query, hide_zero))
        results = p.starmap(dolly_scrape_helper, args)
        p.terminate()
        p.join()
        for x in results:
            dollys_res.extend(x)
    else:
        dollys_res = dolly_scrape_helper(url, card_name_query, hide_zero)

    
    dollys_res.sort(key=itemgetter(3))
    return dollys_res

def dolly_scrape_helper(url, card_name_query, hide_zero):
    result_list = []
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    content_list = soup.find('ul', attrs={'class': 'product-results'}) 
    dollys_res = []
    #sweet jesus unordered lists <ul> <li> <li> .....
    card_name = ''
    card_set = ''
    card_cond = ''
    card_price = 0
    card_quantity = 0
    for li in content_list.findAll('li'):
        app.logger.info("dolly's listing [li.a.get('href')]: " + str(li.a.get('href')))
        card_link = "http://www.dollys.ca" + li.a.get('href')
        li_list_raw = []
        li_list = []
        li_list_raw = li.get_text('@', strip=True).split('@')
        card_name = li_list_raw[0];
        card_set = li_list_raw[1]
        card_cond = li_list_raw[2]
        li_list = [card_name, card_set]
        if not (check_is_card(card_name_query, card_name)):
            continue;
        if card_cond == 'Out of stock':
            app.logger.info("Card is out of stock")
            if hide_zero:
                app.logger.info("skipping card that is out of stock")
                continue; #skip this row
            li_list.extend(['-', remove_cad(li_list_raw[5]), '0'])
        else:
            card_cond = remove_trailing_comma(li_list_raw[4])
            card_price = remove_cad(li_list_raw[2])
            card_quantity = keep_nums(li_list_raw[5], False)
            li_list.extend([card_cond, card_price, card_quantity])
<<<<<<< HEAD
        li_list.append(card_link)
=======
>>>>>>> add flag to no display out of stock cards
        result_list.append(li_list)
    return result_list

#############
## HELPERS ##
#############

def pagination(soup):
    pages = 0
    pagination_div_list = soup.select("div.pagination")
    if len(pagination_div_list) > 0:
        list_page_num = pagination_div_list[0].get_text(';', strip=True).split(';')
        if len(list_page_num) > 1:
            pages = list_page_num[-2]
            try:
                pages = int(pages)
            except ValueError:
                pages = int(list_page_num[-3])
    return pages

def check_is_card(query_card, result_card):
    ## too lazy to figure out regex
    query_card = query_card.replace("+", " ").replace("\"", "").replace(":", "").replace("\'", "")
    result_card = result_card.lower().replace("\"", "").replace(":", "").replace("\'", "").replace("&", "%26")
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
    handler = RotatingFileHandler('cards.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)
