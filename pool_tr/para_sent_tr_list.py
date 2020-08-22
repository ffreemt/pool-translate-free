"""

paras ->
        sents

        pool_tr
     <-
        senti - sentj
list_par_sent
[[str...]...]

lst = [[1, 2], [1]]; import itertools
[*itertools.chain.from_iterable(lst)]
# [1, 2, 1]

from itertools import chain
[*chain.from_iterable(lst)]
# [1, 2, 1]


"""

from pathlib import Path

from itertools import chain  # slightly faster?

# from functool9s import reduce  #
# also [elm for slst in lst for elm in slst]

from typing import Tuple, List, Any

from polyglot.text import Text  # type: ignore

# from seg_zhsent import seg_zhsent
# from seg_xysent import seg_xysent

# from load_paras import load_paras
# from pool_tr import pool_tr
from pool_tr.read_text import read_text


def paras_to_sents(paras: List[str],) -> Tuple[List[Any], List[Any], str]:
    """ sent-segment paras sents list, slice_list and lang
    """
    sents: List[str] = []
    slice_list: List[slice] = []
    lang: str = Text(" ".join(paras[:30])).detect_language()

    para_sents: List[List[str]] = [[]]

    para_sents = [
        Text(para, hint_language_code="zh").raw_sentences for para in paras
    ]  # noqa

    len_list = [*map(len, para_sents)]
    pos_list = [sum(len_list[:idx]) for idx, val in enumerate(len_list)]
    slice_list = [
        slice(val, val + len_list[idx]) for idx, val in enumerate(pos_list)
    ]  # noqa

    sents = [*chain.from_iterable(para_sents)]

    return sents, slice_list, lang


def test_sents2():
    """ test wuth ch2 """
    filename = r"C:\dl\Dropbox\mat-dir\myapps\playground\bm25-similarity\data\wu_ch2_zh.txt"  # noqa

    if not Path(filename).exists():
        raise SystemExit(f"[{filename}] does not exist, exiting...")

    # paras, _ = load_paras(filename)
    paras = [elm.strip() for elm in read_text(filename).splitlines() if elm.strip()]
    sents, slice_list, lang = paras_to_sents(paras)

    assert paras[0] == "".join(sents[slice_list[0]])
    assert paras[6] == "".join(sents[slice_list[6]])
    assert paras[-6] == "".join(sents[slice_list[-6]])
    assert paras[-1] == "".join(sents[slice_list[-1]])
    assert lang == "zh"


def main():
    """main"""

    # paras = sentspp[:100]
    # paras = sentspp[100:500]
    # paras = sentspp[:]

    # paras, _ = load_paras(filename)

    # para_sents = [*map(seg_zhsent, paras)]
    # sents = [*chain.from_iterable(para_sents)]

    # sents = reduce(lambda x, y: x + y, para_sents)

    # reconstruct para_sents from sents and slice_list
    # para_sents1 = [*map(lambda x: sents[x], slice_list)]
    # assert para_sents == para_sents1

    # sents_tr = pool_tr(sents)
