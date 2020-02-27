## install
### dlib error
首先，安装gcc和gcc-c++
```
yum install gcc gcc-c++
```
然后，再安装cmake，boost编译dlib
```
yum install cmake boost
```
最后，安装依赖python的库
```
yum install opencv opencv-python opencv-devel python-devel numpy
```
至此，安装了这些依赖包之后，再安装dlib，就容易了。
```
pip install dlib -i https://pypi.douban.com/simple/
```

### due to an EnvironmentError: [Errno 28] No space left on device
这和所要安装的包好像没有太大关系,是因为服务器上的/tmp空间不足，直接`rm -rf /tmp`
或者`export TMPDIR=/home/$USER/tmp`

### cv2和psycopg2
`pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ opencv-python psycopg2-binary`

### centos python No module named 'tkinter'解决办法
`sudo yum install python36-tkinter`
