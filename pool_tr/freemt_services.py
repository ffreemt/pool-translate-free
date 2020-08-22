"""
free mt_services

"""
from typing import Dict

FREEMT_SERVICES = dict(
    sogou_tr="sogou_tr",
    bing_tr="bing_tr",
    google_tr="google_tr",  # github version based on gltr
    xiaoniu_tr="xiaoniu_tr",
    # googlecn='googlecntr',
    # gapis='googleapis_translate',
    # ** tier 2 **
    promt_tr="promt_tr",
    bdtr="bdtr",  # api free
    qq_tr="qq_tr",
    youdao_tr="youdao_tr",
    # ** tier 3 **
    omni_tr="omni_tr",
    iciba_tr="iciba_tr",
    # systran_tr='systran_tr',
)  # type: Dict[str, str]

freemt_services = (
    FREEMT_SERVICES
)  # type: Dict[str, str]  # pylint: disable=invalid-name
