import os

from nose import with_setup
from click.testing import CliRunner

from wrup import wrup_cli, _move_imported


def create_posts():
    posts = ['test_post1.txt', 'test_post2.txt', 'test_post3.txt']
    for name in posts:
        f = open(name)
        f.write()


def create_posts_with_imported():
    posts = ['test_post1.txt', 'test_post2.txt', 'test_post3.txt',
             '_Imported/test_imported_post1.txt']
    for name in posts:
        f = open(name)
        f.write()


def delete_posts():
    posts = ['test_post1.txt', 'test_post2.txt', 'test_post3.txt',
             '_Imported/test_imported_post1.txt']
    for name in posts:
        try:
            os.remove(name)
        except OSError:
            pass
    try:
        os.remove('_Imported')
    except OSError:
        pass


def remove_directory():
    try:
        os.rmdir('_Imported')
    except OSError:
        pass


class TestInterface:

    def test_upload_exit_code(self):
        runner = CliRunner()
        result = runner.invoke(wrup_cli,
                               input='http://url\nlogin\npass\npass\n')

        assert result.exit_code == 0

    @with_setup(remove_directory, remove_directory)
    def test_imported_directory_not_exists(self):
        """
        Directory '_Importted' with imported posts does not exist
        when running tool

        """
        runner = CliRunner()
        runner.invoke(wrup_cli,
                      input='http://url\nlogin\npass\npass\n')

        assert os.path.exists('_Imported')
        assert os.path.isdir('_Imported')

    @with_setup(None, remove_directory)
    def test_imported_directory_exists(self):
        """
        Directory '_Imported' with imported posts exists when running
        tool

        """
        runner = CliRunner()
        runner.invoke(wrup_cli,
                      input='http://url\nlogin\npass\npass\n')

        assert os.path.exists('_Imported')
        assert os.path.isdir('_Imported')

    @with_setup(create_posts, delete_posts)
    def test_files_moved_to_empty_directory(self):
        runner = CliRunner()
        runner.invoke(wrup_cli,
                      input='http://url\nlogin\npass\npass\n')

        assert os.path.exists('_Imported/test_post1.txt')
        assert os.path.exists('_Imported/test_post2.txt')
        assert os.path.exists('_Imported/test_post3.txt')

        assert not os.path.exists('test_post1.txt')
        assert not os.path.exists('test_post2.txt')
        assert not os.path.exists('test_post3.txt')

    @with_setup(create_posts_with_imported, delete_posts)
    def test_files_moved_to_not_empty_directory(self):
        runner = CliRunner()
        runner.invoke(wrup_cli,
                      input='http://url\nlogin\npass\npass\n')

        assert os.path.exists('_Imported/test_post1.txt')
        assert os.path.exists('_Imported/test_post2.txt')
        assert os.path.exists('_Imported/test_post3.txt')
        assert os.path.exists('_Imported/test_imported_post1.txt')

        assert not os.path.exists('test_post1.txt')
        assert not os.path.exists('test_post2.txt')
        assert not os.path.exists('test_post3.txt')

    @with_setup(create_posts_with_imported, delete_posts)
    def test_move_only_txt_files(self):
        runner = CliRunner()
        runner.invoke(wrup_cli,
                      input='http://url\nlogin\npass\npass\n')

        assert os.path.exists('not_moved.file')
        assert os.path.exists('_Imported/test_post1.txt')
        assert os.path.exists('_Imported/test_post2.txt')
        assert os.path.exists('_Imported/test_post3.txt')
        assert os.path.exists('_Imported/test_imported_post1.txt')

        assert not os.path.exists('_Imported/not_moved.file')
        assert not os.path.exists('test_post1.txt')
        assert not os.path.exists('test_post2.txt')
        assert not os.path.exists('test_post3.txt')


class TestFunctions:
    @with_setup(create_posts, delete_posts)
    def test_move_imported_post():
        _move_imported('test_post1.txt', '_Imported')

        assert os.path.exists('_Imported/test_post1.txt')
        assert not os.path.exists('test_post1.txt')
