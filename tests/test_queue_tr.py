"""
"""

import re
from random import randint

import pytest
from logzero import logger

from pool_tr.queue_tr import queue_tr
from pool_tr.q_services import Q_SERVICES

# import eventlet
# eventlet.monkey_patch()


def random_tail(text="test", lang="en"):
    """ gen a random tail of integer str """
    if lang in ["zh"]:
        text = "测试"
    return text + " " + str(randint(1, 10000))


def test_1():
    """ test 1 """
    # from random_tail import tandom_tail

    # service = 'systran_tr'
    text = random_tail()
    from_lang = "en"
    to_lang = "zh"
    args = [text, from_lang, to_lang]
    # res, service = queue_tr(*args)
    res, service, time_ = queue_tr(*args, appendleft=False)
    print(text, res, service)

    _ = """
    with capsys.disabled():
        print(args, res, queue_tr.service, )
        logger.info('capsys.disabled() res: %s', res)
    """
    logger.info("res: %s", res)
    logger.info("service: %s", service)
    numb = re.search(r"\d+", text).group()
    assert "测试" in res or numb in res


def test_2():
    """ test 2 """
    # from random_tail import tandom_tail

    # service = 'systran_tr'
    text = random_tail()
    from_lang = "en"
    to_lang = "zh"
    # popleft = 0: pop from right
    args = [text, from_lang, to_lang, 0]
    res, service, time_ = queue_tr(*args)
    _ = """
    with capsys.disabled():
        print(args, res, queue_tr.service, )
        logger.info('capsys.disabled() res: %s', res)
    """

    logger.info("res: %s", res)
    logger.info("service: %s", service)
    numb = re.search(r"\d+", text).group()
    assert "测试" in res or numb in res


_ = r"""
@pytest.mark.timeout(60)
def test_systran():
    ''' test systran '''
    # from random_tail import tandom_tail

    # service = 'systran_tr'
    while 1:
        service = Q_SERVICES.pop()
        if service == 'systran_tr':
            Q_SERVICES.append(service)
            break
        # Q_SERVICES.insert(0, service)
        Q_SERVICES.appendleft(service)
    logger.info(' service: %s', service)

    text = random_tail()
    from_lang = 'en'
    to_lang = 'zh'
    # popleft = 0: pop from right
    args = [text, from_lang, to_lang, 0]
    res, service = queue_tr(*args)
    _ = '''
    with capsys.disabled():
        print(args, res, queue_tr.service, )
        logger.info('capsys.disabled() res: %s', res)
    '''
    # print('print res: ', res)
    logger.info('res: %s', res)
    numb = re.search(r'\d+', text).group()
    assert '测试' in res or numb in res
"""


def test_omni():
    """ test omni """
    # from random_tail import tandom_tail

    # service = 'omni_tr'
    service = ""
    while 1:
        service = Q_SERVICES.pop()
        if service == "omni_tr":
            Q_SERVICES.append(service)
            break
        # Q_SERVICES.insert(0, service)
        Q_SERVICES.appendleft(service)
    logger.info(" service: %s", service)

    text = random_tail()
    from_lang = "en"
    to_lang = "zh"
    # popleft = 0: pop from right
    args = [text, from_lang, to_lang, 0]
    res, service, time_ = queue_tr(*args)
    _ = """
    with capsys.disabled():
        print(args, res, queue_tr.service, )
        logger.info('capsys.disabled() res: %s', res)
    """
    # print('print res: ', res)
    logger.info("res: %s", res)
    numb = re.search(r"\d+", text).group()
    assert "测试" in res or numb in res


