import sys
from flask import Flask, render_template
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
from flask_sqlalchemy import SQLAlchemy

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
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item:item['date'], reverse=True)
    return render_template('index.html', posts=posts)

@app.route("/visitedcountries")
def visited_countries():
    from models import MapPhotos
    map_photos = MapPhotos.query.all()
    photos = [{"URL":photo.PhotoURL, "Lat":photo.Latitude,
               "Lon":photo.Longitude, "Date":photo.DateTaken} for photo in map_photos]
    return render_template('countries.html',photos=photos)

@app.route('/<name>/')
def post(name):
    path = '{}/{}'.format(POST_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post)

@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('friendly'), 200, {'Content-Type': 'text/css'}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', debug=True)