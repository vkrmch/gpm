import os
import shutil
import pytest
from gpm import os as gpmos


def prepare_ls_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)

    for i in range(5):
        file = os.path.join(path, 'file' + str(i))
        with open(file, 'w') as f:
            f.write('test')


def remove_ls_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)


def test_ls():
    path = os.path.join(os.path.dirname(__file__), 'testfolder')
    remove_ls_folder(path)
    prepare_ls_folder(path)
    files = gpmos.ls(path=path)
    remove_ls_folder(path)
    assert len(files) == 5


def test_ls_recursive():
    path = os.path.join(os.path.dirname(__file__), 'testfolder')
    subpath = os.path.join(path, 'testsubfolder')
    remove_ls_folder(path)
    prepare_ls_folder(path)
    prepare_ls_folder(subpath)
    files = gpmos.ls(path=path, recursive=True)
    remove_ls_folder(path)
    assert len(files) == 11


def test_ls_recursive_files_only():
    path = os.path.join(os.path.dirname(__file__), 'testfolder')
    subpath = os.path.join(path, 'testsubfolder')
    remove_ls_folder(path)
    prepare_ls_folder(path)
    prepare_ls_folder(subpath)
    files = gpmos.ls(path=path, recursive=True, returnfilesonly=True)
    remove_ls_folder(path)
    assert len(files) == 10


def test_get_parent_folder_file():
    file = '/Users/maria/maria.txt'
    assert gpmos.get_parent_folder(file) == '/Users/maria'


def test_get_parent_folder_folder():
    file = '/Users/maria/'
    assert gpmos.get_parent_folder(file) == '/Users'


def test_get_file_extension():
    file = '/Users/maria/maria.txt'
    assert gpmos.get_file_extension(file) == 'txt'


def test_get_file_extension_no_ext():
    file = '/Users/maria/maria'
    assert gpmos.get_file_extension(file) is None


def test_get_file_extension_dot():
    file = '/Users/maria/maria.'
    assert gpmos.get_file_extension(file) is None


def test_get_file_extension_multipledots():
    file = '/Users/maria/maria..'
    assert gpmos.get_file_extension(file) is None


def test_get_file_extension_dot_in_front():
    file = '/Users/maria/.maria'
    assert gpmos.get_file_extension(file) is None


def test_get_file_extension_dot_in_front_multiple():
    file = '/Users/maria/.maria.hey'
    assert gpmos.get_file_extension(file) == 'hey'


def test_get_file_extension_multipleext():
    file = '/Users/maria/maria.hey.fine'
    assert gpmos.get_file_extension(file) == 'fine'


def test_get_filename_wo_extension():
    file = '/Users/maria/maria.hey.fine'
    assert gpmos.get_filename_wo_extension(file) == 'maria.hey'


def test_get_filename_wo_extension_folder():
    file = '/Users/maria/maria/'
    assert gpmos.get_filename_wo_extension(file) is None


def test_run():
    cmd = 'ls'
    out = gpmos.run(cmd)
    assert out['returncode'] == 0


def test_run_args():
    cmd = 'ls -la'
    out = gpmos.run(cmd)
    assert out['returncode'] == 0


def test_run_args_space():
    path = os.path.join(os.path.dirname(__file__), 'test folder')
    prepare_ls_folder(path)
    cmd = "ls -la '" + path + "'"
    out = gpmos.run(cmd)
    remove_ls_folder(path)
    assert out['returncode'] == 0


def test_run_args_space_invalid():
    path = os.path.join(os.path.dirname(__file__), 'test folder')
    prepare_ls_folder(path)
    cmd = "ls -la " + path
    out = gpmos.run(cmd)
    remove_ls_folder(path)
    assert out['returncode'] > 0
