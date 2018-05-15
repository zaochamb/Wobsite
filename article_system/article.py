import flask as f
import settings
import pandas as pd
import pathlib
import os

app = f.Blueprint('article', __name__)

@app.route('/articles/<art_name>')
@app.route('/articles')
def articles(art_name = ''):
    if art_name == '':
        articles = get_article_list()
        return f.render_template('article_system/Articles.html', articles = articles)
    return f.render_template('article_system/{}.html'.format(art_name))


def get_article_list():
    path = settings.get_dir_templates(pathlib.Path('article_system'))

    list_of_files = os.listdir(path)

    data = pd.DataFrame(data= {'name':list_of_files})
    data['name'] = data['name'].apply(lambda x: x.split('.')[0])
    data = data.set_index('name')
    data = data[data.index !='Articles']
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
        self.url = '/articles/{}'.format(name).replace(' ', '%20')
        return