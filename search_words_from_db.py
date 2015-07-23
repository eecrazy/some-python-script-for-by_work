#coding:utf8
#将数据插入mysql数据库，建立索引查看查询效果
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

#查询word,返回top_word_count word_set, single_flag=True,则为查询单字结果
def search_by_count(word,month1="1",month2="120",total_count=50,single_flag=False):
	cnx = MySQLdb.connect(user="root", passwd="roo", host="127.0.0.1",db="by_work",charset="utf8", \
		cursorclass=MySQLdb.cursors.DictCursor)
	cursor = cnx.cursor()
	num=0
	query1 = ("SELECT word_set FROM paper_simple WHERE word= %s and month between %s and %s")
	query2 = ("SELECT count FROM paper_simple WHERE word= %s and month between %s and %s")
	query3 = ("SELECT word_set FROM paper_single_word WHERE word= %s and month between %s and %s")
	query4 = ("SELECT count FROM paper_single_word WHERE word= %s and month between %s and %s")
	word_hash={}
	word_hash.clear()
	start=time.clock()

	#查询搭配词集
	if not single_flag:
		cursor.execute(query1,(word,month1,month2))
	else:
		cursor.execute(query3,(word,month1,month2))

	cnx.commit()
	end=time.clock()
	results=cursor.fetchall()
	if len(results)==0:
		print "not found!"
		return []
	sql_time=end-start
	start=time.clock()
	for item in results:
		line=item["word_set"].strip().split(" ")
		index_len=len(line)/2
		for index in xrange(index_len):
 			if line[index*2] not in word_hash:
				word_hash[line[index*2]]=0
			word_hash[line[index*2]]+=int(line[index*2+1])
	sorted_word_hash = sorted(word_hash.iteritems(), key=operator.itemgetter(1), reverse=True)

	#查询word的出现次数
	word_count=0.0
	if not single_flag:
		cursor.execute(query2,(word,month1,month2))
	else:
		cursor.execute(query4,(word,month1,month2))
	results=cursor.fetchall()
	for item in results:
		word_count+=float(item["count"])

	#查询搭配词的出现次数
	other_count={}
	num=0
	for key in sorted_word_hash:
		if num>400:
			break
		cur_count=0.0
		cursor.execute(query2,(key[0],month1,month2))
		results=cursor.fetchall()
		for item in results:
			cur_count+=float(item["count"])
		other_count[key[0]]=cur_count
		num+=1

	#输出并返回结果
	num=0
	ret=[]
	for item in sorted_word_hash:
		# print item[0]+"\t"+str(item[1])+"\t"+str(word_count)+"\t"+str(other_count[item[0]])+"\t"+str(word_hash[item[0]])
		ret.append(item[0])
		num+=1
		if num==total_count:
			break
	end=time.clock()
	print "sql time: %f" % (sql_time)
	print "compute time: %f" % (end-start)
	return ret

'''
MI=log(f(x,y)/N)-log((f(x)/N)*(f(y)/N))
其中：f(x,y)--在当前查找范围内共现的次数
f(x)----关键词在整个语料库中的出现次数
f(y)----上下文中的该词在整个语料库中的出现次数
N-------语料库大小
'''
def compute_mutual_info(count1,count2,count3):
	N=20717699.0
	MI=log(N)+log(count3)-log(count2)-log(count1)
	return MI

def search_by_mi(word,month1="1",month2="120",total_count=50,single_flag=False):
	cnx = MySQLdb.connect(user="root", passwd="roo", host="127.0.0.1",db="by_work",charset="utf8", \
		cursorclass=MySQLdb.cursors.DictCursor)
	cursor = cnx.cursor()
	query1 = ("SELECT word_set FROM paper_simple WHERE word= %s and month between %s and %s")
	query2 = ("SELECT count FROM paper_simple WHERE word= %s and month between %s and %s")
	query3 = ("SELECT word_set FROM paper_single_word WHERE word= %s and month between %s and %s")
	query4 = ("SELECT count FROM paper_single_word WHERE word= %s and month between %s and %s")
	start=time.clock()

	#查询搭配词集
	if not single_flag:
		cursor.execute(query1,(word,month1,month2))
	else:
		cursor.execute(query3,(word,month1,month2))
	cnx.commit()
	results=cursor.fetchall()
	end=time.clock()
	sql_time=end-start
	if len(results)==0:
		print "not find!"
		return []
	print "sql_time:"+str(sql_time)
	word_hash={}
	word_hash.clear()
	start1=time.clock()
	line=""
	for item in results:
		line+=item["word_set"].strip()
		line+=" "
	line=line.strip().split()
	index_len=len(line)/2
	for index in xrange(index_len):
 		if line[index*2] not in word_hash:
			word_hash[line[index*2]]=0
		word_hash[line[index*2]]+=int(line[index*2+1])
	end=time.clock()
	# print "1",end-start1

	#查询词word出现次数：word_count
        start=time.clock()
	word_count=0.0
	if not single_flag:
		cursor.execute(query2,(word,month1,month2))
	else:
		cursor.execute(query4,(word,month1,month2))

	results=cursor.fetchall()
	for item in results:
		word_count+=float(item["count"])
	end=time.clock()
    # print "2",end-start

	#以共现次数为标准筛选top n
	start=time.clock()
	n=400
	sorted_word_hash = sorted(word_hash.iteritems(), key=operator.itemgetter(1), reverse=True)
	mutual_info={}#互信息
	other_count={}#另一个词的出现次数
	num=0
	for key in sorted_word_hash:
		if num>n:
			break
		cur_count=0.0
		cursor.execute(query2,(key[0],month1,month2))
		results=cursor.fetchall()
		for item in results:
			cur_count+=float(item["count"])
		num+=1
		if cur_count<5:
			continue
		other_count[key[0]]=cur_count
		mutual_info[key[0]]=compute_mutual_info(word_count,cur_count,float(word_hash[key[0]]))
        end=time.clock()	
	# print "3",end-start
	#以互信息为标准筛选top n
        start=time.clock()	
	sorted_mutual_info = sorted(mutual_info.iteritems(), key=operator.itemgetter(1), reverse=True)
	num=0
	ret=[]
	for item in sorted_mutual_info:
		# print item[0]+"\t"+str(item[1])+"\t"+str(word_count)+"\t"+str(other_count[item[0]])+"\t"+str(word_hash[item[0]])
		ret.append(item[0])
		num+=1
		if num==total_count:
			break
	end=time.clock()
	# print "4",end-start
	print "compute_time:",end-start1
	return ret

def search():
	while(1):
		word=raw_input("input word:")
		search_by_mi(word)
	return

def search_word(word,year,total_count=50,count_flag=False):
	month1=1+12*(int(year)-2005)
	month2=12+12*(int(year)-2005)
	if count_flag:
		if len(word.strip())!=3:
			print 1
			return search_by_count(word,month1,month2,total_count,single_flag=False)
		else:
			print 2
			return search_by_count(word,month1,month2,total_count,single_flag=True)
	else:
		if len(word.strip())!=3:
			print 3
			return search_by_mi(word,month1,month2,total_count,single_flag=False)
		else:
			print 4
			return search_by_mi(word,month1,month2,total_count,single_flag=True)

if __name__ == '__main__':
	ret=search_word("无",2010,total_count=10,count_flag=True)
	print " ".join(ret)
	print "finish"


	

