import requests, os, asyncio, aiohttp

"""
miguMusic类可直接调用
"""


class miguMusic:
    def __init__(self, keyword):
        self.header = {
            "sign": "3c30c9a4629c9d01b15e21806cb6aa17",
            "appId": "yyapp2",
            "timestamp": "1585017019971",
            "Connection": "Keep-Alive"
        }
        self.params_search = {
            "feature": "1111000000",
            "pageNo": 1,
            "pageSize": 20,
            "sort": 0,
            "text": "告白气球",
            "sid": "ccb88a5ea4df4a9d9463354936ef3bd59856bccecf184c09bc85b093fad321c4",
            "isCopyright": 1,
            "isCorrect": 1,
            "searchSwitch": "{'song': 1, 'album': 0, 'singer': 0, 'tagSong': 1, 'mvSong': 0, 'bestShow': 1,'songlist': 0, 'lyricSong': 0}"
        }
        self.params_download = {
            "toneFlag": "SQ",
            "netType": "00",
            "userId": 15548614588710179085069,
            "ua": "Android_migu&version5.1",
            "copyrightId": 0,
            "contentId": 600906000000260455,
            "resourceType": "E",
            "channel": 0
        }
        self.searchUrl = "http://jadeite.migu.cn:7090/music_search/v2/search/searchAll"
        self.downloadUrl = "http://app.pd.nf.migu.cn/MIGUM2.0/v1.0/content/sub/listenSong.do"  # 服务器链接
        self.params_search["text"] = keyword
        if not os.path.exists("./Music"):  # 在当前目录下生成一个Music的文件夹 用于存储下载的歌曲
            os.mkdir("./Music")

    def search_show(self):

        response = requests.get(url=self.searchUrl, params=self.params_search, headers=self.header)
        self.songlist = response.json()["songResultData"]["resultList"]  # 进行筛选,数据清洗

        # Show
        for num in range(len(self.songlist)):
            name = self.songlist[num][0]["name"]
            singer = self.songlist[num][0]["singers"][0]["name"]
            print("[%d]" % num, "name:", name, "---singer:", singer)

    async def download(self, num):
        self.params_download["contentId"] = str(self.songlist[num][0]["relatedSongs"][2]["productId"])
        name = self.songlist[num][0]["name"]
        print("开始下载：", name, "请稍等！！")
        singer = self.songlist[num][0]["singers"][0]["name"]
        path = "./Music/" + name + "---" + singer + ".flac"
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.downloadUrl, params=self.params_download)as resp:
                # print(resp.url)
                with open(path, 'wb')as fp:
                    while True:
                        chunk = await resp.content.read()
                        if not chunk:
                            break
                        fp.write(chunk)
        print(name, "---", singer, ' DownloadSuccess！！')

    def run(self):
        try:
            self.search_show()
            tasks = []  # 存放将要异步的线程
            nums = []  # 存放要下载的编号
            while True:
                num = int(input("请问要下载的是哪一首歌曲呢?------(退出即开始下载请输入88)"))
                if num == 88:
                    break
                nums.append(num)
                print(self.songlist[num][0]["name"], " 已加入下载列表！！")

            if len(nums) != 0:
                for n in nums:
                    c = self.download(n)
                    task = asyncio.ensure_future(c)
                    tasks.append(task)
                loop = asyncio.get_event_loop()
                loop.run_until_complete(asyncio.wait(tasks))
                loop.close()
            else:
                print("无下载列表！")
        except Exception as fp:
            print(fp)
            print('异常请联系管理员！')
      


if __name__ == "__main__":
    kwd = input("KeyWord:")
    down = miguMusic(kwd)
    down.run()
