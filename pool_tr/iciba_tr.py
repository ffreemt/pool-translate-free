"""

iciba

many-translaters

https://github.com/Chinese-boy/Many-Translaters/blob/master/iCIBA%E7%BF%BB%E8%AF%91.py

url0 = 'http://fy.iciba.com/ajax.php'
data1 =  {
    'a': 'fy',
    'f': 'auto',
    't': 'auto',
    'w': text,
}
# x res2 = requests.post(url0, data=data1)  # NOK
res2 = requests.get(f'{url0}?{urllib.parse.urlencode(data1)}')  # res2.json() OK

"""
import logging
from pathlib import Path
import re
import time
from random import random

import pytest

# from unittest import mock

# import urllib.parse
# urlencode
# parse_qs parse_qsl
# urlparse/urlunparse

# import json
# import requests
import requests_cache

# from urllib.parse import urlencode

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17"
HEADERS = {"User-Agent": UA}
HOME_FOLDER = Path.home()
CACHE_NAME = (Path(HOME_FOLDER) / (Path(__file__)).stem).as_posix()
EXPIRE_AFTER = 3600

# requests.post not cached in genreal? or just in this case, use requests_cache.CachedSession(): no go

requests_cache.install_cache()
requests_cache.core.configure(
    cache_name=CACHE_NAME,
    expire_after=EXPIRE_AFTER,
    allowable_codes=(200,),
    allowable_methods=("GET", "POST"),
)  # post ok

# requests_cache.configure(cache_name=CACHE_NAME, expire_after=EXPIRE_AFTER)  # 10 hours

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


def make_throttle_hook(timeout=1.0):
    """
    Returns a response hook function which sleeps for `timeout` seconds if
    response is not cached

    time.sleep(max(0, timeout - 0.5) + random())
        average delay: timeout

    s = requests_cache.CachedSession()
    s.hooks = {'response': make_throttle_hook(0.1)}
    s.get('http://httpbin.org/delay/get')
    s.get('http://httpbin.org/delay/get')
    """

    def hook(response, *args, **kwargs):  # pylint: disable=unused-argument
        if not getattr(response, "from_cache", False):
            # print(f'sleeping {timeout} s')

            timeout0 = max(0, timeout - 0.5) + random()
            LOGGER.debug("sleeping %s s", round(timeout0, 2))

            time.sleep(timeout0)
        return response

    return hook


def iciba_tr(text, from_lang="auto", to_lang="auto", timeout=(55, 65), cache=True):
    """
    text = 'this is a test'
    """
    try:
        text = str(text).strip()
    except Exception as exc:
        LOGGER.error("str(text).strip(): %s", exc)
        text = ""

    if not text:
        return ""

    # if all numbers, return original
    if not re.search(r"\D", text):
        return text

    url = "http://fy.iciba.com/ajax.php?a=fy"
    data = {
        "f": from_lang,
        "t": to_lang,
        "w": text,
    }

    # res = requests.get(f'{url}&{urllib.parse.urlencode(data)}')
    # jdata = res.json()  # OK

    # tmp = '''

    # post cache ok
    # res = requests_cache.core.CachedSession(

    # post cache ok
    sess = requests_cache.CachedSession(
        cache_name=CACHE_NAME,
        expire_after=EXPIRE_AFTER,
        allowable_methods=("GET", "POST"),
    )

    # s.hooks = {'response': make_throttle_hook(0.1)}
    sess.hooks = {"response": make_throttle_hook(1)}

    # '''
    # del tmp
    # res = None

    def fetch():
        """fetch"""
        # nonlocal res

        try:
            # res = requests.get(
            res = sess.post(
                url,
                data=data,
                # f'{url}&{urlencode(data)}',
                headers=HEADERS,
                timeout=timeout,
            )
            res.raise_for_status()
        except Exception as exc:  # pragma: no cover
            LOGGER.error("requests.post exc: %s", exc)
            res = str(exc)
            raise

        LOGGER.debug(" from_cache? %s", "from_cache" in dir(res) and res.from_cache)
        return res

    if cache:
        res = fetch()
    else:
        with requests_cache.disabled():
            res = fetch()

    # res.json()  # OK
    try:
        jdata = res.json()
    except Exception as exc:  # pragma: no cover
        LOGGER.error("jdata = res.json exc: %s", exc)
        raise

    content = jdata.get("content")

    iciba_tr.content = content

    if content:
        return content.get("out")

    return content  # pragma: no cover


def test_empty():
    """test space"""
    text = " "
    assert iciba_tr(text) == ""


@pytest.mark.parametrize("num, output", [("1", "1"), (1, 1), (2, 2), (3, 3), (4, 4)])
def test_numbers(num, output):
    """test_numbers: test numbers"""
    text = num
    assert iciba_tr(text) == str(output)


def test_1():
    """test 1: test 123"""
    text = "test 123"
    res = iciba_tr(text)
    assert "试验" in res or "123" in res
    # assert iciba_tr(text, cache=False) == '试验 123'


def main():  # pragma: no cover
    """main"""
    import sys

    from pool_tr.report_time import report_time

    fmt = "%(name)s-%(filename)s[ln:%(lineno)d]"
    # FORMAT += '%(asctime)s:'
    fmt += "%(levelname)s:\n\t%(message)s"
    logging.basicConfig(format=fmt, level=logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) < 2:
        print("Supply something to translate...")
        sys.exit(1)
    text = " ".join(sys.argv[1:])
    with report_time(" "):
        trtext = iciba_tr(text, from_lang="en", to_lang="zh")
    with report_time(" cache disabled "):
        trtext = iciba_tr(text, from_lang="en", to_lang="zh", cache=False)

    print(f"{text}, Trans: [{trtext}]")


if __name__ == "__main__":  # pragma: no cover
    main()
