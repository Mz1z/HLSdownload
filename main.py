import requests
import re
import time
import threading

from bili_get_stream import get_real_url

urls = []   # 全局变量

# 在新线程中刷新m3u8
def flush_m3u8(line):
	global urls
	print('> 启动 flush_m3u8 thread')
	fragments = []    # 用于保存碎片文件名，计算哪些下载过了
	first = True   # 第一次刷新要快，不然会丢帧
	while True:
		print('  > flush m3u8...')
		try:
			m3u8 = requests.get(line).text    # get m3u8
		except Exception as e:
			print(f'> [flush_m3u8] err: {e}')
			continue
		rows = m3u8.split('\n')
		_num = 0     # 计算延时
		for row in rows:    # 整理出视频地址
			if len(row) == 0 or '#' == row[0]:
				continue
			if row not in fragments:
				urls.append(row)
				fragments.append(row)
				_num += 1
				
		if first:   # 第一次快速刷新
			first = False
			continue
			
		if _num > 0:   # 延时检查
			print(f'  > new fragment: {_num}')
			time.sleep(_num-1)    # 延时
		else:
			print('    > too fast')
			time.sleep(3)
	
# 获取直播流地址
def download(room):
	global urls
	url = get_real_url(str(room))
	line = url['线路1']
	print(line)

	# 获取token和url前缀
	token = '?' + line.split('?')[-1]
	print('\n> token: ' + token)
	pre_url = re.findall('^(https://.*?/live-bvc/.*?/.*?/)', line)[0]
	print('\n> pre_url: ' + pre_url)

	# 读取m3u8文件
	m3u8 = requests.get(line).text
	print('\n' + m3u8)

	# 获取#EXT-X-MAP地址
	# 这个文件要作为每一个文件的文件头
	ext_x_map = re.findall('#EXT-X-MAP:URI="(.*?)"', m3u8)[0]
	ext_url = pre_url+ext_x_map+token
	r = requests.get(ext_url)
	head = r.content   # 获取文件头
	
	# 启动刷新m3u8线程
	t = threading.Thread(target=flush_m3u8, args=(line,))
	t.start()

	# 直接合并写入
	with open(f'tmp/{time.strftime("%Y%m%d_%H_%M_%S", time.localtime())}.m4s', 'wb') as f:
		f.write(head)
		while True:
			if len(urls) != 0:
				fname = urls.pop(0)  # pop取出第一个元素fname
				url = pre_url + fname + token
				try:
					r = requests.get(url)
					f.write(r.content)
				except Exception as e:
					print(f'> err: {e}')
					time.sleep(1)
				print(f'  > downloaded: {fname}')
			else:
				time.sleep(2)

	print('over')

if __name__ == '__main__':
	download(21728563)



