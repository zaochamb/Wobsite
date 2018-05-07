import flask as f
import settings
import pandas as pd
import pathlib

app = f.Blueprint('article', __name__)

@app.route('/articles/<art_name>')
@app.route('/articles')
def articles(art_name = ''):
    if art_name == '':
        articles = get_article_list()
        return f.render_template('article_system/articles.html', articles = articles)
    return f.render_template('article_system/{}.html'.format(art_name))


def get_article_list():
    dir = settings.get_dir(pathlib.Path('article_system', 'articles.csv'))
    data = pd.read_csv(dir)
    data = data.set_index('name')
    arts = []
    for index in data.index:
        arts.append(make_article(index))
    return arts

def make_article(name):
    art = Article(name)
    return art

class Article():
    name = None
    url = None

    def __init__(self, name):
        self.name = name
        self.url = '/articles/{}'.format(name.lower())
        return
