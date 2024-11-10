from bs4 import BeautifulSoup
import requests
import pandas as pd
import random

response = requests.get('https://www.mimuw.edu.pl/') 
soup = BeautifulSoup(response.text, 'html.parser')

events_section = soup.find('div', class_='news-grid')
events = events_section.find_all('div', class_='news-item')

events_data = []

for event in events:
    title = event.find('h3').text
    date = event.find('div', class_='news-item-text-date').text
    url = None  # Domyślnie brak linku
    link = event.find('span', class_='more')
    
    # Sprawdzam czy link istieje
    if link:
        
        url = link.find('a')['href']
        if not url.startswith('http'):
            url = 'https://www.mimuw.edu.pl' + url # uzupełniam link
    

    events_dict = {
        'title': title,
        'date': date,
        'url': url
    }
    
    events_data.append(events_dict)

df = pd.DataFrame(events_data)
df.to_csv('news_data.csv', index=False, encoding='utf-8')

random_news = random.sample(events_data, 5)
for news in random_news:
    print(f"Tytuł: {news['title']}")
    print(f"Data: {news['date']}")
    print(f"Link: {news['url']}\n")