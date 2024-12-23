import eventlet
eventlet.monkey_patch()  # 必须在导入其他模块之前运行

import time
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import re
import os
import threading
from queue import Queue

# 初始化 `results` 变量
results = []

urls = [
"http://1.196.55.1:9901",
"http://1.197.249.1:9901",
"http://101.65.32.1:9901",
"http://101.66.198.1:9901",
"http://101.66.199.1:9901",
"http://101.72.127.1:808",
"http://106.46.147.1:10443",
"http://106.55.164.1:9901",
"http://111.225.112.1:808",
"http://111.225.114.1:808",
"http://111.33.89.1:9901",
"http://111.78.22.1:9901",
"http://111.8.224.1:8085",
"http://112.132.160.1:9901",
"http://112.234.23.1:9901",
"http://112.26.18.1:9901",
"http://112.5.89.1:9900",
"http://112.5.89.1:9901",
"http://113.116.145.1:8883",
"http://113.116.59.1:8883",
"http://113.124.234.1:9901",
"http://113.195.13.1:9901",
"http://113.195.162.1:9901",
"http://113.195.4.1:9901",
"http://113.195.45.1:9901",
"http://113.200.214.1:9902",
"http://113.201.61.1:9901",
"http://113.205.195.1:9901",
"http://113.205.196.1:9901",
"http://113.206.102.1:9901",
"http://113.218.204.1:8081",
"http://113.220.234.1:9999",
"http://113.220.235.1:9999",
"http://113.57.20.1:9901",
"http://113.57.93.1:9900",
"http://113.92.198.1:8883",
"http://114.254.92.1:88",
"http://115.149.139.1:10001",
"http://115.236.83.1:1111",
"http://115.48.22.1:9901",
"http://115.48.63.1:9901",
"http://116.128.224.1:9901",
"http://116.128.242.1:9901",
"http://116.167.111.1:9901",
"http://116.167.76.1:9901",
"http://116.167.79.1:9901",
"http://116.227.232.1:7777",
"http://116.233.34.1:7777",
"http://116.30.121.1:8883",
"http://116.31.165.1:280",
"http://116.31.165.1:3079",
"http://116.31.165.1:6666",
"http://117.27.190.1:9998",
"http://117.90.196.1:6000",
"http://118.248.168.1:8088",
"http://118.248.169.1:8088",
"http://118.248.216.1:8088",
"http://118.81.106.1:9999",
"http://118.81.107.1:9999",
"http://119.125.134.1:7788",
"http://119.163.228.1:9901",
"http://120.0.52.1:8086",
"http://120.0.8.1:8086",
"http://121.19.134.1:808",
"http://121.232.178.1:5000",
"http://121.232.187.1:6000",
"http://121.33.239.1:9901",
"http://122.188.62.1:8800",
"http://123.129.70.1:9901",
"http://123.130.84.1:8154",
"http://123.138.216.1:9902",
"http://123.138.22.1:9901",
"http://123.139.57.1:9901",
"http://123.154.154.1:9901",
"http://123.182.247.1:4433",
"http://124.126.4.1:9901",
"http://124.128.73.1:9901",
"http://124.231.213.1:9999",
"http://125.106.86.1:9901",
"http://125.107.177.1:9901",
"http://125.125.234.1:9901",
"http://14.106.236.1:9901",
"http://14.106.239.1:9901",
"http://171.8.75.1:8011",
"http://180.113.102.1:5000",
"http://180.117.149.1:9901",
"http://180.124.146.1:60000",
"http://180.175.163.1:7777",
"http://180.213.174.1:9901",
"http://182.113.206.1:9901",
"http://182.117.136.1:9901",
"http://202.100.46.1:9901",
"http://210.22.75.1:9901",
"http://218.74.169.1:9901",
"http://218.76.32.1:9901",
"http://218.87.237.1:9901",
"http://220.161.206.1:9901",
"http://220.179.68.1:9901",
"http://220.180.112.1:9901",
"http://220.249.114.1:9901",
"http://221.2.148.1:8154",
"http://221.205.128.1:9999",
"http://221.205.129.1:9999",
"http://221.205.130.1:9999",
"http://221.205.131.1:9999",
"http://221.233.192.1:1111",
"http://222.134.245.1:9901",
"http://222.243.221.1:9901",
"http://223.166.234.1:7777",
"http://223.241.247.1:9901",
"http://223.68.201.1:9901",
"http://27.14.163.1:9901",
"http://27.14.84.1:9901",
"http://27.8.192.1:9901",
"http://27.8.233.1:9901",
"http://27.8.243.1:9901",
"http://36.249.150.1:9901",
"http://36.249.151.1:9901",
"http://36.40.236.1:9999",
"http://36.44.157.1:9901",
"http://36.99.206.1:9901",
"http://47.104.163.1:9901",
"http://47.116.70.1:9901",
"http://49.232.48.1:9901",
"http://49.234.31.1:7004",
"http://58.17.116.1:9908",
"http://58.19.244.1:1111",
"http://58.209.101.1:9901",
"http://58.216.229.1:9901",
"http://58.220.219.1:9901",
"http://58.23.27.1:9901",
"http://58.243.224.1:9901",
"http://58.243.93.1:9901",
"http://58.48.37.1:1111",
"http://58.48.5.1:1111",
"http://59.173.183.1:9901",
"http://59.63.22.1:8888",
"http://60.169.254.1:9901",
"http://60.172.59.1:9901",
"http://60.174.86.1:9901",
"http://61.136.172.1:9901",
"http://61.136.67.1:50085",
"http://61.156.228.1:8154",
"http://61.173.144.1:9901"
    # 添加更多 URL
]

