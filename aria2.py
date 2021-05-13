
import os
import time
from pyaria2 import Aria2RPC

# from pyaria2 import Jsonrpc
# jsonrpc = Jsonrpc('localhost', 6800)
# resp = jsonrpc.addUris('https://music.snowmusic.cc/radio/13714_1507261169_4.mp3', options={"out": "aa.mp3"})
jsonrpc = Aria2RPC()
def get_file_from_url(link, file_name):
    print(link)
    set_dir = os.path.dirname(__file__)
    options = {"dir": set_dir, "out": file_name, }
    res = jsonrpc.addUri([link], options=options)


def get_file_from_cmd(link):
    exe_path = r'D:\aria2-1.35.0-win-64bit-build1\aria2c.exe'
    order = exe_path + ' -s16 -x10 ' + link
    os.system(order)

def active_task_num():
    active=jsonrpc.tellActive()
    return len(active)

def get_waitting_paths():
    waiting=jsonrpc.tellWaiting(0,10)
    waitting_paths=[]
    for i in waiting:
        waitting_paths.append(i["files"][0]["path"])
    return waitting_paths

def remove_error_task():
    stopped=jsonrpc.tellStopped(0,100)
    for i in stopped:
        if i["status"]=="error":
            jsonrpc.removeDownloadResult(i["gid"])
def get_global_speed():
    status=jsonrpc.getGlobalStat()
    speed=int(status['downloadSpeed'])/1024/1024
    return speed
if __name__ == '__main__':
    get_global_speed()
    # link = 'http://180.97.210.157/videos/v0/20200713/b0/ec/4bfd28f79b639e575c476e7345a595ed.f4v?key=0085fd54fc59e2be7a03308d36974c34b&dis_k=2959416db98d353ba9c48c33be647ee14&dis_t=1620789649&dis_dz=OTHER-None&dis_st=103&src=iqiyi.com&dis_hit=0&dis_tag=00000000&uuid=2f633ae0-609b4991-116&qd_ip=2f633ae0&qd_k=d7ac4311b5451de0e81bcf9781581287&qd_aid=228872801&qd_stert=0&qd_uid=0&qd_p=2f633ae0&qd_src=01012001010000000000&qd_index=1&qd_vip=0&qd_tvid=2336969100&qd_vipdyn=0&qd_vipres=0&qd_tm=1620789649440'
    # filename = '2021.f4v'
    # start = time.time()
    # get_file_from_url(link,filename)
    # end = time.time()
    # print(f"耗时:{end - start:.2f}")
    # active_task_num()
    # print(get_waitting_paths())
    # get_stopped()
    pass