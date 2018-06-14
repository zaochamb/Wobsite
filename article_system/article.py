import flask as f
import settings
import pandas as pd
import pathlib
import os
import datetime

app = f.Blueprint('article', __name__)
base_folder = 'Articles'


def get_main_template():
    return base_folder + '/main.html'


@app.route('/articles')
def re_routearticles():
    return f.redirect('/Articles')


def get_last_modified_date(path):
    x = settings.add_paths(base_folder, path)
    x = settings.get_dir_templates(pathlib.Path(x))
    x = os.path.getmtime(x)
    x = datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d')
    return x


def get_hub_name(path):
    x = path.replace('\\', '/')
    last_name = path.split('/')[-1]
    x = x + '/' + last_name + '.html'
    return x


@app.route('/Articles/<path:path>')
@app.route('/Articles', defaults={'path': ''})
def articles(path):

    path = path.replace('+', ' ')
    path = path.replace('%20', ' ')
    links = get_links(path)
    if '.html' in path:


        last_modified_date = get_last_modified_date(path)
        return f.render_template(base_folder + '/' +  path, links = links, last_modified_date = last_modified_date)

    if '.html' not in path:


        try:
            hubname = get_hub_name(path)
            last_modified_date = get_last_modified_date(hubname)
            return f.render_template(base_folder+'/' + hubname, links = links, last_modified_date = last_modified_date)
        except FileNotFoundError:
            pass


        if path == '':
            path = 'Articles'
        return f.render_template(get_main_template(),links = links, page_name = path.replace('.html', '') )


def get_links(subcategory):
    if subcategory.endswith('.html'):
        subcategory = subcategory.replace('\\', '/')
        subcategory = '/'.join(subcategory.split('/')[:-1])

    path = settings.add_paths(base_folder, subcategory)
    path = settings.get_dir_templates(pathlib.Path(path))

    list_of_files = os.listdir(path)

    data = pd.DataFrame(data={'name': list_of_files})
    data['filename'] = data['name'].copy().str.replace('+', ' ')
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
        self.filename = filename.replace(' ', '+')
        return
