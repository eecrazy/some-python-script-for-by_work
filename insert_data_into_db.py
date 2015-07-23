#coding:utf8
#将数据插入mysql数据库，建立索引查看查询效果
import MySQLdb
import MySQLdb.cursors
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def sql_index_word_md5():
	cnx = MySQLdb.connect(user="root", passwd="roo", host="127.0.0.1",db="by_work", charset='utf8')
	cursor = cnx.cursor()
	add_item = ("INSERT INTO paper_single_word (word,month,count,word_set) VALUES (%s,%s,%s,%s)")
	num=0
	for line in open("noorder_single/single_word"):
		line=line.strip().split("\t")
		if len(line)!=5:
			continue
		num+=1
		month=str(int(line[1])+12*(int(line[4])-2005))
		item = (line[0],month,line[2],line[3])
		try:
			cursor.execute(add_item, item)
		except:
			print num
		if not num%80000:
			cnx.commit()
	cnx.commit()

if __name__ == '__main__':
	sql_index_word_md5()