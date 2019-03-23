import os
import shutil
import json
import pytest
from gpm import config


def prepare_config_file(c):
    c_data = {
        'test': True
    }

    with open(c._file_path, 'w') as outfile:
        json.dump(c_data, outfile)


def prepare_invalid_config_file(c):
    with open(c._file_path, 'w') as outfile:
        outfile.write('test')


def remove_config_folder(folder=None):
    if folder is None:
        folder = os.path.join(os.path.dirname(__file__), 'cfg')

    if os.path.exists(folder):
        shutil.rmtree(folder, ignore_errors=True)


def test_no_param():
    remove_config_folder()
    c = config.Config(script='')
    with pytest.raises(FileNotFoundError):
        c.read()
    remove_config_folder()


def test_file_does_not_exist():
    remove_config_folder()
    c = config.Config(script=__file__)
    with pytest.raises(FileNotFoundError):
        c.read()
    remove_config_folder()


def test_valid_config_variable():
    remove_config_folder()
    c = config.Config(script=__file__, create=True)
    prepare_config_file(c)
    c.read()
    assert c.test
    remove_config_folder()


def test_create_file():
    remove_config_folder()
    c = config.Config(script=__file__, create=True)
    c.read()

    assert os.path.exists(c._file_path)
    remove_config_folder()


def test_invalid_config():
    remove_config_folder()
    c = config.Config(script=__file__, create=True)
    prepare_invalid_config_file(c)
    with pytest.raises(json.decoder.JSONDecodeError):
        c.read()
    remove_config_folder()


def test_custom_cfg_dir():
    cfg_dir = os.path.join(os.path.dirname(__file__), 'config')
    remove_config_folder(cfg_dir)
    c = config.Config(script=__file__, create=True, cfg_dir=cfg_dir)
    assert os.path.exists(os.path.join(cfg_dir, c._file))
    remove_config_folder(cfg_dir)


def test_custom_cfg_dir_invalid():
    cfg_dir = '/config'
    with pytest.raises(PermissionError):
        c = config.Config(script=__file__, create=True, cfg_dir=cfg_dir)


def test_custom_cfg_file():
    cfg_file = 'config.json'
    remove_config_folder()
    c = config.Config(script=__file__, create=True, cfg_file=cfg_file)
    assert os.path.exists(os.path.join(c._dir, cfg_file))
    remove_config_folder()


def test_custom_cfg_dir_file():
    cfg_dir = os.path.join(os.path.dirname(__file__), 'config')
    cfg_file = 'config.json'
    remove_config_folder(cfg_dir)
    c = config.Config(script=__file__, create=True, cfg_dir=cfg_dir, cfg_file=cfg_file)
    assert os.path.exists(os.path.join(cfg_dir, cfg_file))
    remove_config_folder(cfg_dir)
