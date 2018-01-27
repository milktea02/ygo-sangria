### YGO-Sangria

Web scraper for Canadian YGO card sellers:
- Face to Face Games
- Dollys Toys & Games

### What does it do
- So far it doesn't do anything other than gather information from both sites and prints it to console

### Usage
```
python scrape.py 'deskbot 001'

```

### Limitations
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

