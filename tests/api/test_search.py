# -*- coding: utf-8 -*-
# @project S-pixiv
# @file api.py
# @brief
# @author yx
# @data 2024-02-06 14:11:46

import dataclasses
from pprint import pprint

from api.serach import SearchApi
import tools.files


def test_search_work():
    res = api.search_work("https://www.pixiv.net/artworks/114517436")
    pprint(res)


def test_search_user():
    res = api.search_user("1113943")
    pprint(res)


def test_search_novel():
    res = api.search_novel("https://www.pixiv.net/novel/show.php?id=21262289")
    pprint(res)


def test_search_follow_users():
    res = api.search_follow_users()
    # da = [dataclasses.asdict(r) for r in res]
    # tools.files.save("tmp/follow_users_da.json", da, ensure_json=True)
    pprint(res)


def test_search_trends():
    res = api.search_trends(1, "r18G")
    # tools.files.save("tmp/trends_da.json", dataclasses.asdict(res), ensure_json=True)
    pprint(res)


def test_search_user_works():
    res = api.search_user_works("24008955")
    res = api.search_user_works("13379747")
    pprint(res)


if __name__ == '__main__':
    cookie = tools.files.read("config/cookie")
    proxies = {
        "http": "127.0.0.1:7890",
        "https": "127.0.0.1:7890"
    }
    api = SearchApi(cookie, proxies)

    # test_search_work()
    # test_search_user()
    # test_search_novel()
    # test_search_follow_users()
    # test_search_trends()
    test_search_user_works()
