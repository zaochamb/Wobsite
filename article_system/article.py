import flask as f


app = f.Blueprint('article', __name__)



@app.route('/articles')
def articles():
    return f.render_template('article_system/articles.html')