"""
check free mt service response time
"""
from random import randint
import importlib

from pool_tr.freemt_services import FREEMT_SERVICES
from pool_tr.report_time import report_time


def random_tail():
    """ random tail. """
    return " " + str(randint(1, 10000))


for _ in FREEMT_SERVICES:
    # equiv to from elm import elm
    globals()[_] = getattr(importlib.import_module(_), _)


def main():
    """ main """
    import logging

    logging.basicConfig(level=20)

    for elm in FREEMT_SERVICES:
        with report_time(elm):
            if elm == "omni_tr":
                # print(elm, globals()[elm]('测试 123', 'en'))
                args = ("测试" + random_tail(), "en")
            else:
                # print(elm, globals()[elm]('测试 123', 'zh', 'en'))
                args = ("测试" + random_tail(), "zh", "en")

            try:
                res = globals()[elm](*args)
            except TimeoutError:
                res = "timed out"
            print(" " * 10, elm, res)


if __name__ == "__main__":
    main()
