import flask as f
import settings
import pandas as pd
import pathlib
import os

app = f.Blueprint('article', __name__)
base_folder = 'Articles'


def get_main_template():
    return base_folder + '/main.html'


@app.route('/articles')
def re_routearticles():
    return f.redirect('/Articles')


@app.route('/Articles/<path:path>')
@app.route('/Articles', defaults={'path': ''})
def articles(path):
    if '.html' in path:
        return f.render_template(base_folder + '/' +  path.replace('%20', ' '))

    if '.html' not in path:
        links = get_links(path)
        if path == '':
            path = 'Articles'
        return f.render_template(get_main_template(),links = links, page_name = path.replace('.html', '') )


def get_links(subcategory):
    path = settings.add_paths(base_folder, subcategory)
    path = settings.get_dir_templates(pathlib.Path(path))

    list_of_files = os.listdir(path)

    data = pd.DataFrame(data={'name': list_of_files})
    data['filename'] = data['name'].copy().str.replace('%20', ' ')
    if subcategory != '':
        data['filename'] = subcategory + '/' + data['filename']

    def remove_html(name):
        return name.replace('.html', '')
    data['name'] = data['name'].apply(remove_html)
    data = data.set_index('name')
    data = data[data.index != 'main']
    data = data.sort_index()
    arts = []
    for index in data.index:

        filename = data.loc[index, 'filename']
        arts.append(Article(index, filename))
    return arts


class Article():
    name = None
    filename = None

    def __init__(self, name, filename):
        self.name = name
        self.filename = filename.replace(' ', '%20')
        return
