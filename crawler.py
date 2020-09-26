import csv, pandas as pd, time, requests
from bs4 import BeautifulSoup

metacriticURL = 'https://www.metacritic.com'
data = pd.read_csv('mc.csv')
data['fullurl'] = metacriticURL + data['url']
print(data['fullurl'][0])

def getGenreDev(link):
    url = link
    userAgent = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=userAgent)
    soup = BeautifulSoup(response.text, 'html.parser')
    genreListItems = soup.find_all('li', {"class":"summary_detail product_genre"})
    genre = genreListItems[0].find_all('span', {"class":"data"})
    devlistItems = soup.find_all('li', {"class":"summary_detail developer"})
    developer = devlistItems[0].find_all('span', {"class":"data"})
    genres = [i.text for i in genre]
    return developer[0].text.strip(), genres

#print(getGenreDev(data['fullurl'][0]))
data['developer'] = ""
data['genre'] = ""
index = 0
while index < data.shape[0]: #need to fix to be the length of data set
    print(index)
    # if requests.get(data['fullurl'][index]).status_code == 200:
    #     pass
    # else:
    #     index +=1
    try:
        data['developer'].loc[index] = (getGenreDev(data['fullurl'][index])[0])
        data['genre'].loc[index] = (getGenreDev(data['fullurl'][index])[1])
    except:
        data['developer'].loc[index] = "No Data"
        data['genre'].loc[index] = "No Data"
    index += 1
    time.sleep(3.25)    
data.to_csv('metacritic_output.csv')
