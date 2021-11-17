#!/usr/bin/env Python
#
##
###		ISBN finder version 1.0
####
#####		by Gabe Fierro
####
###		Written 30 November 2008
##
#
import urllib, re, sys, socket
try:
	import psyco
	psyco.full()
except:
	pass
from urllib import FancyURLopener
from random import choice
from optparse import OptionParser
def findMode(list1,list2):
	listNew=list1+list2
	commonisbn=[]
	for item in listNew:
		item=int(item)
	listNew.sort()
	for item in listNew:
		item=str(item)
	for isbnNumber in listNew:
		if isbnNumber[:3]=='978':
			isbnNumber=isbnNumber[3:]
	for isbnNumber in listNew:
		if listNew.count(isbnNumber) > 1:
			commonisbn.append(isbnNumber)
	return commonisbn[0]
usage = "usage: %prog [options]"
parser = OptionParser(prog='isbnfinder.py', usage=usage)
parser.add_option('-a','--author',dest='author',action='store_true', help="author's name <=enclose in single quotation marks ''")
parser.add_option('-t','--title',dest='title',action='store_true', help="title <=enclose in single quotation marks ''")
parser.add_option('-p','--publisher',dest='publisher',action='store_true', help="publisher <=enclose in single quotation marks ''")
parser.add_option('-i','--time_to_live',dest='time_to_live',action='store_true', help="number of seconds to try on each web page before giving up [default 3]")
parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
    help='display searched pages and user-agent for each search [default false]')
parser.add_option('-m','--use_more_pages',dest='use_more_pages',action='store_true',help='search more web pages for isbn numbers. Slower, but more data. Specify number [default 1]')
parser.add_option('-u', '--display_user_agent', dest='display_user_agent', action='store_true',
    help='display the current user agent [default false]')
parser.add_option('-l', '--display_link', dest='display_link', action='store_true',
    help='display the current link [default false]')
parser.add_option('-s','--hide_status_bar',dest='hide_status_bar',action='store_true', help='hide the status bar [default false]')
parser.add_option('-o', '--show_all_isbn', dest='show_all_isbn', action='store_true',
    help='display all found isbn numbers [default false]')
parser.add_option('-e','--hide_error_messages',dest='hide_error_messages',action='store_true',help='hide error messages [default false]')
options, args = parser.parse_args()
user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
]
if options.time_to_live:
	try:
		socket.setdefaulttimeout(float(sys.argv[int(sys.argv.index('-i')+1)]))
	except:
		socket.setdefaulttimeout(float(sys.argv[int(sys.argv.index('--time_to_live')+1)]))
else:
	socket.setdefaulttimeout(3)
class MyOpener(FancyURLopener):
	version=choice(user_agents)
newOpener=MyOpener()
if options.author:
	try:
		author=sys.argv[(sys.argv.index('-a')+1)]
	except:
		author=sys.argv[(sys.argv.index('--author')+1)]
else:
	author=' '
if options.title:
	try:
		title=sys.argv[(sys.argv.index('-t')+1)]
	except:
		title=sys.argv[(sys.argv.index('--title')+1)]
else:
	title=' '
if options.publisher:
	try:
		publisher=sys.argv[(sys.argv.index('-p')+1)]
	except:
		publisher=sys.argv[(sys.argv.index('--publisher')+1)]
else:
	publisher=' '
if (not options.author or author==' ') and (not options.title or title==' '):
	print 'please provide sufficient information [use options -a and -t to provide author and title for book]'
	sys.exit()
author=author.split(' ')
title=title.split(' ')
publisher=publisher.split(' ')
searchQuery=''
for word in title:
	searchQuery=searchQuery+'+'+word
if author:
	for word in author:
		searchQuery=searchQuery+'+'+word
if publisher:
	for word in publisher:
		searchQuery=searchQuery+'+'+word
urllist=[]
isbnNumbers=[]
links=[]
actualLinks=[]
linkFormat=re.compile('http://[a-z\cA-\cZ\.&%#?!/=\+;:0-9\-]+')
httpTest=re.compile('http://[0-9\.]+')
if options.use_more_pages:
	try:
		numPages=sys.argv[(sys.argv.index('-m')+1)]
	except:
		numPages=sys.argv[(sys.argv.index('--use_more_pages')+1)]
else:
	numPages=1
for page in range(0,int(numPages)):
	urllist.append('http://www.google.com/search?hl=en&q=%s+isbn&start=%s&sa=N' % (searchQuery, str(int(page)*10)))

for url in urllist:
	try:
		websitelist=newOpener.open(url)
		googleSearchpage=websitelist.read()
	except:
		print "Error! Now trying next link. Try again the same settings, or try using the -i option to set a longer time_to_live."
	googleSearchpage=googleSearchpage.split('<')
	for link in googleSearchpage:
		if '.google.com' in link:
			if 'book.google.com' not in link:
				continue
		if '.youtube.com' in link:
			continue
		if '.answers.com' in link:
			continue
		if '.textbookx.com' in link:
			continue
		httpMatch=httpTest.search(link)
		if httpMatch:
			continue
		matchAnyLink=linkFormat.search(link)
		if matchAnyLink:
			newLink=matchAnyLink.group()
			links.append(newLink)
for link in links:
	class MyOpener(FancyURLopener):
		version=choice(user_agents)
	classInstance=MyOpener()
	if options.verbose:
		print 'Using Random User-Agent:',classInstance.version
		print 'Using link:', link
	if options.display_user_agent:
		print 'Using Random User-Agent:',classInstance.version
	if options.display_link:
		print 'Using link:',link
	if not options.hide_status_bar:
		overwrite = 0
		sys.stdout.write("%s%s\r" % (("="*(links.index(link)+1)+">"+str(round(float((links.index(link)+1))/float(len(links)),3)*100)+"%"), " "*overwrite))
		sys.stdout.flush()
		overwrite = len("="*(links.index(link)+1)+">")
	try:
		website=classInstance.open(link)
	except:
		if not options.hide_error_messages:
			print 'Link',link,'failed. Choosing next link.'
		continue
	try:
		content=website.read()
	except:
		content=''
	num=re.compile('isbn.{0,5}[0-9\-]+')
	matchnum=num.search(content)
	if matchnum:
		isbnNumbers.append(matchnum.group())
isbn13=[]
isbn10=[]
num=re.compile('[0-9\-]+')
for isbn in isbnNumbers:
	match=num.search(isbn)
	if match:
		if len(match.group())==13:
			isbn13.append(match.group())
		if len(match.group())==10:
			isbn10.append(match.group())
if not options.show_all_isbn:
	try:
		isbn=findMode(isbn13,isbn10)
		if isbn[:3]=='978':
			print 'isbn:','(978)'+isbn[3:]
		else:
			print 'isbn:','(978)'+isbn
	except:
		print ''
		print '13 digit isbn:',isbn13
		print '10 digit isbn:',isbn10
if options.show_all_isbn:
	print ''
	if isbn13!=[]:
		print '13 digit isbn:',isbn13
	if isbn10!=[]:
		print '10 digit isbn:',isbn10
		
##NOW TO SUBMIT THIS TO EASYBIB.COM

