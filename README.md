# web_log_parse
####  1、适用场景

​	经常有web应用应急响应的事情过来，一般客户的需求都是希望追踪溯源、查杀后门，web服务器的记录的访问日志是开展溯源工作的重要分析源，由于常见的WEB服务器往往以文本的形式存储access_log的，当有大量日志文件需要分析的时候，最好的方式是放到数据库，可以更为灵活的检索、分析。

​	脚本支持把多个分散（如果）的日志文件合并到一起存到sqlite里。

####2、iis_log_sqlite.py

- iis6默认日志路径：C:\Windows\System32\LogFiles， 
- iis7默认日志路径：C:\inetpub\logs\LogFiles
- GMT时间就是英国格林威治时间，也就是世界标准时间，是本初子午线上的地方时，是0时区的区时，与我国的标准时间北京时间（东八区）相差8小时，即晚8小时，实际时间是要多8个小时，IIS默认使用了GMT时间，所以在分析日志做时间比对的时候要注意。

脚本支持默认的日志格式，如果管理员自定义了日志格式需要修改脚本。

IIS7默认开启日志，默认记录字段如下

> date time s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs(User-Agent) sc-status sc-substatus sc-win32-status time-taken

IIS6默认开启日志，默认字段如下：

>  date time s-sitename s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs(User-Agent) sc-status sc-substatus sc-win32-status 



- 这个脚本是按照IIS6的默认字段写的，后续支持IIS7



#### 2、nginx_log_sqlite.py



- nginx 源码默认的日志路径是 /usr/local/nginx/logs/access.log  或 /var/log/nginx/access.log
- nginx 使用的东八区时间，形如  [29/Nov/2017:18:13:32 +0800] 

nginx默认不开访问日志记录，手工开启需要配置nginx.conf，默认字段如下：

```
log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '

                              '$status $body_bytes_sent $request_body "$http_referer" '

                              '"$http_user_agent" "$http_x_forwarded_for" "$request_time"';


```



#### 3、apache_log_sqlite.py

-  Apache 默认的日志路径是/usr/local/apache/logs/access_log或者/var/log/apache2/access_log

Apache默认开启访问日志记录，手工开启conf目录下的httpd.conf文件，默认配置：

- windows 环境：

ErrorLog "logs/error.log"

LogFormat "%h %l %u %t \"%r\" %>s %b" common

- linux环境：

  Apache默认提供了如下格式模板，默认使用了common

LogFormat "%v:%p %h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"" vhost_combined
LogFormat "%h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"" combined
LogFormat "%h %l %u %t \"%r\" %>s %O" common
LogFormat "%{Referer}i -> %U" referer
LogFormat "%{User-agent}i" agent



> %h 访问的用户IP地址
> %l 访问逻辑用户名，通常返回'-'
> %u 访问验证用户名，通常返回'-'
> %t 访问日时
> %r 访问的方式(post或者是get)，访问的资源和使用的http协议版本
> %s 访问返回的http状态
> %b 访问资源返回的流量
> %T 访问所使用的时间



默认使用了  %h %l %u %t \"%r\" %>s 



#### 4、tomcat_log_sqlite.py

- 首先是配置tomcat访问日志数据，默认情况下访问日志没有打开，配置的方式如下：

编辑 ${catalina}/conf/server.xml 文件.

(注: ${catalina}是tomcat的安装目录,把以下的注释()去掉即可。)

```
<!--
<Valve className="org.apache.catalina.valves.AccessLogValve"
directory="logs"  prefix="localhost_access_log." suffix=".txt"
pattern="common" resolveHosts="false"/>
-->
```

common是tomcat提供的一个标准设置格式。其具体的表达式为 %h %l %u %t "%r" %s %b