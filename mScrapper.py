import requests, csv, pandas as pd, pprint, time
from bs4 import BeautifulSoup
import lxml,html5lib

data_dict = {'name':[], 'date':[], 'platform': [], 'score':[], 'url':[], 'userscore':[]} # Data Structure

def webpage(pageNum,year): #function that navigates the metacritic SRP(Search Results Pages) based on the page number and the year
    url = 'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected='+ str(year) +'&distribution=&sort=desc&view=condensed&page='+ str(pageNum)
    userAgent = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=userAgent)
    return response

def numberPages(response): # Helper Function that determines how many pages are in a SRP to know how many times to run scrapper function
    soup = BeautifulSoup(response.text, 'html.parser')
    pages = soup.find_all('li', {"class":"page last_page"})
    pagesCleaned = pages[0].find('a', {"class":"page_num"})
    return (pagesCleaned.text)

def scrapper(num_loops,content):
    tblnum = 0
    while tblnum < num_loops:
        #get Game name
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            for a in td[1].find_all('a', {"class":"title"}):
                data_dict['name'].append(a.find('h3').text)
                #print(a.find('h3').text)

        #get Game release date
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            for date in td[1].find_all('span',{"class":""}):
                data_dict['date'].append(date.text)
                #print(date.text)

        #get platform
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            for platform in td[1].find_all('span',{"class":"data"}):
                data_dict['platform'].append(platform.text.strip())
                #print(platform.text.strip())

        #get Game score
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            for user in td[0].find_all('div',{"class":"metascore_w"}):
                data_dict['score'].append(user.text.strip())
                #print(user.text.strip())

        #getting game url
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            for a in td[1].find_all('a', {"class":"title"} ,href=True):
                data_dict['url'].append(a['href'])
                #print(a['href'])

        #get Game userscore
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            for score in td[1].find_all('div', {"class":"metascore_w"}):
                data_dict['userscore'].append(score.text)
                #print(score.text)
        tblnum += 1

def pages(lastPageNum, year): #Function that returns the html(code) and initiates the web scrapper
    currentPage = 0
    while currentPage < int(lastPageNum):
        url = url = 'https://www.metacritic.com/browse/games/score/metascore/year/all/filtered?year_selected='+ str(year) +'&distribution=&sort=desc&view=condensed&page=' + str(currentPage)
        userAgent = {'User-agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=userAgent)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find_all('table')

        num_loops = len(content)
        #print(num_loops)
        scrapper(num_loops,content)
        #print(data_dict)
        currentPage += 1
        print(currentPage)
        time.sleep(6)

def main():
    years = list(range(2015,2021))
    for year in years:
        numPage = (numberPages(webpage(0,year)))
        pages(int(numPage),year)
        time.sleep(5)
        print(year)
    xData = (pd.DataFrame.from_dict(data_dict))
    xData.to_csv('mc.csv')

# file1= open("sample_html","w")
# file1.write(webpage(0,2020).text)
# file1.close()
# #print(webpage(0,2020).text)
main()