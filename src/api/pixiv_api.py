# -*- coding: utf-8 -*-
# @project S-pixiv
# @file pixiv_api.py
# @brief
# @author yx
# @data 2024-02-07 20:44:32

from typing import Dict

from api.serach import SearchApi
from api.download import DownloadApi


class PixivApi(object):
    def __init__(self, cookie: str, proxies: Dict):
        self.search = SearchApi(cookie, proxies)
        self.download = DownloadApi(cookie, proxies)