# 修改 URL 的函数
def modify_urls(url):
    modified_urls = []
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find(":", ip_start_index)
    base_url = url[:ip_start_index]  # http:// 或 https://
    ip_address = url[ip_start_index:ip_end_index]
    port = url[ip_end_index:]
    ip_end = "/iptv/live/1000.json?key=txiptv"
    for i in range(1, 256):
        modified_ip = f"{ip_address[:-1]}{i}"
        modified_url = f"{base_url}{modified_ip}{port}{ip_end}"
        modified_urls.append(modified_url)

    return modified_urls

# 检查 URL 可访问性
def is_url_accessible(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            return url
    except requests.exceptions.RequestException:
        pass
    return None

# 去重处理后的 URLs
x_urls = []
for url in urls:  # 对 urls 进行处理，ip 第四位修改为 1，并去重
    url = url.strip()
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find(":", ip_start_index)
    ip_dot_start = url.find(".") + 1
    ip_dot_second = url.find(".", ip_dot_start) + 1
    ip_dot_three = url.find(".", ip_dot_second) + 1
    base_url = url[:ip_start_index]  # http:// or https://
    ip_address = url[ip_start_index:ip_dot_three]
    port = url[ip_end_index:]
    ip_end = "1"
    modified_ip = f"{ip_address}{ip_end}"
    x_url = f"{base_url}{modified_ip}{port}"
    x_urls.append(x_url)

urls = set(x_urls)  # 去重得到唯一的 URL 列表

valid_urls = []
# 使用多线程获取可用的 URL
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    futures = []
    for url in urls:
        url = url.strip()
        modified_urls = modify_urls(url)
        for modified_url in modified_urls:
            futures.append(executor.submit(is_url_accessible, modified_url))

    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result:
            valid_urls.append(result)

for url in valid_urls:
    print(url)

# 遍历网址列表，获取 JSON 文件并解析
for url in valid_urls:
    try:
        ip_start_index = url.find("//") + 2
        ip_dot_start = url.find(".") + 1
        ip_index_second = url.find("/", ip_dot_start)
        base_url = url[:ip_start_index]  # http:// or https://
        ip_address = url[ip_start_index:ip_index_second]
        url_x = f"{base_url}{ip_address}"

        json_url = f"{url}"
        response = requests.get(json_url, timeout=0.5)
        json_data = response.json()

        try:
            # 解析 JSON 文件，获取 name 和 url 字段
            for item in json_data['data']:
                if isinstance(item, dict):
                    name = item.get('name')
                    urlx = item.get('url')
                    if ',' in urlx:
                        urlx = f"aaaaaaaa"
                    if 'http' in urlx:
                        urld = f"{urlx}"
                    else:
                        urld = f"{url_x}{urlx}"

                    if name and urlx:
                        # 删除特定文字
                        name = name.replace("cctv", "CCTV")
                        name = name.replace("中央", "CCTV")
                        name = name.replace("央视", "CCTV")
                        name = name.replace("高清", "")
                        name = name.replace("超高", "")
                        name = name.replace("HD", "")
                        name = name.replace("标清", "")
                        name = name.replace("频道", "")
                        name = name.replace("-", "")
                        name = name.replace(" ", "")
                        name = name.replace("PLUS", "+")
                        name = name.replace("＋", "+")
                        name = name.replace("(", "")
                        name = name.replace(")", "")
                        name = re.sub(r"CCTV(\d+)台", r"CCTV\1", name)
                        name = name.replace("CCTV1综合", "CCTV1")
                        name = name.replace("CCTV2财经", "CCTV2")
                        name = name.replace("CCTV3综艺", "CCTV3")
                        name = name.replace("CCTV4国际", "CCTV4")
                        name = name.replace("CCTV4中文国际", "CCTV4")
                        name = name.replace("CCTV4欧洲", "CCTV4")
                        name = name.replace("CCTV5体育", "CCTV5")
                        name = name.replace("CCTV6电影", "CCTV6")
                        name = name.replace("CCTV7军事", "CCTV7")
                        name = name.replace("CCTV7军农", "CCTV7")
                        name = name.replace("CCTV7农业", "CCTV7")
                        name = name.replace("CCTV7国防军事", "CCTV7")
                        name = name.replace("CCTV8电视剧", "CCTV8")
                        name = name.replace("CCTV9记录", "CCTV9")
                        name = name.replace("CCTV9纪录", "CCTV9")
                        name = name.replace("CCTV10科教", "CCTV10")
                        name = name.replace("CCTV11戏曲", "CCTV11")
                        name = name.replace("CCTV12社会与法", "CCTV12")
                        name = name.replace("CCTV13新闻", "CCTV13")
                        name = name.replace("CCTV新闻", "CCTV13")
                        name = name.replace("CCTV14少儿", "CCTV14")
                        name = name.replace("CCTV15音乐", "CCTV15")
                        name = name.replace("CCTV16奥林匹克", "CCTV16")
                        name = name.replace("CCTV17农业农村", "CCTV17")
                        name = name.replace("CCTV17农业", "CCTV17")
                        name = name.replace("CCTV5+体育赛视", "CCTV5+")
                        name = name.replace("CCTV5+体育赛事", "CCTV5+")
                        name = name.replace("CCTV5+体育", "CCTV5+")
                        name = name.replace("兵器科技", "CCTV-兵器科技")
                        name = name.replace("第一剧场", "CCTV-第一剧场")
                        name = name.replace("风云足球", "CCTV-风云足球")
                        name = name.replace("世界地理", "CCTV-世界地理")
                        name = name.replace("风云音乐", "CCTV-风云音乐")
                        name = name.replace("风云剧场", "CCTV-风云剧场")
                        name = name.replace("怀旧剧场", "CCTV-怀旧剧场")
                        name = name.replace("文化精品", "CCTV-文化精品")
                        name = name.replace("女性时尚", "CCTV-女性时尚")
                        name = name.replace("电视指南", "CCTV-电视指南")
                        name = name.replace("高尔夫网球", "CCTV-高尔夫网球")
                        results.append(f"{name},{urld}")
        except Exception:
            continue
    except Exception:
        continue

channels = []

for result in results:
    line = result.strip()
    if result:
        channel_name, channel_url = result.split(',')
        channels.append((channel_name, channel_url))

# 线程安全的队列
task_queue = Queue()

# 线程安全的列表
results = []
error_channels = []

# 定义工作线程函数
def worker():
    while True:
        channel_name, channel_url = task_queue.get()
        try:
            channel_url_t = channel_url.rstrip(channel_url.split('/')[-1])  # m3u8 链接前缀
            lines = requests.get(channel_url, timeout=1).text.strip().split('\n')
            ts_lists = [line.split('/')[-1] for line in lines if not line.startswith('#')]
            ts_lists_0 = ts_lists[0].rstrip(ts_lists[0].split('.ts')[-1])
            ts_url = channel_url_t + ts_lists[0]

            with eventlet.Timeout(5, False):
                start_time = time.time()
                content = requests.get(ts_url, timeout=1).content
                end_time = time.time()
                response_time = (end_time - start_time) * 1

            if content:
                with open(ts_lists_0, 'ab') as f:
                    f.write(content)
                file_size = len(content)
                download_speed = file_size / response_time / 1024
                normalized_speed = min(max(download_speed / 1024, 0.001), 100)
                result = channel_name, channel_url, f"{normalized_speed:.3f} MB/s"
                results.append(result)
        except Exception:
            error_channel = channel_name, channel_url
            error_channels.append(error_channel)
        task_queue.task_done()

# 创建多个工作线程
num_threads = 10
for _ in range(num_threads):
    t = threading.Thread(target=worker, daemon=True)
    t.start()

# 添加下载任务到队列
for channel in channels:
    task_queue.put(channel)

# 等待所有任务完成
task_queue.join()
