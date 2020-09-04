### 在云服务器上配置网站

#### 需要的包

- nginx
- virtualenv 
- pip
- Git

#### nginx虚拟主机
- 参考nginx.template.conf
- 把SITENAME替换成所需的域名，例如staging.leocodec.cn

#### Systemd服务
- 参考gunicorn-systemd.template.service
- 把SITENAME替换成所需的域名，例如staging.leocodec.cn

#### 文件夹结构
- 假设有用户账号，家目录为home/username
- 目录结构如下：
- ![image-20200904144501277](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20200904144501277.png)virtualenv改成venv(虚拟环境一般存储这个文件夹）

