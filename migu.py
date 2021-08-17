#!/usr/bin/python3
# coding=utf-8

"""
咪咕音乐下载
爬取关键点：
1、搜索歌曲的url：
    https://m.music.migu.cn/migu/remoting/scr_search_tag?rows=20&type=2&keyword=%25E6%25B1%25AA%25E8%258B%258F%25E6%25B3%25B7&pgc=1
    'http://m.music.migu.cn/migu/remoting/scr_search_tag'

2、搜索歌曲url请求参数：
    keyword：歌曲名
    rows：搜索数量
    params = {'rows': pagesize, 'type': 2, 'keyword': key, 'pgc': 1, }

https://m.music.migu.cn/migu/remoting/scr_search_tag?rows=20&type=2&keyword=%25E9%2583%25AD%25E9%2587%2587%25E6%25B4%2581&pgc=1

"""
import os
from requests import get
from progressBar import progressbar as pb

test = "https://m.music.migu.cn/migu/remoting/scr_search_tag?rows=20&type=2&keyword=%25E8%25AE%25B8%25E5%25B5%25A9&pgc=1"

class MiGu:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ",
            "Host": "m.music.migu.cn",
            "Referer": "https://m.music.migu.cn/v3/search"
        }
        self.url_search = 'https://m.music.migu.cn/migu/remoting/scr_search_tag'
        self.params_search = {'rows': "", 'type': 2, 'keyword': "", 'pgc': 1, }
        self.song_list = []
        self.url_download = "https://app.pd.nf.migu.cn/MIGUM3.0/v1.0/content/sub/listenSong.do"  # 服务器链接
        self.url_getContent = 'https://m.music.migu.cn/migu/remoting/cms_detail_tag?cpid='
        # 接contentId就可以查询出productId从而构造播放路径

        self.params_download = {
            "toneFlag": "HQ",
            "netType": "00",
            "userId": 15548614588710179085069,
            "ua": "Android_migu&version5.1",
            "copyrightId": '600547019381',
            "contentId": 600902000006889305,
            "resourceType": "E",
            "channel": 0
        }

    def search(self, key, pagesize=30):
        """
        :param key: keyword
        :param pagesize:
        :return: None
        """
        self.params_search["keyword"] = key
        self.params_search["rows"] = pagesize

        #res = get(test, headers = self.headers);
        try:
            res = get(self.url_search, headers=self.headers, params=self.params_search)
        except Exception:
            print("搜索错误!")
            exit()

        if res.status_code == 200:
            self.parse(res.json()["musics"])
        else:
            printf("响应码错误!")


    def parse(self, resData):
        """
        :param resData: 搜索后返回的数据
        :return:
        """
        for i in resData:
            buf = {"name": i["songName"], "singer": i["singerName"], "url_play": i["mp3"], "url_lrc": i["lyrics"],
                   "url_pic": i["cover"], "copyrightId": i['copyrightId']}
            # TODO lrc暂时出现问题
            self.song_list.append(buf)

    def getPlayUrl(self, copyrightId):
        res = get(url=self.url_getContent + copyrightId, headers = self.headers).json()
        try:
            contentId = res['data']['qq']['productId']
        except TypeError:
            return None
        self.params_download['contentId'] = contentId
        url =  """https://app.pd.nf.migu.cn/MIGUM3.0/v1.0/content/sub/listenSong.do?toneFlag={}&netType=00&userId={}&ua=Android_migu&version5.1&copyrightId={}&contentId={}&resourceType=E&channel=0""".format('HQ', self.params_download["userId"], 0, contentId)
        return url

# "toneFlag": "HQ",
#             "netType": "00",
#             "userId": 15548614588710179085069,
#             "ua": "Android_migu&version5.1",
#             "copyrightId": '600547019381',
#             "contentId": 600902000006889305,
#             "resourceType": "E",
#             "channel": 0


if __name__ == "__main__":
    ret = MiGu()
    kwd = input("搜索关键字:")
    ret.search(kwd)
    info = ret.song_list
    # print(info)# input("输入copyrightId:")


    for i in range(len(info)):
        print("[{}]歌名:{}---歌手:{}".format(i, info[i]["name"], info[i]["singer"]))

    while(True):
        num = input("输入要下载的编号:(下载所有输入all, 退出q)")
        if num == "all":
            for i in info:
                url = ret.getPlayUrl(i["copyrightId"])
                if url == None:
                    print("解析失败...")
                    continue
                path = "./music/{}---{}.mp3".format(i["name"], i["singer"])
                if not os.path.exists(path):
                    try:
                        pb(url = url, path = path)
                    except KeyError:
                        print("下载失败",i["name"])
                        continue
                else:
                    print("{}，已存在".format(path))
            break
        elif num == "q":
            break
        else:
            url = ret.getPlayUrl(info[int(num)]["copyrightId"])
            # print(url)
            path = "./music/{}---{}.mp3".format(info[int(num)]["name"], info[int(num)]["singer"])
            if not os.path.exists(path):
                # print(url)
                try:
                    pb(url = url, path = path)
                except KeyError:
                    print("该歌曲未有版权!")
            else:
                print("{}，已存在".format(path))
        # del ret  # 删除之后info还在
        # print(info)


