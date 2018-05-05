
import os


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')


def get_dir(directory):
    return os.path.join(APP_STATIC, directory)