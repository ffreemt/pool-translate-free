"""
prob and reorder/remove services

"""
# import logging
import importlib

from random import randint
from typing import List, Any, Tuple
from collections import deque
from pprint import pprint

# import coloredlogs  # type: ignore

from logzero import logger

from pool_tr.freemt_services import FREEMT_SERVICES  # type: ignore
from pool_tr.report_time import report_time

# from pool_tr.queue_tr import _sogou_tr

# from pool_tr.queue_tr import _sogou_tr  # pylint: disable=unused-import  # needed in line 41  # noqa

_ = """
try:
    FREEMT_SERVICES.pop('xiaoniu_tr')
except KeyError:
    ...
# """

# import tr modules
for _ in FREEMT_SERVICES:
    # equiv to from _ import _
    if _ in ["omni_tr", "iciba_tr"]:
        globals()[_] = getattr(importlib.import_module(f"pool_tr.{_}"), _)
    else:
        globals()[_] = getattr(importlib.import_module(_), _)

# LOGGER = logging.getLogger(__name__)
# LOGGER.addHandler(logging.NullHandler())
# FMT = '%(filename)-18s[ln%(lineno)-4d]: %(message)s [%(funcName)s]'
# coloredlogs.install(fmt=FMT, level=20)

Q_SERVICES = deque(FREEMT_SERVICES)


def translate(service, text, from_lang, to_lang):
    """ translate """  # pylint: disable=duplicate-code
    if service == "omni_tr":
        args = [text, to_lang]
    else:
        args = [text, from_lang, to_lang]

    try:
        if service == "sogou_tr":
            return globals()["_" + service](*args)

        return globals()[service](*args)
    except Exception as exc:
        logger.error("service: %s, exc: %s", service, exc)
        return None


def probe_services(cutoff: float = 10) -> Tuple[Any, Any, Any]:
    """ prob services disregard services with response time > cutoff time"""

    pairs = []  # type: List[Tuple[Any, Any, Any]]
    text = "test" + " " + str(randint(1, 10000))  # type: str
    from_lang = "en"  # type: str
    to_lang = "zh"  # type: str
    for _ in Q_SERVICES:
        with report_time():
            res = translate(_, text, from_lang, to_lang)
        pairs.append((_, report_time.time_elapsed, res))

    pairs = []
    tail = randint(1, 10000)
    text = "test" + " " + str(tail)
    for _ in Q_SERVICES:
        with report_time():
            res = translate(_, text, from_lang, to_lang)
        pairs.append((_, report_time.time_elapsed, res))
        logger.info("%s, %s, %s", _, report_time.time_elapsed, res)
    pairs = sorted(pairs, key=lambda _: _[1])
    # logger.info('%s', pairs)
    pprint(pairs)

    # res is not None, time_elapsed leq cutoff, '测试' or tail in res

    # valid = [elm[0] for elm in pairs if elm[2] is not None and elm[1] < cutoff and ('试验' in elm[2] or '测试' in elm[2] or str(tail) in elm[2])]  # noqa
    valid = []  # type: List[Any]
    invalid = []  # type: List[Any]
    for elm in pairs:
        # fmt: off
        if elm[2] is not None and float(elm[1]) < cutoff and (
                "试验" in elm[2] or "测试" in elm[2]
                or str(tail) in elm[2]):  # noqa  # fmt: on
            valid += [elm[0]]
        else:
            invalid += [elm[0]]
        # fmt: on
    return valid, invalid, pairs


def main():
    """main"""
    # log_fmt = '%(filename)-12s %(lineno)6d %(levelname)-6s: %(message)s'
    # logging.basicConfig(format=log_fmt, level=20)

    # logging.basicConfig(level=20)
    # root_logger = logging.getLogger()
    # root_logger.level = 20

    print(probe_services())


if __name__ == "__main__":
    main()

# Q_SERVICES = deque(probe_services()[0])
