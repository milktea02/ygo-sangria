### YGO-Sangria

Web scraper for Canadian YGO card sellers:
- Face to Face Games
- Dollys Toys & Games

### What does it do
- So far it doesn't do anything other than gather information from both sites and prints it to console

### Usage and Example
```
$ python scrape.py 'deskbot 002'
Starting scrape.py ...
...
Searching for: deskbot 002

NAME | PACK |
CONDITION | LANGUAGE | PRICE | STOCK
=========== SHOWING RESULTS FOR FACE TO FACE GAMES ==============
Deskbot 002 - DUEA-ENDE5 - Super Rare - Limited Edition |Duelist Alliance - DUEA
Near Mint       | English       |CAD$ 0.99      |x 8

Deskbot 002 - MP15-EN156 - Common - 1st Edition |Mega Pack 2015 - MP15
Near Mint       | English       |CAD$ 0.25      |x 9

Deskbot 002 - NECH-EN042 - Common - 1st Edition |The New Challengers - NECH
-       |-      |CAD$ 0.25      |0

Deskbot 002 - NECH-EN042 - Common - Unlimited Edition   |The New Challengers - NECH
-       |-      |CAD$ 0.25      |0


=========== SHOWING RESULTS FOR DOLLYS TOYS & GAMES ==============
Deskbot 002 - DUEA-ENDE5 - Super Rare - Limited Edition |Duelist Alliance
Near Mint,      |English        |CAD$ 1.29      |6 in-stock

Deskbot 002 - MP15-EN156 - Common - 1st Edition |Mega Tins 2015
Near Mint,      |English        |CAD$ 0.65      |6 in-stock

Deskbot 002 - NECH-EN042 - Common - 1st Edition |New Challengers (The)
Near Mint,      |English        |CAD$ 0.39      |6 in-stock

Deskbot 002 - NECH-EN042 - Common - Unlimited Edition   |New Challengers (The)
Near Mint,      |English        |CAD$ 0.25      |3 in-stock

```

### Limitations
- it's slow as hell
- Doesn't support pagination, ie. it only looks at first page
- if f2f or dollys ever changes their theme RIP
- only takes first card available from booster/deck, eg if near mint and slightly played are available for purchase it'll list the near mint one because it is first

### Requirements:
- python 2.7 (not compatible with python 3.xx)
- `pip install beautifulsoup4` https://www.crummy.com/software/BeautifulSoup/bs4/doc/

You can run it using virtualenv to keep things clean https://virtualenv.pypa.io/en/stable/

#### Ubuntu
```
### install virtualenv using apt or pip
sudo apt-get install python-virtualenv
### start the env (ours is called dev)
source dev/bin/activate
### get out of the env
deactivate
```
#### Windows
You can install virtualenv here: http://pymote.readthedocs.io/en/latest/install/windows_virtualenv.html  
Recommend to use virtualenv with windows

### Why
I was drinking a sangria while having dinner and decided to make a web scraper for fun.


