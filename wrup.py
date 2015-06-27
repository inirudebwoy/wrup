import click


@click.command()
@click.option('--url', prompt=True)
@click.option('--login', prompt=True)
@click.password_option()
def wrup_cli(url, login, password):
    click.echo('Posts uploaded to %s' % url)


def _move_imported(src_file, target_dir):
    pass

if __name__ == '__main__':
    wrup_cli()
