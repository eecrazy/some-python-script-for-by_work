#coding:utf8
#生成data文件
import commands
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
	num=0
	os.chdir("dcc_2012")
	for paper_name in os.listdir(os.path.expanduser(".")):
		if paper_name==".DS_Store":
			continue
		# print paper_name
		os.chdir(paper_name)
		# print os.getcwd() 

		for year in os.listdir(os.path.expanduser(".")):
			if year==".DS_Store":
				continue
			os.chdir(year)
			# print os.getcwd() 
			for month in os.listdir(os.path.expanduser(".")):
				if month==".DS_Store":
					continue
				os.chdir(month)
				# print os.getcwd() 
				for day in os.listdir(os.path.expanduser(".")):
					if day==".DS_Store":
						continue
					os.chdir(day)
					# print os.getcwd() 
					now_date=year+"-"+month+"-"+day
					for file_name in os.listdir(os.path.expanduser(".")):
						if file_name==".DS_Store":
							continue
						# print file_name
						for line in open(os.path.expanduser(file_name)):
							line=line.strip()
							try:
								pass
								# print paper_name+"\t\t"+now_date+"\t\t"+line.decode("gb2312").encode("utf8")
							except:
								num+=1
								# pass
					os.chdir("..")
					# print os.getcwd() 
				os.chdir("..")
				# print os.getcwd() 
			os.chdir("..")
			# print os.getcwd() 
		os.chdir("..")
		# print os.getcwd() 
	print num


def hehe():
	for line in open("/Users/lzy/workspace/by_work/dcc_2012/中国青年报/2012/1/01/00000000.txt"):
		print line.decode("gbk")

if __name__ == '__main__':
	main()
	# hehe()