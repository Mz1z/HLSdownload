# HLSdownload

> author: Mz1
>
> email: mzi_mzi@163.com
>
> 更新日期：2023/3/16

适用于无损下载B站（bilibili）直播的python小工具。

如有问题可以issue~



## requirements

```
requests
```



## usage

main.py下面修改直播间房号即可【下载完的视频存放在tmp文件夹中】：

```python
if __name__ == '__main__':
	download(xxxxxxx)   # 填写房间号
```



## problem

有的特殊流地址用正则处理会出问题，有待修复。