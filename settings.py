
import os


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')
APP_TEMPLATES = os.path.join(APP_ROOT, 'templates')

def get_dir_static(directory):
    return os.path.join(APP_STATIC, directory)


def get_dir_templates(directory):
    return os.path.join(APP_TEMPLATES, directory)