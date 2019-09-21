import os

from utils import save_json, load_json


PATH = '/tmp/t.json'
INVALID_PATH = '/tmp/not-existed.json'
DATA = {'a': 3, 'b': 5}
CONTENT = """\
{
  "a": 3,
  "b": 5
}"""


def test_save_json():
    save_json(DATA, PATH)
    with open(PATH) as f:
        assert f.read() == CONTENT
    os.remove(PATH)


def test_load_json():
    with open(PATH, 'w') as f:
        f.write(CONTENT)
    assert load_json(PATH) == DATA
    os.remove(PATH)


def test_load_json_with_default():
    assert load_json(INVALID_PATH) == {}
    assert load_json(INVALID_PATH, {'foo': 'bar'}) == {'foo': 'bar'}
