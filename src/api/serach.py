# -*- coding: utf-8 -*-
# @project S-pixiv
# @file api.py
# @brief
# @author yx
# @data 2024-02-06 13:55:34

from enum import Enum
from typing import Dict, Optional

import requests

import web_parser.headers
import api.utils.pixiv_parse as pixiv_parser
from api.utils.types import (
    UserItem, WorkItem, NovelItem, FollowUsersItems, TrendsItem
)
import tools.logger


class TrendsMode(Enum):
    All  = "all"
    r18  = "r18"
    r18G = "r18G"


class SearchApi(object):
    __version_key = "f17e4808608ed5d09cbde2491b8c9999df4f3962"

    def __init__(self, cookie: str, proxies: Dict = None):
        self.__api = {
            "work": "https://www.pixiv.net/artworks/",  # 单个work,
            "user_info": "https://www.pixiv.net/ajax/user/{uid}/profile/top",  #
            # "user_info": "https://www.pixiv.net/users/{uid}",  # 用户info => html 弃用
            "get_user_all_works": "https://www.pixiv.net/ajax/user/{uid}/profile/all",  # 获取用户所有work
            "get_follow_users": "https://www.pixiv.net/ajax/user/{uid}/following",  # 获取所有关注的用户
            "trends_page": "https://www.pixiv.net/ajax/follow_latest/illust?"  # 动态
        }

        uid = pixiv_parser.match_uid(cookie)
        self.session = requests.session()
        self.session.headers.update({
            "User-Agent": web_parser.headers.user_agent(),
            "Referer": "https://pixiv.net/",
            # "X-User-Id": uid,
        })
        self.session.cookies = web_parser.headers.get_cookies_from_str(cookie)
        self.session.proxies = proxies
        self.__api["get_follow_users"] = self.__api["get_follow_users"].format(uid=uid)

        self.logger = tools.logger.get_logger(__class__.__name__)

    def search_user(self, uid: str) -> Optional[UserItem]:
        api = self.__api["user_info"].format(uid=uid)
        params = {
            "lang": "zh",
            "version": SearchApi.__version_key
        }
        res = self.session.get(api, params=params)
        if not res.ok:
            self.logger.warning(f"search user {uid} failed: {res.status_code}")
            return
        return pixiv_parser.parse_user_doc(res.json())

    def search_work(self, url: str) -> Optional[WorkItem]:
        res = self.session.get(url)
        if not res.ok:
            self.logger.warning(f"search work {url} failed: {res.status_code}")
            return
        return pixiv_parser.parse_work_doc(res.text, pixiv_parser.match_wid(url))

    def search_novel(self, url: str) -> Optional[NovelItem]:
        res = self.session.get(url)
        if not res.ok:
            self.logger.warning(f"search novel {url} failed: {res.status_code}")
            return
        return pixiv_parser.parse_novel_doc(res.text, pixiv_parser.match_nid(url))

    def search_follow_users(self, offset: int = 0, limit: int = 24) -> Optional[FollowUsersItems]:
        """

        :param offset: 偏移量
        :param limit:  张数 use default values
        :return:
        """
        api = self.__api["get_follow_users"]
        params = {
            "offset": offset,
            "limit": limit,
            "tag": "",
            "lang": "zh",
            "rest": "show",
            "acceptingRequests": 0,
            "version": SearchApi.__version_key,
        }
        res = self.session.get(api, params=params)
        if not res.ok:
            self.logger.warning(f"search follow users failed: {res.status_code}")
            return
        return pixiv_parser.parse_follow_users_doc(res.json())

    def search_trends(self, page: int, mode: str = TrendsMode.All) -> Optional[TrendsItem]:
        """

        :param page:
        :param mode: all | r18 | r18G
        :return:
        """
        api = self.__api["trends_page"]
        params = {
            "p": page,
            "mode": mode,
            "lang": "zh",
            "version": SearchApi.__version_key,
        }
        res = self.session.get(api, params=params)
        if not res.ok:
            self.logger.warning(f"search trends failed: {res.status_code}")
            return
        return pixiv_parser.parse_trends_doc(res.json())

    def search_user_works(self, uid: str):
        api = self.__api["get_user_all_works"].format(uid=uid)
        params = {
            "lang": "zh",
            "version": SearchApi.__version_key
        }
        res = self.session.get(api, params=params)
        if not res.ok:
            self.logger.warning(f"search user all works {uid} failed: {res.status_code}")
            return
        return pixiv_parser.parse_user_works_doc(res.json())
