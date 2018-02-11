# -*- coding: utf-8 -*-
import requests
import time

headers = {
    'User-Agent': 'Mozilla/5.0'
}


def get_videos_nums(mid):
    space_url = "https://api.bilibili.com/x/space/navnum?mid={}".format(mid)
    resp = requests.get(space_url, headers=headers)
    resp.raise_for_status()
    resp.encoding = 'utf-8'
    try:
        resp_json = resp.json()
    except ValueError:
        print("json 解析失败：{}".format(resp.text))
    else:
        return resp_json['data']['video']
    return None


def get_video_aid_title(mid):
    videos_url = "https://space.bilibili.com/ajax/member/" \
                 "getSubmitVideos?mid={}&pagesize=1&page=1&order=pubdate".format(mid)

    resp = requests.get(videos_url, headers=headers)
    resp.raise_for_status()
    resp.encoding = 'utf-8'
    try:
        resp_json = resp.json()
    except ValueError:
        print("json 解析失败：{}".format(resp.text))
    else:
        aid = resp_json['data']['vlist'][0]['aid']
        title = resp_json['data']['vlist'][0]['title']
        return aid, title
    return None


def post_comment(aid, message):
    reply_url = "https://api.bilibili.com/x/v2/reply/add"
    cookie = {
        "DedeUserID": "",  # 用户ID
        "DedeUserID__ckMd5": "",  # 用户ID_MD5值
        "SESSDATA": "",  # 会话cookie
        "bili_jct": ""  # crsf cookie
    }
    request_headers = {
        "Cookie": "DedeUserID={DedeUserID}; "
                  "DedeUserID__ckMd5={DedeUserID__ckMd5}; "
                  "SESSDATA={SESSDATA}; "
                  "bili_jct={bili_jct}; ".format(DedeUserID=cookie["DedeUserID"],
                                                 DedeUserID__ckMd5=cookie["DedeUserID__ckMd5"],
                                                 SESSDATA=cookie["SESSDATA"],
                                                 bili_jct=cookie['bili_jct']),
        "User-Agent": "Mozilla/5.0",
    }
    form_data = {
        "oid": aid,
        "type": 1,
        "message": message,
        "plat": 1,
        "jsonp": "jsonp",
        "csrf": cookie["bili_jct"]
    }
    try:
        resp = requests.post(reply_url, headers=request_headers, data=form_data)
        resp.raise_for_status()
        resp_json = resp.json()
    except requests.HTTPError:
        print("网络错误")
    except ValueError:
        print("json 解析失败")
    else:
        if resp_json.get('code', None) is not None:
            if resp_json['code'] == 0:
                print("评论成功：{}".format(message))
                return True
            else:
                print("评论失败：{}".format(message))
        else:
            print("json 格式错误")
    return False


if __name__ == '__main__':
    mid = 221648  # UP主ID号
    message = "第一"  # 留言内容
    try:
        current_videos_num = get_videos_nums(mid)
        target_num = current_videos_num + 1
        while target_num != get_videos_nums(mid):
            time.sleep(1)
        aid, title = get_video_aid_title(mid)
        if post_comment(aid, message):
            print("视频{}评论成功".format(title))
        else:
            print("视频{}评论失败".format(title))
    except requests.HTTPError:
        print("网络错误")
