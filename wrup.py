import os.path
from os import listdir
import shutil

import click

IMPORTED_DIR = '_Imported'


@click.command()
@click.option('--url', prompt=True)
@click.option('--login', prompt=True)
@click.password_option()
def wrup_cli(url, login, password):
    click.echo('Posts uploaded to %s' % url)
    for f in post_list('.'):
        if upload(f):
            _move_imported(f, IMPORTED_DIR)

    # print report


def upload(path):
    """
    Should return Bool

    """
    # this will upload if I dig into API
    return True


def post_list(path):
    return (f for f in listdir(path) if os.path.splitext(f)[1] == '.txt')


def _move_imported(src_file, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    shutil.move(src_file, target_dir)


if __name__ == '__main__':
    wrup_cli()
