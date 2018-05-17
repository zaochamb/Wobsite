import flask as f
import settings
import pandas as pd
import pathlib
import os

app = f.Blueprint('article', __name__)
base_folder = 'Articles'


@app.route('/articles')
def re_routearticles():
    return f.redirect('/Articles')


@app.route('/Articles/<subcategory>')
@app.route('/Articles')
def articles(subcategory=''):
    if '.html' not in subcategory:



        links = get_links(subcategory)


        if subcategory == '':
            subcategory = 'Articles'
        return f.render_template('/Articles/main.html', page_name=subcategory, links = links)

    if '.html' in subcategory:
        f.render_template(subcategory)

    return


def get_links(subcategory):
    path = settings.add_paths(base_folder, subcategory)
    path = settings.get_dir_templates(pathlib.Path(path))

    list_of_files = os.listdir(path)

    data = pd.DataFrame(data={'name': list_of_files})
    data['filename'] = data['name'].copy()
    data['filename'] = subcategory + '/'+ data['filename'].str.replace('%20', ' ')

    data['name'] = data['name'].apply(lambda x: x.split('.')[0])
    data = data.set_index('name')
    data = data[data.index != 'Articles']
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
