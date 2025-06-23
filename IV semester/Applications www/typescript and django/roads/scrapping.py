import requests
from bs4 import BeautifulSoup

def scrap(url, sessionid):
    response = requests.get(url, cookies={'sessionid': sessionid})
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = soup.find_all('a')
    count = len(links)
    
    
    return count

def scrap_pages():
    url = "https://www.best-pets.co.uk/"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    container = soup.find("div", class_= "container")
    
    snacks = container.find("ul", class_="offerproducts slick")
    list = []
    for ul in snacks.find_all("li"):
        
        name = ul.find("h5").get_text(strip=True)
        size = ul.find("p", class_="prodsize").get_text(strip=True)
        img = ul.find("p", class_="prodimage").find("img").get("src")
                        
        list.append({"name": name, "size": size, "img": img})
    return list
                
            
def create_html():
    list = scrap_pages()
    
    
        
        
        
    
    
scrap_pages()