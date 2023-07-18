# CameraNVR
CameraNVR是一款监控视频自动备份到网盘的工具，目前支持百度网盘和阿里云盘！

可以利用一些价格低廉的设备刷debian，ubuntu，liunx等系统运行此源码，

如：NAS，玩客云，电视盒子，猫盘，手机，矿机，工控机等功耗低的设备。

软件支持：python3.0版本以上！


# 主要功能

#### 1，视频捕获：通过提供的视频流URL，该程序可以捕获实时视频流。

#### 2，运动检测：使用背景减除算法，程序会检测视频中的运动物体，并记录包含运动物体的视频段

#### 3，视频录制：当程序检测到运动时，会开始录制视频，并将包含运动物体的视频段保存在本地

#### 4，视频上传：根据设置，程序可以将录制的视频上传到指定的网盘（百度网盘和/或阿里云网盘）

#### 5，空间管理：自定检测网盘剩余空间，当网盘空间不足时，会删除早期上传的视频文件，以便为新的视频上传腾出空间。



# 安装教程

### 您需要安装以下依赖项：

#### 1，安装pip用于安装和管理Python软件包的命令行工具
执行命令：
sudo apt-get install python3-pip

#### 2，安装bypy百度网盘库，用于百度网盘的文件上传和管理。
执行命令：
pip3 install bypy       （安装百度网盘）
bypy info              （登录百度网盘获取cookie，填写后回车执行）

#### 3，安装aligo阿里云盘库，用于阿里云盘的文件上传和管理。
执行命令：
pip3 install aligo

#### 4，安装OpenCV库，用于视频捕获、处理和录制。您可以通过以下命令使用pip安装：
执行命令：
pip install opencv-python

#### 5，下载源码
执行命令：
apt install git
git clone https://github.com/topak47/CameraNVR.git

修改CameraNVR.py里面的配置：

* Networkdisk = [1]  # 选择网盘 ([1] 表示百度网盘；[2] 表示阿里云网盘；[1, 2]同时选择两个网盘，)
* Cameraname = 'videos'  # 摄像头名称，支持自定义
* videopath = '/Camera/'  # 本地文件路径，支持自定义
* NVRurl = '根据摄像头填写'  # 视频流URL ，根据你摄像头的NVR地址来填写
* videotime = 1  # 录制视频时长（分钟，范围：1-1000）
* Updisk = True  # 是否上传到网盘？（True 表示上传；False 表示不上传）
* deletevd = True  # 上传后是否删除视频文件？（True 表示删除；False 表示保留）
* motion_frame_interval = 3  # 背景减除帧间隔，表示只每隔3帧进行一次运动检测，这样做的目的是为了减少运动检测的频率，节省计算资源。
* Networkdisk_space_threshold = 500  # 网盘剩余空间阈值（GB），当网盘的剩余可用空间低于或等于这个阈值时，系统会删除最早上传的视频，以防止网盘的空间不足。
* upload_threshold = 500  # 视频上传总大小阈值（GB），当视频累计上传到这个阈值后，开始自动检测网盘百度网盘和阿里云盘的空间容量是否足够，不够采取删除！

#### 6，运行
执行命令：
python3 pyNvr.py

运行后阿里云盘用手机扫描登录！


# 常见NVR摄像头码流
国内网络摄像机的端口及RTSP地址
#### 1，海康威视
* 默认IP地址：192.168.1.64/DHCP 用户名admin 密码自己设
* 端口：“HTTP 端口”（默认为 80）、“RTSP 端口”（默认为 554）、“HTTPS 端 口”（默认 443）和“服务端口”（默认 8000），ONVIF端口 80。
* 主码流：rtsp://admin:12345@192.0.0.64:554/h264/ch1/main/av_stream
* 子码流：rtsp://admin:12345@192.0.0.64/mpeg4/ch1/sub/av_stream

#### 2，大华
* 默认IP地址：192.168.1.108 用户名/密码：admin/admin
* 端口：TCP 端口 37777/UDP 端口 37778/http 端口 80/RTSP 端口号默认为 554/HTTPs 443/ONVIF 功能默认为关闭，端口80
* RTSP地址：rtsp://username:password@ip:port/cam/realmonitor?channel=1&subtype=0


#### 3，雄迈/巨峰
* 默认IP地址：192.168.1.10 用户名admin 密码空
* 端口：TCP端口：34567 和 HTTP端口：80，onvif端口是8899
* RTSP地址：rtsp://10.6.3.57:554/user=admin&password=&channel=1&stream=0.sdp?

#### 4，天视通
* 默认IP地址：192.168.0.123 用户名admin 密码123456
* 端口：http端口80 数据端口8091 RTSP端口554 ONVIF端口 80
* RTSP地址：主码流地址:rtsp://192.168.0.123:554/mpeg4
* 子码流地址:rtsp://192.168.0.123:554/mpeg4cif
* 需要入密码的地址： 主码流 rtsp://admin:123456@192.168.0.123:554/mpeg4
* 子码流 rtsp://admin:123456@192.168.0.123:554/mpeg4cif


#### 5，中维/尚维
* 默认IP地址：DHCP 默认用户名admin 默认密码 空
* RTSP地址：rtsp://0.0.0.0:8554/live1.264（次码流）
* rtsp://0.0.0.0:8554/live0.264 (主码流)

#### 6，九安
* RTSP地址：rtsp://IP:port（website port）/ch0_0.264（主码流）
* rtsp://IP:port（website port）/ch0_1.264（子码流）

#### 7，技威/YOOSEE
* 默认IP地址：DHCP 用户名admin 密码123
* RTSP地址：主码流：rtsp://IPadr:554/onvif1
* 次码流：rtsp://IPadr:554/onvif2
* onvif端口是5000
* 设备发现的端口是3702

#### 8，V380
* 默认IP地址：DHCP 用户名admin 密码空/admin
* onvif端口8899
* RTSP地址：主码流rtsp://ip//live/ch00_1
* 子码流rtsp://ip//live/ch00_0

#### 9，宇视
* 默认IP地址： 192.168.0.13/DHCP 默认用户名 admin 和默认密码 123456
* 端口：HTTP 80/RTSP 554/HTTPS 110(443)/onvif端口 80
* RTSP地址：rtsp://用户名:密码@ip:端口号/video123 123对应3个码流

#### 10，天地伟业
* 默认IP地址：192.168.1.2 用户名“Admin”、密码“1111”
* onvif端口号“8080”
* RTSP地址：rtsp：//192.168.1.2

#### 11，巨龙/JVT
* 默认IP地址：192.168.1.88 默认用户名 admin 默认密码admin
* 主码流地址:rtsp://IP地址/av0_0
* 次码流地址:rtsp://IP地址/av0_1
* onvif端口 2000


#### 12，TP-Link/水星安防
* 默认IP地址：192.168.1.4   用户名“Admin”、密码“app里设置”
* 主码流地址:rtsp://user:password@ip:554/stream1
* 次码流地址:rtsp://user:password@ip:554/stream2


# 使用说明
由于能力有限，本源码可能存在缺陷，不保证能用，不要用于商业行为，仅供学习使用！
注意：涉及到有隐私的视频请勿使用本源码，上传到网盘中有可能会造成泄露！

感谢各位大佬的分享的参考源码：
https://github.com/wfxzf/pyNvr

https://github.com/houtianze/bypy

https://github.com/foyoux/aligo

