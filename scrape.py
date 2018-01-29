import requests, sys
from bs4 import BeautifulSoup
from colorama import init , Fore, Style
from operator import itemgetter
from multiprocessing import Pool
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

def card_init(card_name):
    card_name_query = card_name.replace(' ', '+')
    return card_name_query


#################################
## SCRAPING FACE TO FACE GAMES ##
#################################
def f2f_scrape(card_name_query):
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
        urls = []
        cards = []
        for i in range(1, pages + 1):
            url = "http://www.facetofacegames.com/products/search?page={}&query={}".format(i, card_name_query)
            urls.append((url, card_name_query))
        results = p.starmap(f2f_scrape_helper, urls)
        p.terminate()
        p.join()
        for x in results:
            f2f_res.extend(x)
    else:
        f2f_res = f2f_scrape_helper(url, card_name_query)
    
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

    return result_list

#####################
## SCRAPING DOLLYS ##
#####################

def dolly_scrape(card_name_query):
    dollys_res = []
    url = "http://www.dollys.ca/products/search?q={}".format(card_name_query)
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    content_list = soup.find('ul', attrs={'class': 'product-results'})
    if content_list == None:
        return dollys_res
    pages = pagination(soup)
    dollys_res = dolly_scrape_helper(url, card_name_query)

    if pages > 0:
        p = Pool(pages)
        args = []
        for i in range(1, pages+1):
            url = "http://www.dollys.ca/products/search?page={}&q={}".format(i, card_name_query)
            args.append((url, card_name_query))
        results = p.starmap(dolly_scrape_helper, args)
        p.terminate()
        p.join()
        for x in results:
            dollys_res.extend(x)
    else:
        dollys_res = dolly_scrape_helper(url, card_name_query)

    
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
            pages = int(soup.select("div.pagination")[0].get_text(';', strip=True).split(';')[-2])
    return pages

def check_is_card(query_card, result_card):
    ## too lazy to figure out regex
    query_card = query_card.replace("+", " ").replace("\"", "").replace(":", "").replace("\'", "")
    result_card = result_card.lower().replace("\"", "").replace(":", "").replace("\'", "")
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


if __name__ == '__main__':
    print("Starting", sys.argv[0], "...")
    print("...")

    if len(sys.argv) < 2:
        print(Fore.RED + "Usage: python scrape.py 'card name'")
        print("\twhere the card name should not have any special characters")
        print("\teg. $ python scrape.py 'maxx c'")
        print("exiting....")
        exit()

    card_name = sys.argv[1].lower()
    print("Searching for:", card_name)
    card_name_query = card_init(card_name)

    f2f = f2f_scrape(card_name_query)
    dolly = dolly_scrape(card_name_query)

    print() 
    print(Fore.GREEN + "NAME | PACK |\nCONDITION | PRICE | STOCK")
    print(Fore.CYAN + "=========== SHOWING RESULTS FOR FACE TO FACE GAMES ==============")
    for row in f2f:
        print(row[0] + "\t|" + row[1])
        print(row[2] + "\t|" + str(row[3]) + "\t|" + row[4] + "\n")

    print(Fore.CYAN + "\n=========== SHOWING RESULTS FOR DOLLYS TOYS & GAMES ==============")
    for row in dolly:
        print(row[0] + "\t|" + row[1])
        print(row[2] + "\t|" + str(row[3]) + "\t|" + row[4] + "\n")
