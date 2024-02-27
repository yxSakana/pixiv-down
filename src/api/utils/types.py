# -*- coding: utf-8 -*-
# @project S-pixiv
# @file types.py
# @brief
# @author yx
# @data 2024-02-06 15:09:34

from typing import List
import dataclasses


@dataclasses.dataclass
class UserItem:
    uid:            str
    user_name:      str
    home_url:       str = ""
    image_url:      str = ""
    background_url: str = ""
    description:    str = ""


@dataclasses.dataclass
class WorkItem:
    user_info:   UserItem
    wid:         str
    title:       str
    tags:        List[str]
    description: str = ""
    image_urls:  List[str] = dataclasses.field(default_factory=list)


WorkItems = List[WorkItem]


@dataclasses.dataclass
class NovelItem:
    user_info:   UserItem
    nid:         str
    title:       str
    tags:        List[str]
    description: str = ""
    content:     str = ""  # 小说内容
    user_novels: List[str] = dataclasses.field(default_factory=list)  # 该用户其他小说的id


NovelItems = List[NovelItem]


@dataclasses.dataclass
class FollowUsersItem:
    user_info: UserItem
    novels:    NovelItems
    novel_ids: List[str]
    works:     WorkItems
    work_ids:  List[str]


FollowUsersItems = List[FollowUsersItem]


@dataclasses.dataclass
class TrendsItem:
    ids:    List[str]
    works:  WorkItems


@dataclasses.dataclass
class UserWorksItem:
    work_ids:  List[str]
    novel_ids: List[str]
    manga_ids: List[str]
