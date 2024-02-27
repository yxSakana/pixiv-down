# -*- coding: utf-8 -*-
# @project S-pixiv
# @file pixiv_parse.py
# @brief
# @author yx
# @data 2024-02-06 15:02:14

import re
import json
import urllib.parse
from typing import Dict

from lxml import etree

from .types import (
    UserItem, WorkItem, NovelItem,
    FollowUsersItem, TrendsItem,
    UserWorksItem
)


JsonData = Dict


def match_uid(cookie: str) -> str:
    return re.search("PHPSESSID=(\\d+?)_", cookie).group(1)


def match_wid(url: str) -> str:
    base_url = "https://www.pixiv.net/artworks/"
    url = urllib.parse.urljoin(base_url, url)
    return url.split("/")[-1]


def join_wid(wid: str) -> str:
    return f"https://www.pixiv.net/artworks/{wid}"


def match_nid(url: str) -> str:
    return re.search("\\?id=(\\d+)", url).group(1)


def join_nid(nid: str) -> str:
    return f"https://www.pixiv.net/novel/show.php?id={nid}"


def parse_work_doc(text: str, wid: str) -> WorkItem:
    docs = etree.HTML(text)
    preload_data = json.loads(docs.xpath('//*[@id="meta-preload-data"]/@content')[0])
    body = preload_data["illust"][wid]
    start_url = body["urls"]["original"]
    page_count = int(body["pageCount"])
    return WorkItem(
        UserItem(
            uid= list(preload_data["user"].keys())[0],
            user_name = body["userName"],
        ),
        wid         = wid,
        title       = body["title"],
        tags        = [tag["tag"] for tag in body["tags"]["tags"]],
        description = body["description"] or body["illustComment"],
        image_urls  = [re.sub("_p\\d+", f"_p{str(i)}", start_url, count=1)
                       for i in range(page_count)]
    )


def parse_user_doc(data: JsonData) -> UserItem:
    meta = data["body"]["extraData"]["meta"]
    return UserItem(
        uid            = meta["canonical"].split("/")[-1],
        user_name      = meta["ogp"]["title"],
        home_url       = meta["canonical"],
        image_url      = "",
        background_url = meta["twitter"]["image"],
        description    = meta["ogp"]["description"]
    )


def parse_novel_doc(text: str, nid: str) -> NovelItem:
    docs = etree.HTML(text)
    content = docs.xpath('//*[@id="meta-preload-data"]/@content')[0]
    data = json.loads(content)

    novel_id, novel_data = tuple(data["novel"].items())[0]
    user_id, user_data = tuple(data["user"].items())[0]
    return NovelItem(
        UserItem(
            uid       = user_id,
            user_name = user_data["name"],
            image_url = user_data["imageBig"]
        ),
        nid         = nid,
        title       = novel_data["title"],
        tags        = [item["tag"] for item in novel_data["tags"]["tags"]],
        description = novel_data["extraData"]["meta"]["description"],
        content     = novel_data["content"],
        user_novels = list(novel_data["userNovels"].keys())
    )


def parse_follow_users_doc(data: JsonData):
    users = data["body"]["users"]
    return [FollowUsersItem(
        user_info = UserItem(
            uid         = item["userId"],
            user_name   = item["userName"],
            image_url   = item["profileImageUrl"],
            description = item["userComment"]
        ),
        novels = [
            NovelItem(
                user_info = UserItem(
                    uid         = item["userId"],
                    user_name   = item["userName"],
                    image_url   = item["profileImageUrl"],
                    description = item["userComment"]
                ),
                nid         = novel["id"],
                title       = novel["title"],
                tags        = novel["tags"],
                description = novel["description"],
                content     = "",
                user_novels = [],
            )
            for novel in item.get("novels", [])
        ],
        novel_ids = [novel["id"] for novel in item.get("novels", [])],
        works = [
            WorkItem(
                user_info = UserItem(
                    uid         = item["userId"],
                    user_name   = item["userName"],
                    image_url   = item["profileImageUrl"],
                    description = item["userComment"]
                ),
                wid         = work["id"],
                title       = work["title"],
                tags        = work["tags"],
                description = work["description"],
                image_urls  = []
            )
            for work in item.get("illusts", [])
        ],
        work_ids = [work["id"] for work in item.get("illusts", [])],
    )
        for item in users
    ]


def parse_trends_doc(data: JsonData):
    main_data = data["body"]
    return TrendsItem(
        ids = main_data["page"]["ids"],
        works = [WorkItem(
            user_info = UserItem(
                uid = item["userId"],
                user_name = item["userName"],
            ),
            wid   = item["id"],
            title = item["title"],
            tags  = item["tags"],

        ) for item in main_data["thumbnails"]["illust"]]
    )


def parse_user_works_doc(data: JsonData) -> UserWorksItem:
    import tools.files
    tools.files.save("tmp/user_works_novel.json", data, ensure_json=True)
    works  = data["body"]["illusts"]
    novels = data["body"]["novels"]
    mangas = data["body"]["manga"]
    return UserWorksItem(
        work_ids  = list(works.keys()) if isinstance(works, dict) else [],
        novel_ids = list(novels.keys()) if isinstance(novels, dict) else [],
        manga_ids = list(mangas.keys()) if isinstance(mangas, dict) else [],
    )
