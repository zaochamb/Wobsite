
import os


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')
APP_TEMPLATES = os.path.join(APP_ROOT, 'templates')
APP_DATABASE = os.path.join(APP_ROOT, 'database')

def get_dir_static(directory):
    return os.path.join(APP_STATIC, directory)


def get_dir_templates(directory):
    return os.path.join(APP_TEMPLATES, directory)

def get_database_dir(directory):
    return os.path.join(APP_DATABASE, directory)


def add_paths(path1, path2):
    return str(os.path.join(path1, path2))