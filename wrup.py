import base64
import os
import os.path
import shutil
from urlparse import urljoin
from datetime import datetime

import click
import requests


IMPORTED_DIR = '_Imported'
REST_API_ROOT_PATH = 'wp-json'
REST_API_POSTS_PATH = 'posts'


@click.command()
@click.option('--url', prompt=True)
@click.option('--username', prompt=True)
@click.password_option()
def wrup_cli(url, username, password):
    uploaded = []
    failed = []
    click.echo('Posts uploaded to %s' % url)
    for file_ in post_list(u'.'):
        post = post_from_path(file_)
        if upload(url, username, password, post):
            uploaded.append(file_)
            _move_imported(file_, IMPORTED_DIR)
        else:
            failed.append(file_)
    report(uploaded, failed)


def report(succ, failed):
    def print_(file_list):
        for el in file_list:
            print el
    if succ:
        print 'Successful uploads:'
        print_(succ)

    print
    if failed:
        print 'Failed uploads:'
        print_(failed)


def encoded_creds(username, password):
    return base64.b64encode('%s:%s' % (username, password))


def upload(url, username, password, post):
    headers = {'Authorization': 'Basic %s' % encoded_creds(username, password)}
    resp = requests.post(make_url(url), params=post, headers=headers)
    return resp.status_code == 201


def post_from_path(path):
    date = datetime.fromtimestamp(os.path.getmtime(path))
    return {'data[date]': date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'data[title]': os.path.splitext(path)[0],
            'data[content_raw]': open(path).read()}


def make_url(url):
    return urljoin(url, REST_API_ROOT_PATH) + '/' + REST_API_POSTS_PATH


def post_list(path):
    return (f for f in os.listdir(path) if os.path.splitext(f)[1] == '.txt')


def _move_imported(src_file, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    shutil.move(src_file, target_dir)


if __name__ == '__main__':
    wrup_cli()
