# -*- coding: utf-8 -*-
# @project S-pixiv
# @file test_download.py
# @brief
# @author yx
# @data 2024-02-06 22:35:49

import dataclasses
import os
from typing import Dict

from api.serach import SearchApi
import api.utils.pixiv_parse as pixiv_parser
import tools.files
import tools.logger


class DownloadApi(object):
    def __init__(self, cookie: str, proxies: Dict = None):
        self.search_api = SearchApi(cookie, proxies)
        self.base_path = "data"
        self.logger = tools.logger.get_logger(__class__.__name__)

    def set_download_dir(self, dir_name: str) -> None:
        self.base_path = dir_name

    def work(self, url: str) -> None:
        self.logger.debug(f"work {url} downloading...")
        item = self.search_api.search_work(url)
        if item is None:
            return
        dir_name = os.sep.join([self.base_path, item.user_info.user_name, "image", item.title])
        tools.files.download_multiple_media_(
            f"{dir_name}",
            item.image_urls,
            headers=self.search_api.session.headers,
            proxies=self.search_api.session.proxies
        )
        tools.files.save(f"{dir_name}/data.txt", dataclasses.asdict(item), ensure_json=True)
        self.logger.debug(f"work {url} finish")

    def novel(self, url: str) -> None:
        self.logger.debug(f"novel {url} downloading...")
        item = self.search_api.search_novel(url)
        if item is None:
            return
        dir_name = os.sep.join([self.base_path, item.user_info.user_name, "novel", item.title])
        tools.files.save(f"{dir_name}/{item.title}.txt",
                         f"""
                         title: {item.title}\n
                         tags: {item.tags}\n
                         words: {tools.files.format_words(len(item.content))}\n
                         {item.content}
                         """)
        tools.files.save(f"{dir_name}/data.txt",
                         {k: v for k, v in dataclasses.asdict(item).items() if k != "content"},
                         ensure_json=True)
        self.logger.debug(f"novel {url} finish")

    def user_works(self, uid: str) -> None:
        item = self.search_api.search_user_works(uid)
        if item is None:
            return
        for i in item.work_ids:
            self.work(pixiv_parser.join_wid(i))
        for i in item.novel_ids:
            self.novel(pixiv_parser.join_nid(i))

