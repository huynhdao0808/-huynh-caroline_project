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

soup = get_URL("https://www.hbo.com/series")
#print(soup.prettify()[10000:20000])
movie_list = []
movies = soup.find_all(class_="components/Card--card components/Card--promotional components/Card--withBottomBorder")
for movie in movies:
    _movie = {}
    _movie["title"] = movie.find(class_="components/CardText--title").string
    _movie["link"] = "https://www.hbo.com"+movie["href"]
    _movie["img"] = "https://www.hbo.com"+movie.find(class_="components/CardImage--imageContainer").img["src"]
    try:
        _movie["description"] = movie.find(class_="components/CardText--details").p.string
        _movie["show_time"] = movie.find(class_="components/CardText--contextualLabel").string
    except:
        pass
    movie_list.append(_movie)
#print(movies.prettify())
for movie in movie_list:
    print(movie)

#for mo in movies:
#    vie = {}
 #   if movie.img:
  #      _movie["title"] = movie["title"]
   #     _movie["link"] = movie["href"]
    #    _movie["img"] = movie.img["data-src"]
     #   movies_list.append(_movie)
    