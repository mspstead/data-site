import sys
from flask import Flask, render_template
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
from flask_sqlalchemy import SQLAlchemy
import datetime

DEBUG = True

app = Flask(__name__)

FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_MARKDOWN_EXTENSIONS = ['fenced_code','codehilite']
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog-site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

flatpages = FlatPages(app)
freezer = Freezer(app)
app.config.from_object(__name__)
db = SQLAlchemy(app)

@app.route("/")
def posts():
    title = "Blog Home"
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item:item['date'], reverse=True)
    return render_template('index.html', posts=posts, title=title)

@app.route("/about")
def about_me():
    title = "About Me"
    return render_template('about.html',title=title)

@app.route("/portfolio")
def portfolio():
    title = "Portfolio Analytics"
    basket_composition = {
        "BasketComposition": [
            {"Identifier": "VFEM.L", "Shares": 10},
            {"Identifier": "VWRL.L", "Shares": 40},
            {"Identifier": "VMID.L", "Shares": 30}
        ],
        "Currency": "GBP",
        "StartDate": "2019-10-01",
        "EndDate": datetime.datetime.today().strftime("%Y-%m-%d")
    }
    return render_template('portfolio.html',title=title, basket_composition=basket_composition)

@app.route("/visitedcountries")
def visited_countries():
    from models import MapPhotos
    title = "Country Tracker"
    map_photos = MapPhotos.query.all()
    photos = [{"URL":photo.PhotoURL, "Lat":photo.Latitude,
               "Lon":photo.Longitude, "Date":photo.DateTaken} for photo in map_photos]
    return render_template('countries.html',photos=photos, title=title)

@app.route('/<name>/')
def post(name):
    title = "Tech Blog"
    path = '{}/{}'.format(POST_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post, title=title)

@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('friendly'), 200, {'Content-Type': 'text/css'}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', debug=True)