def test_qq():
    """ test qq """
    # from random_tail import tandom_tail

    # service = 'qq_tr'
    service = ""
    while 1:
        service = Q_SERVICES.pop()
        if service == "qq_tr":
            Q_SERVICES.append(service)
            break
        Q_SERVICES.insert(0, service)
    logger.info(" service: %s", service)

    text = random_tail()
    from_lang = "en"
    to_lang = "zh"
    # popleft = 0: pop from right
    args = [text, from_lang, to_lang, 0]
    res, service, time_ = queue_tr(*args)
    _ = """
    with capsys.disabled():
        print(args, res, queue_tr.service, )
        logger.info('capsys.disabled() res: %s', res)
    """

    logger.info("res: %s", res)
    numb = re.search(r"\d+", text).group()
    assert "测试" in res or numb in res


def test_google():
    """ test google """
    # from random_tail import tandom_tail

    service_ = "google_tr"
    service = ""
    while 1:
        service = Q_SERVICES.pop()
        if service == service_:
            Q_SERVICES.append(service)
            break
        Q_SERVICES.insert(0, service)
    logger.info(" service: %s", service)

    text = random_tail()
    from_lang = "en"
    to_lang = "zh"
    # popleft = 0: pop from right
    args = [text, from_lang, to_lang, 0]
    res, service, time_ = queue_tr(*args)
    _ = """
    with capsys.disabled():
        print(args, res, queue_tr.service, )
        logger.info('capsys.disabled() res: %s', res)
    """
    # print('print res: ', res)
    logger.info("res: %s", res)
    numb = re.search(r"\d+", text).group()
    assert "测试" in res or numb in res


def test_sogou():
    """ test sogou """
    # from random_tail import tandom_tail

    service_ = "google_tr"
    service = ""
    service_ = "sogou_tr"
    while 1:
        service = Q_SERVICES.pop()
        if service == service_:
            Q_SERVICES.append(service)
            break
        Q_SERVICES.insert(0, service)
    logger.info(" service: %s", service)

    text = random_tail()
    from_lang = "en"
    to_lang = "zh"
    # popleft = 0: pop from right
    args = [text, from_lang, to_lang, 0]
    res, service, time_ = queue_tr(*args)

    # print('print res: ', res)
    logger.info("res: %s", res)
    numb = re.search(r"\d+", text).group()
    assert "测试" in res or numb in res


def test_baidu():
    """ test baidu. """
    # from random_tail import tandom_tail

    service_ = "google_tr"
    service = ""
    service_ = "sogou_tr"
    service_ = "bdtr"
    while 1:
        service = Q_SERVICES.pop()
        if service == service_:
            Q_SERVICES.append(service)
            break
        # Q_SERVICES.insert(0, service)
        Q_SERVICES.appendleft(service)
    logger.info(" service: %s", service)

    text = random_tail()
    from_lang = "en"
    to_lang = "zh"
    # popleft = 0: pop from right
    args = [text, from_lang, to_lang, False]
    res, service, time_ = queue_tr(*args)

    # print('print res: ', res)
    logger.info("res: %s", res)
    numb = re.search(r"\d+", text).group()
    assert "测试" in res or numb in res


@pytest.mark.parametrize("service_name", ["sogou_tr", "bdtr", "googleapis_translate"])
def test_param(service_name):
    """ test google """
    # from random_tail import tandom_tail

    service_ = service_name
    logger.info("service_name: %s", service_name)
    # r"""
    service = ""
    while 1:
        service = Q_SERVICES.pop()
        if service == service_:
            Q_SERVICES.append(service)
            break
        Q_SERVICES.insert(0, service)
    logger.info(" service: %s", service)

    text = random_tail()
    from_lang = "en"
    to_lang = "zh"
    # popleft = 0: pop from right
    args = [text, from_lang, to_lang, 0]
    res, service = queue_tr(*args)
    _ = """
    with capsys.disabled():
        print(args, res, queue_tr.service, )
        logger.info('capsys.disabled() res: %s', res)
    """

    logger.info("res: %s", res)
    numb = re.search(r"\d+", text).group()
    assert "测试" in res or numb in res
    # """


_ = '''
def main():
    """ main """
    _ = random_tail()
# '''
