from flask import Flask, render_template

from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

BASE_URL = "https://vnexpress.net/"

r = requests.get(BASE_URL)
print(r)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
 