r"""
omnifanyi fiddler4

allheaders = POST /transsents.do HTTP/1.1
Host: www.omifanyi.com
Connection: keep-alive
Content-Length: 59
Pragma: no-cache
Cache-Control: no-cache
Accept: application/json, text/javascript, */*; q=0.01
Origin: https://www.omifanyi.com
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Referer: https://www.omifanyi.com/?tdsourcetag=s_pctim_aiomsg
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Cookie: JSESSIONID=AE1DD5B34D2D51F96906BB2CCCCE37DE

"""

from typing import Optional

import logging

import requests
import langid

from jmespath import search

langid.set_languages(["en", "zh"])

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

# from user_agent import UA
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17"  # NOQA
# from allheaders_to_headers import textview_to_data

URL0 = "https://www.omifanyi.com"
URL = "https://www.omifanyi.com/transsents.do"

# textview = 'sentsToTrans=these+are+tests&languageType=undef&userDbName='

# data = textview_to_data(textview)

# query = 'i love you. I love you more'


def omni_tr(text: str, to_lang: str = "zh") -> Optional[str]:
    """
        e2c, c2e only
    """

    text = text.strip()

    if not text:
        return ""

    if to_lang.lower() in ["en", "english"]:
        to_lang = "en"
    if to_lang.lower() in ["zh", "chinese"]:
        to_lang = "zh"

    if to_lang not in ["en", "zh"]:
        LOGGER.warning(" to_lang %s not ['en', 'zh']", to_lang)
        raise Exception("Invalid")

    langid_, _ = langid.classify(text[:3000])

    if langid_ == to_lang:
        return text

    if to_lang.lower() in ["en"]:
        language_type = "c2e"
    else:
        language_type = "e2c"

    # data['sentsToTrans'] = query
    data = {"languageType": language_type, "sentsToTrans": text, "userDbName": ""}

    # res = requests.post(URL, data=data, )
    headers0 = {"User-Agent": UA, "origin": URL0}
    res = requests.post(URL, data=data, headers=headers0)

    # res1 = requests.get(f'{url}?{textview}')  # OK

    jdata = res.json()
    omni_tr.json = jdata

    try:
        s_res = search("sentsResults[1]", jdata)[0]
    except Exception as exc:
        LOGGER.warning("search('sentsResults[1]', jdata)[0] exc :%s", exc)
        s_res = None

    if s_res is None:
        LOGGER.warning(" **No output**, probably because daily free quota exceeded")
        trtext = "None"
    # else: trtext = s_res

    # return trtext
    return s_res


def main():
    """ main. """
    from random import randint

    print(omni_tr("test " + str(randint(1, 1000))))


if __name__ == "__main__":
    main()
