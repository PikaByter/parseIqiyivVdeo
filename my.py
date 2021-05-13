import requests
from bs4 import BeautifulSoup
from aria2 import *
from config import *
# OVER:配置aria2
# OVER:使用go多线程调用aria2下载文件，并合并
# todo:写好aria2初探文档和go调用exec.command文档
# Wait for Test:每五秒检查失败的任务，并将其移除
# todo:下载失败后保存相关信息，并在全部结束后重试，仍失败则将其输出到文件中
# OVER:在aria2下载视频的同时申请解析
# OVER:选择下载清晰度
# OVER:提交任务前先检索任务是否提交过

def save_links(links):
    with open("%s\\links.txt"%video_name, "w", encoding="utf-8") as f:
        for link in links:
            f.write(link + "\n")

def get_links():
    print("解析详情页获取每集链接")
    r = requests.get(video_info_url)
    soup = BeautifulSoup(r.text, 'lxml')
    link_elements = soup.find_all(attrs={'class': 'site-piclist_pic_link'})
    link_elements = link_elements[:-1]
    links = []
    for link_element in link_elements:
        links.append(link_element["href"].strip("//"))
    print("保存每集链接")
    save_links(links)
    return links

def load_links():
    print("从文件中加载每集链接")
    with open("%s\\links.txt"%video_name, "r", encoding="utf-8") as f:
        links = f.readlines()
        links = [i.strip("\n") for i in links]
    return links


def check_task_done_or_exist(path):
    if os.path.exists(path):
        return True

    waitting_paths=get_waitting_paths()
    if path.replace("\\","/") in waitting_paths:
        return True
    return False



def parse(links):

    if os.path.exists("current_episode.txt"):
        with open("current_episode.txt","r") as f:
            episode_num=int(f.readline().strip())
    else:
        episode_num=1

    for link in links[episode_num-1:]:
        print("申请解析第%d集的数据"%episode_num)
        data = {
            "url": "https://" + link
        }
        headers = {
            "cookie": 'uuid=8c430ecb-2a66-4512-c5bf-d7e753b26d6f; slim_session={"slim.flash":[]}; _access=af3f6dc2d1ac3dcc930b46dd16d01b65a69679888ded721b3fdab3693da4d0ae',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            "origin": "https://tool.lu",
            "referer": "https://tool.lu/videoparser/"
        }
        parse_url = "https://tool.lu/videoparser/ajax.html"
        r = requests.post(url=parse_url, headers=headers, data=data)
        print("解析完成，获取链接！")

        data = eval(str(r.text))
        streams=data["items"][0]["streams"]
        HD_urls_info= get_HD_urls_info(streams)

        dir_name = "%s\\%s第%d集" % (video_name, video_name, episode_num)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        episode_num+=1
        slice_num=0
        for HD_url_info in HD_urls_info:
            save_path=os.path.join(dir_name,"%d.mp4"%slice_num)
            url=HD_url_info["url"].replace("\\","").replace("\\","")
            if not check_task_done_or_exist(os.path.join(os.getcwd(),save_path)):
                get_file_from_url(url,save_path)
            slice_num+=1
        while True:
            time.sleep(1)
            remove_error_task()
            if active_task_num()<3:
                print("\n本集剩余任务不足3个，开始下一集的解析")
                break
            files=os.listdir(dir_name)
            downloading_num=0
            for file in files:
                if ".aria" in file:
                    downloading_num+=1

            info = "共有%d个分片,正在下载文件数：%d,已完成文件数：%d,当前下载速度：%.3fM/s"%(slice_num,downloading_num,len(files)-2*downloading_num,get_global_speed())
            info_added_color='\033[5;33;40m%s\033[0m'%info
            print("\r",info_added_color, end='', flush=True)

        print("————————————————")
        print()
        with open("current_episode.txt","w") as f:
            f.write(str(episode_num))


def get_HD_urls_info(streams):
    quality_dic = {}
    quality_list = []
    for stream in streams:
        size = float(stream["size"].replace(" MB", ""))
        quality_dic[size] = stream["urls"]
        quality_list.append(size)
    quality_list.sort(reverse=True)
    HD_urls_info = quality_dic[quality_list[quality_num]]
    return HD_urls_info


if __name__ == '__main__':
    if not os.path.exists(video_name):
        os.mkdir(video_name)
    if not os.path.exists("%s\\links.txt"%video_name):
        links=get_links()
    else:
        links = load_links()
    parse(links)
