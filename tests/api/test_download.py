# -*- coding: utf-8 -*-
# @project S-pixiv
# @file test_download.py
# @brief
# @author yx
# @data 2024-02-06 23:05:08

from api.download import DownloadApi
import tools.files


def test_work():
    api.work("https://www.pixiv.net/artworks/114517436")


def test_novel():
    api.novel("https://www.pixiv.net/novel/show.php?id=21262289")


def test_user_works():
    # api.user_works("13379747")
    api.user_works("24008955")


if __name__ == '__main__':
    cookie = tools.files.read("config/cookie")
    proxies = {
        "http": "127.0.0.1:7890",
        "https": "127.0.0.1:7890"
    }
    api = DownloadApi(cookie, proxies)

    # test_work()
    # test_novel()
    test_user_works()
