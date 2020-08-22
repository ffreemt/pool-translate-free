"""
queue translate

q_services = deque(FREEMT_SERVICES)

service = q_services.popleft()

# do translate stuff

add back when finished
successful: q_services.insert(0, service)  # appendleft
empty or None: q_services.append(service)

# timeout? from wrapt_timeout_decorator import timeout

queue translate
"""
# import logging

from typing import (
    # Any,
    # List,
    # Deque,
    Optional,
    Tuple,
)

import importlib
from time import perf_counter

# import re

# from collections import deque
# import pytest  # type: ignore

# import coloredlogs  # type: ignore
# need six docutils jmespath urllib3 botocore certifi clickk idna joblib numpy

from wrapt_timeout_decorator import timeout

from logzero import logger

from pool_tr.with_func_attrs import with_func_attrs
from pool_tr.freemt_services import FREEMT_SERVICES
from pool_tr.q_services import Q_SERVICES

from sogou_tr import sogou_tr

# pip install -e pypi-projects\baidu-tr-free
from bdtr import bdtr

_ = """
try:
    FREEMT_SERVICES.pop("xiaoniu_tr")  # TODO： fix xiaoniu_tr iciba_tr?
    # FREEMT_SERVICES.pop("iciba_tr")
except Exception:
    ...
# """

# import tr modules
for elm in FREEMT_SERVICES:
    # equiv to from elm import elm
    if elm in ["omni_tr", "iciba_tr"]:
        globals()[elm] = getattr(importlib.import_module(f"pool_tr.{elm}"), elm)
    else:
        globals()[elm] = getattr(importlib.import_module(elm), elm)

# LOGGER = logging.getLogger(__name__)
# LOGGER.addHandler(logging.NullHandler())
# FMT = '%(filename)-18s[ln%(lineno)4d]%(funcName)-10s: %(message)s'
# coloredlogs.install(fmt=FMT, level=10, logger=LOGGER)


def _sogou_tr(text, from_lang, to_lang):
    from textwrap import wrap

    if from_lang in ["zh", "chinese"]:
        _ = wrap(text, 40)
        _ = [sogou_tr(elm, "zh", "en") for elm in _]
        return " ".join(_)

    return sogou_tr(text, from_lang, to_lang)


def _bdtr(text, from_lang, to_lang):
    from textwrap import wrap

    if from_lang in ["zh", "chinese"]:
        _ = wrap(text, 30)
        _ = [bdtr(elm, "zh", "en") for elm in _]
        return " ".join(_)

    return bdtr(text, from_lang, to_lang)


# @timeout(10)
# fmt:off
def translate(
        service: Optional[str], text: str, from_lang: str, to_lang: str
) -> Optional[str]:
    # fmt: on
    """ translate """

    if service is None:
        return None

    if service == "omni_tr":
        args = [text, to_lang]
    else:
        args = [text, from_lang, to_lang]

    try:
        if service == "sogou_tr":  # switch to _sogou_tr
            return globals()["_" + service](*args)

        if service == "bdtr":  # switch to _bdtr_tr
            return globals()["_" + service](*args)

        return globals()[service](*args)
    except Exception as exc:
        logger.error("service: %s, exc: %s", service, exc)
        return None


@with_func_attrs(service="")
# def queue_tr(text: List[str], from_lang: str = 'zh', to_lang: str = 'en', q_services: Deque[Any] = Q_SERVICES, popleft: bool = True) -> str:
# fmt: off
def queue_tr(
        text: str,
        from_lang: str = "zh",
        to_lang: str = "en",
        popleft: bool = True,
        appendleft: bool = True,
        preset: Optional[str] = None,  # preset service
) -> Tuple[Optional[str], Optional[str], float]:
    # fmt: on
    """ queue translate """

    then = perf_counter()

    # if preset serivce is not set, fetch from Q_SERVICES
    if preset is None:
        logger.debug("Q_SERVICES: %s", Q_SERVICES)
        if popleft:
            try:
                service = Q_SERVICES.popleft()
            except Exception as exc:
                logger.error("exc: %s", exc)
                # raise
                res = -1
                service = None
        else:
            try:
                service = Q_SERVICES.pop()
            except Exception as exc:
                logger.error("exc: %s", exc)
                # raise
                res = -1
                service = None

        logger.debug("service: *%s*", service)
        logger.debug("Q_SERVICES: %s", Q_SERVICES)

        queue_tr.service = service
    else:
        queue_tr.service = preset
        service = preset
        logger.debug("preset service: %s", service)

    # do_translate()
    try:
        res = translate(service, text, from_lang, to_lang)
    except OSError as exc:  # timeout error
        logger.error("%s", exc)
        res = None
    except Exception as exc:
        logger.error("%s", exc)
        res = None

    if res is None or not res.strip():
        if service is not None and preset is None:
            Q_SERVICES.append(service)
            logger.debug("appended: %s", service)
    elif appendleft:
        if service is not None and preset is None:
            Q_SERVICES.appendleft(service)
            logger.debug("preapended: %s", service)
            # q_services.append(service)
            # logger.info('apended: %s', service)
    else:
        if service is not None and preset is None:
            Q_SERVICES.append(service)
            logger.debug("preapended: %s", service)

    logger.debug(" Q_SERVICES: %s", Q_SERVICES)

    return res, service, round(perf_counter() - then, 2)
