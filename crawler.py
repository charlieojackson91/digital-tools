from bs4 import BeautifulSoup
import requests
import re
import time
#from requests_html import HTMLSession



def Crawl_url(url):
    content = requests.get(url)
    html = content.text
    contents = html.encode('utf-8', "ignore")
    soup = BeautifulSoup(contents, 'html.parser')
    find_description = soup.find("meta",  property="og:description")
    find_links = soup.find_all('a')
    if find_description == None:
        description = "Unable to find meta description"
        title = soup.title.string
        link_count = len(find_links)
    else:
        description = find_description['content']
        title = soup.title.string
        link_count = len(find_links)
    return title, description, link_count


def Get_rankings(keyword):
    content = requests.get("https://www.google.co.uk/search?q="+keyword)
    html = content.text
    contents = html.encode('utf-8', "ignore")
    soup = BeautifulSoup(contents, 'html.parser')
    soups = str(soup)
    rank_clean = []
    rank = re.findall('<h3 class="r"><a href="(.*?)"',soups)
    for links in rank:
        find = links.find("&amp")
        final_url = links[7:find]
        rank_clean.append(final_url)
    return rank_clean


def Get_uat(url):
    # clean url
    if 'https://www.' in url:
        clean_url = url.replace('https://www.','')
    elif 'https://' in url:
        clean_url = url.replace('https://','')
    elif 'http://www.' in url:
        clean_url = url.replace('http://www.','')
    elif 'http://' in url:
        clean_url = url.replace('http://','')
    else:
        clean_url = 'Enter a valid url'
    check_serps = Get_rankings('site:' + clean_url + ' Lorem ipsum')
    uat_serps = Get_rankings('site:' + clean_url + 'inurl: uat')
    return check_serps
    
def JS_crawler(url):
    #session = HTMLSession()
    #source = session.get(inp)
    #links = source.html.links
    return url
