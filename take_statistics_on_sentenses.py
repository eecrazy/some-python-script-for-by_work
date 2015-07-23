#coding:utf8
#clean_data数据经过统计写入noorder，noorder经过排序生成用于插入数据库的数据
import operator
import MySQLdb
import time
import datetime
import time
import MySQLdb.cursors
import sys
from  math import log
reload(sys)
sys.setdefaultencoding('utf8')


def take_statistics():
	my_hash={}
	word_count_hash={}
	for i in range(12):#一个月一个月的处理
		fname=str(i+1)
		my_hash.clear()
		word_count_hash.clear()
		for line in open("single_word/"+sys.argv[1]):
			line=line.strip().split("\t\t")
			if line[0]!=fname:
				continue
			if len(line)!=2:
				continue
			line[1]=line[1].strip()
			seg=line[1].split(" ")
			seg=list(set(seg))#一句话中一个词出现多次只当做一次来算
			for word in seg:
				if len(word)!=3:#提取单字
					continue
				if word not in word_count_hash:
					word_count_hash[word]=0
				word_count_hash[word]+=1
				key=word+"\t"+str(line[0])
				if key not in my_hash:
					my_hash[key]={}
				for w in seg:
					if len(w)==3:#去除单字
						continue
					if word==w:#一句话中自身与自身
						continue
					if w not in my_hash[key]:
						my_hash[key][w]=0
					my_hash[key][w]+=1
		p=open("noorder_single/"+sys.argv[1],"a")
		for key in my_hash:
			p.write(key)
			p.write("\t")
			word=key.split("\t")[0]
			p.write(str(word_count_hash[word]))
			ss="\t"
			for kk in my_hash[key]:
				ss+=kk+" "+str(my_hash[key][kk])+" "
			p.write(ss)
			p.write("\n")
		p.close()

if __name__ == '__main__':
	take_statistics()