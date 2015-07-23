#coding:utf8
#简单的根据句号“。！？& ……”来断句，并根据词性去除部分虚词
#生成clean_data文件

'''
，/w
了/y
啊/y
★/x
——11/x
的/u
等/u
从/p
对/p
对于/p
在/p
亿/m
3.1/m
2011年/t
过去/t
2009年6月26日/t
当时/t
（t.cyol.com）/x
'''
import sys

stop_words_list=["w","y","x","u","p","m","t"]
def main():
	stop_words_hash={}
	for line in open("stop.words"):
		line=line.strip()
		stop_words_hash[line]=1

	for line in open("raw_data/paper_"+sys.argv[1]):
		line=line.strip().split("\t\t")
		if len(line)!=3:
			continue
		#分句
		line[2]=line[2].replace("？/w","。/w")
		line[2]=line[2].replace("！/w","。/w")
		line[2]=line[2].replace("……/w","。/w")
		sentence=line[2].split("。/w")
		#根据词性以及一些长度限制去除一部分停用词，可以自己设置词过滤规则
		for item in sentence:
			if len(item.strip())==0:
				continue
			# print line[0]+"\t\t"+line[1]+"\t\t",
			print str(int(line[1].split("-")[1]))+"\t\t",
			item=item.strip()
			ss=""
			seg=item.split(" ")
			for word in seg:
				sen=word
				word=word.split("/")
				#词过滤规则
				if len(sen.strip())==0 or len(word)!=2 or word[1] in stop_words_list or word[0] in stop_words_hash:
					continue
				ss=ss+word[0].strip()
				ss+=" "
			if len(ss.strip())==0:
				continue
			print ss


if __name__ == '__main__':
	main()
