#coding:utf8
#xml_parser.py

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os


import  xml.dom.minidom

from BeautifulSoup import BeautifulSoup #html
from BeautifulSoup import BeautifulStoneSoup #xml

def process_html(fname):
	html=open(fname).read()
	soup = BeautifulSoup(html)

	for item in  soup.findAll('b'):
		print item.text

	for item in  soup.findAll('p'):
		if "网站简介" in item.text:
			break
		print item.text
		# print item.nextSibling


# /Volumes/lzy_disk/北语语料/新浪新闻/20071212_20131111/
# 20071212_20131111/20071212
def process_xml():
	os.chdir("20071212_20131111")
	for dir_name in os.listdir(os.path.expanduser(".")):
		if dir_name==".DS_Store":
			continue
		print "zzllzy-"+dir_name
		os.chdir(dir_name)
		# print os.getcwd() 

		for fname in os.listdir(os.path.expanduser(".")):
			if fname==".DS_Store" or "xml" not in fname:
				continue
			xml=open(os.path.expanduser(fname)).read()
			soup=BeautifulStoneSoup(xml)
			# print soup.root.ent
			p=soup.findAll('news')
			for item in  p:
				print item.title.text
				print item.content.text
		os.chdir("..")
	# os.chdir("..")


if __name__ == '__main__':
	# process_html("1.html")
	process_xml("ent.xml")




