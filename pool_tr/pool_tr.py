"""
pool_tr

pool_exec = ThreadPoolExecutor(len(FREEM_SERVICES))

"""
# pylint: disable=too-many-locals

from typing import List, Any, Tuple, Dict, Deque, Optional, Union

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from collections import deque

from logzero import logger

# from load_paras import load_paras
from pool_tr.read_text import read_text
from pool_tr.report_time import report_time
from pool_tr.with_func_attrs import with_func_attrs
from pool_tr.queue_tr import queue_tr

from pool_tr.freemt_services import FREEMT_SERVICES  # type: ignore
from pool_tr.q_services import Q_SERVICES  # type: ignore

# from pool_tr.queue_tr import _sogou_tr  # special handling when from_lang='zh'

# LOGGER = logging.getLogger(__name__)
# LOGGER.addHandler(logging.NullHandler())


def get_batch(q_s) -> List[str]:
    """ get n items from deque q_s"""

    batch = []  # type: List[str]
    # for _ in range(n):
    while 1:
        try:
            batch += [q_s.popleft()]
        except IndexError:  # empty deque
            break
    return batch


# fmt: off
@with_func_attrs(result="", dist="", rdict="")
def pool_tr(
        sents: List[str],
        # services: List[str] = None,
        max_workers: Optional[int] = -1,
        timeout: float = 100,
) -> List[Any]:
    # fmt: on
    """ translate sents to English """

    _ = """
    if services is None:
        services = FREEMT_SERVICES
    # """

    if max_workers is None or max_workers <= 0:
        max_workers = len(Q_SERVICES)
    pool_exec = ThreadPoolExecutor(max_workers)

    resu = []  # type: List[Any]

    sent_idx_list = [
        *zip(sents, range(len(sents)))
    ]  # type: List[Tuple[Union[str, int], Union[str, int]]]
    q_sents = deque(
        sent_idx_list
    )  # type: Deque[Tuple[Union[str, int], Union[str, int]]]

    # preventive measure: None of the service returns anything
    # other than None or '' or ' '
    loop_ = 0
    while q_sents:
        batch = get_batch(q_sents)  # type: List[str]
        fut_dict = {}  # type: Dict[Any, Any]
        for elm in batch:
            sent, idx = elm
            # queue_tr => res, service
            args = [queue_tr, sent, "zh", "en"]  # type: List[Any]
            fut_dict = {**fut_dict, **{pool_exec.submit(*args): idx}}

        # fut_dict: dict {(res, service): idx}
        # collect result if available, or send sents back to q_sents
        try:
            for fut in as_completed(fut_dict, timeout=timeout):
                fut.result(0)
        except Exception as exc:
            # print(' **as_completed(fut_dict) exc:** ', exc)
            logger.error(" **as_completed(fut_dict) exc**: %s", exc)

        # unsuccessful terms
        # [[idx, elm.result()] for idx, elm in enumerate(fut_dict) if not elm.result()[0]]

        for fut, idx in fut_dict.items():
            # idx, _ = idx_service
            try:
                # resu += [(fut.result(0), idx_service,)]
                _ = fut.result(0)

                trtext, service, time = _

                # send back to the queue if trtext is None, "",
                if trtext is None or not trtext.strip() :
                    q_sents.append((sents[idx], idx))  # type: ignore
                else:
                    # service in fut.result()[1]
                    resu += [(fut.result(0), idx)]
            except Exception as exc:
                # print('resu += [fut.result(0), idx_service] exc:', exc)
                logger.debug("resu += [fut.result(0), idx_service] exc: %s", exc)

                # q_sents.append((sents[idx], idx))  # type: ignore
                q_sents.append((sents[idx], idx))  # type: ignore

        loop_ += 1
        # if loop_ > len(sents):
        if loop_ > 5:
            logger.warning(
                " Too many attempts, giving up -- probably net problem or none of the services if working"
            )  # noqa
            raise Exception(
                " Too many attempts, giving up -- probably net problem or none of the services if working"
            )

    pool_tr.loop = loop_
    pool_tr.result = resu

    _ = [
        *zip(
            FREEMT_SERVICES,
            [
                *map(
                    lambda x: len([elm for elm in resu if elm is not None and elm[0][1] == x]),
                    FREEMT_SERVICES,
                )
            ],
        )
    ]

    # sorted contribution in reverse order
    pool_tr.dist = sorted(_, key=lambda x: -x[1])

    # rdict
    _ = {
        service: [[elm[0][0], elm[1]] for elm in resu if elm is not None and elm[0][1] == service]
        for service in FREEMT_SERVICES
    }  # noqa
    pool_tr.rdict = _

    resu = [elm for elm in resu if elm is not None]

    # return sorted(resu, key=lambda x: resu[1][0])  # type: ignore
    return sorted(resu, key=lambda x: x[1])  # type: ignore


# if 1:
def main():
    """ main. """
    from pprint import pprint

    log_fmt = "%(filename)10s %(lineno)4d %(levelname)6s %(message)s"
    logging.basicConfig(format=log_fmt, level=10)

    filename2 = (
        r"C:\dl\Dropbox\mat-dir\myapps\playground\bm25-similarity\data\wu_ch2_zh.txt"
    )
    # sents2, _ = load_paras(filename2)
    sents2 = [elm.strip() for elm in read_text(filename2).splitlines() if elm.strip()]

    filename1 = (
        r"C:\dl\Dropbox\mat-dir\myapps\playground\bm25-similarity\data\wu_ch1_zh.txt"
    )
    # sents1, _ = load_paras(filename1)
    sents1 = [elm.strip() for elm in read_text(filename1).splitlines() if elm.strip()]

    filename3 = (
        r"C:\dl\Dropbox\mat-dir\myapps\playground\bm25-similarity\data\wu_ch3_zh.txt"
    )
    # sents3, _ = load_paras(filename3)
    sents3 = [elm.strip() for elm in read_text(filename3).splitlines() if elm.strip()]

    file_lover10 = r"C:\dl\Dropbox\mat-dir\myapps\playground\bm25-similarity\data\lover-ch10_zh.txt"
    # sents10, _ = load_paras(file_lover10)
    sents10 = [
        elm.strip() for elm in read_text(file_lover10).splitlines() if elm.strip()
    ]

    file_pp = r"C:\dl\Dropbox\shuangyu_ku\txt-books\傲慢与偏见-译林body.txt"
    # sentspp, _ = load_paras(file_pp)
    sentspp = [elm.strip() for elm in read_text(file_pp).splitlines() if elm.strip()]

    sents = sentspp[:100]
    sents = sentspp[100:500]
    sents = sentspp[500:1000]
    sents = sentspp[500:550]
    sents = sentspp[1000:1500]

    with report_time(" sents "):
        try:
            # res = pool_tr(sents[:50], timeout=150)
            res = pool_tr(sents, timeout=150)
        except Exception as exc:
            pprint(exc)
            res = ""
    pprint(pool_tr.result[-10:])
    pprint(res[-10:])

    # dist = [*zip(FREEMT_SERVICES, [*map(lambda x: len([elm for elm in res if elm[0][1] == x]), FREEMT_SERVICES)])]
    print(report_time.time_elapsed, len(sents), report_time.time_elapsed / len(res))
    pprint(pool_tr.dist)

    # check None and '' translation
    print([elm for elm in res if elm[0][0] is None or not elm[0][0].strip()])

    # check 'None' translation
    pprint([elm for elm in res if 'None' in elm[0][0]])


if __name__ == "__main__":
    main()
