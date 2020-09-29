import csv, pandas as pd, time, requests
from bs4 import BeautifulSoup

metacriticURL = 'https://www.metacritic.com'
data = pd.read_csv('mc.csv')
data['fullurl'] = metacriticURL + data['url']
#print(data['fullurl'][0])

def getGenreDev(link):
    url = link
    userAgent = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=userAgent)
    soup = BeautifulSoup(response.text, 'html.parser')
    #Getting Genre from HTML
    genreListItems = soup.find_all('li', {"class":"summary_detail product_genre"})
    genre = genreListItems[0].find_all('span', {"class":"data"})
    #Getting Developer from HTML
    devlistItems = soup.find_all('li', {"class":"summary_detail developer"})
    developer = devlistItems[0].find_all('span', {"class":"data"})
    genres = [i.text for i in genre] #list comprehension to consolidate games with multiple genres
    #Getting Number of user ratings
    numberratings = soup.find_all('span', {"class":"count"})
    ratings = numberratings[1].find_all('a') 
    return developer[0].text.strip(), genres, ratings[0].text.split(' ')[0]


#print(getGenreDev(data['fullurl'][0]))
data['developer'] = ""
data['genre'] = ""
data['no_userreviews'] = ""
index = 0
while index < data.shape[0]: #need to fix to be the length of data set
    print(index) #for troubleshooting
    try:
        data['developer'].loc[index] = (getGenreDev(data['fullurl'][index])[0]) #looks at the row represented by (loc[index]) and sets that equal to the first output of the "getGenreDev" function
        data['genre'].loc[index] = (getGenreDev(data['fullurl'][index])[1])
        data['no_userreviews'].loc[index] = (getGenreDev(data['fullurl'][index])[2])
    except:
        data['developer'].loc[index] = "No Data"
        data['genre'].loc[index] = "No Data"
        data['no_userreviews'].loc[index]
    index += 1
    time.sleep(3.25)    
data.to_csv('metacritic_output.csv')

