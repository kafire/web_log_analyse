# web_log_parse
####  1、适用场景

​	经常有web应用应急响应的事情过来，一般客户的需求都是希望追踪溯源、查杀后门，web服务器的记录的访问日志是开展溯源工作的重要分析源，由于常见的WEB服务器往往以文本的形式存储access_log的，当有大量日志文件需要分析的时候，最好的方式是放到数据库，可以更为灵活的检索、分析。

####2、iis_log_sqlite.py

​	iis_log_sqlite.py主要实现了把多个分散的iis日志文件合并到一起存到sqlite里，默认需要在IIS中勾选启用日志记录。

- iis6默认日志路径：C:\Windows\System32\LogFiles， 
- iis7默认日志路径：C:\inetpub\logs\LogFiles



#### 2、nginx_log_sqlite.py

​	nginx_log_sqlite.py主要实现了把多个分散的nginx日志文件合并到一起存到sqlite里，需要在nginx开启nginx日志记录。

- 在nginx的nginx.conf配置文件找到：log_format 这里就是日志的格式

  ```
  log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '

                                '$status $body_bytes_sent $request_body "$http_referer" '

                                '"$http_user_agent" "$http_x_forwarded_for" "$request_time"';


  ```

  ​

- nginx 默认的日志路径是 /usr/local/nginx/logs/access.log