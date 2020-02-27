# install
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
