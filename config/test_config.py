import configparser
from pathlib import Path

def _load() -> configparser.SectionProxy:
    props = configparser.ConfigParser()
    content = '[s]\n' + (Path(__file__).parent / 'test.properties').read_text(encoding='utf-8')
    props.read_string(content)
    return props['s']

_P = _load()

def get_base_url() -> str:  return _P['base.url']
def get_login() -> str: return _P['login']
def get_password() -> str: return _P['password']