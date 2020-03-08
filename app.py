from flask import Flask, render_template

import requests
from bs4 import BeautifulSoup, re


app = Flask(__name__)

MOVEEK_URL = "https://moveek.com/en/"
HBO_URL = "https://www.hbo.com/series"

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


def crawl_rating_moveek(URL):
    movies_list = crawl_moveek(URL)
    for i in range(len(movies_list)):
        movie = movies_list[i]
        soup = get_URL("https://moveek.com"+movie["link"])
        movie["gerne"] = soup.find(class_ = "mb-0 text-muted text-truncate").string.strip().strip("-").strip()
        try:
            movie["description"] = soup.find(class_ = "mb-3 text-justify").text
        except:
            if "description" not in movie:
                soup=get_URL("https://moveek.com/"+movie["link"].strip("/en"))
                movie["description"] = soup.find(class_ = "mb-3 text-justify").text
        movie["rating"] = soup.find(href = re.compile("/review/")).text.strip()
        if movie["rating"] == "Reviews" or movie["rating"] == "Đánh giá":
            movie["rating"] = "No Review"
    return movies_list

def crawl_hbo(URL):
    soup = get_URL(URL)
    movie_list = []
    movies = soup.find_all(class_="components/Card--card components/Card--promotional components/Card--withBottomBorder")
    for movie in movies:
        _movie = {}
        _movie["title"] = movie.find(class_="components/CardText--title").string
        _movie["link"] = "https://www.hbo.com"+movie["href"]
        _movie["img"] = "https://www.hbo.com" + movie.find(class_="components/CardImage--imageContainer").img["src"]
        try:
            _movie["description"] = movie.find(class_="components/CardText--details").p.string
            _movie["show_time"] = movie.find(class_="components/CardText--contextualLabel").string
        except:
            pass
        movie_list.append(_movie)
    return movie_list

@app.route('/')
def movies():
  data=crawl_rating_moveek(MOVEEK_URL)
  return render_template('movies.html', data=data)

@app.route('/series')
def series():
  data=crawl_hbo(HBO_URL)
  return render_template('series.html', data=data)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
