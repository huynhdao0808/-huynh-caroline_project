import requests
from bs4 import BeautifulSoup, re

BASE_URL = "https://moveek.com/en/" 

def get_URL(URL):
    """Get HTML from(URL)
    """
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def crawl_moveek(URL):
    soup = get_URL(URL)
    movies = soup.find_all(href=re.compile("/phim/"))
    movies_list = list()

    for movie in movies:
        _movie = {}
        if movie.img:
            _movie["title"] = movie["title"]
            _movie["link"] = movie["href"]
            _movie["img"] = movie.img["data-src"]
            movies_list.append(_movie)
    return movies_list
        
def crawl_rating(URL):
    movies_list = crawl_moveek(URL)
    for i in range(len(movies_list)):
        movie = movies_list[i]
        soup = get_URL("https://www.google.com/search?q="+movie["title"])
        try:
            movie["imdb_URL"] = soup.find(href=re.compile("imdb"))["href"].strip("/url?q=").split("&")[0]
            movie["rotten_URL"] = soup.find(href=re.compile("rotten"))["href"].strip("/url?q=").split("&")[0]
        except:
            pass
    return movies_list

movie = {}
soup = get_URL("https://moveek.com/en/phim/the-invisible-man/")
try:
    movie["gerne"] = soup.find(class_= "mb-0 text-muted text-truncate").string.strip().strip("-").strip()
    movie["description"] = soup.find(class_ = "mb-3 text-justify").text
    movie["rating"] = soup.find(href="/en/review/the-invisible-man/").text.strip()
except:
    pass
print(movie)