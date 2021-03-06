import urllib2
import urlparse
from bs4 import BeautifulSoup
import re
import lxml.html
import sys
import httplib

reload(sys)
sys.setdefaultencoding("utf-8")

# this is supposed to create a list of all the working groups, but is broken - it only scrapes the first 6 lists for some reason. So I've selected the groups to scrape manually, in the wgsAll list below
#def getWGs():
#	page = urllib22.urlopen("https://lists.okfn.org/mailman/listinfo")
#	soup = BeautifulSoup(page)
#	wgs = soup.findAll('strong')

# getWGs()

# selected working group lists to monitor
wgs = ['board-fi','bundesgit','ckan-news','data-catalogs','data-driven-journalism','data-protocols','datahub-discuss','euopendata','members-fi','od-discuss','odc-discuss','offenes-parlament','ogd-fr','ok-berlin','ok-scotland','okf-chapters','oparl-tech','open-access','open-aid-de','open-archaeology','open-bibliography','open-contentmining','open-data-census','open-data-handbook','Open-data-immigration','open-data-nahverkehr','open-development','open-economics','open-education','Open-education-be','open-glam','open-government','open-humanities','open-legislation','open-research-cam','open-science','open-science-de','open-science-fi','open-science-it','Open-science-nl','open-spectrum','Open-sports','open-sustainability','open-sustainability-fi','open-transport','open-visualisation','openbiblio-dev','opendesign','openglam-at','openlawindex','openspending','product','publicdomainreview','ris','school-of-data','school-of-data-announce','science-at','yourtopia']

#full list of all wg mailing lists
wgsAll = ['annotator-dev','avoin-glam-fi','blogsite-admins','blogsite-owners','board-fi','bundesgit','cienciaaberta','ckan-announce','ckan-contributors','ckan-dev','ckan-news','ckan-pt','ckan-updates','ckan-users','ckan4rdm','codeforberlin','codeforchemnitz','Codeforde','Codeforde-cert','Codeforgiessen','codeforhamburg','codeforleipzig','codeformunich','Codeforstuttgart','Codingdavinci','council-projects','data-catalogs','data-driven-journalism','data-edu-au','data-protocols','datahub-discuss','Date-deschise','ddj-de-tools','ddj-nrw','ecoledesdonnees','escoladedados','escuela-de-datos','escuela-de-datos-alertas','euopendata','fossil-bank','fragdenstaat','froide-dev','glam-survey-coordination','iRail','maker-at','members-fi','mydata-open-data','od-discuss','odc-discuss','offener-haushalt','offenes-parlament','ogd-fr','ok-berlin','ok-scotland','okf-chapters','okf-fi','okfestival-discuss','okfestival-volunteers','okfn-ar','okfn-at','okfn-au','okfn-aus-event','okfn-bd','okfn-be','okfn-bf','okfn-bg','okfn-bih','okfn-br','okfn-ca','okfn-ch','okfn-cn','okfn-cz','okfn-de','okfn-discuss','okfn-dk','okfn-dz','okfn-ec','okfn-eg','okfn-en','okfn-fi','okfn-fr','okfn-francophone','okfn-gr','okfn-hk','okfn-hu','okfn-id','okfn-ie','okfn-in','okfn-ir','okfn-irl','okfn-is','okfn-it','okfn-jp','okfn-ke','okfn-kh','okfn-kr','okfn-labs','okfn-latin-america','okfn-lt','okfn-lu','okfn-ma','okfn-md','okfn-mena','okfn-mt','okfn-mx','okfn-ng','okfn-nl','okfn-no','okfn-np','okfn-ph','okfn-py','okfn-ro','okfn-ru','okfn-se','okfn-sn','okfn-sp','okfn-sv','okfn-tw','okfn-us','okfn-us-ma','okfn-us-or','okfn-us-tx','okfn-uy','okfn-volunteers','okfn-za','oparl-tech','open-access','open-aid-de','open-archaeology','open-bibliography','open-contentmining','open-data-census','open-data-handbook','Open-data-immigration','open-data-maker-at','open-data-nahverkehr','Open-design','open-development','open-economics','open-education','Open-education-be','open-geodata','open-glam','open-government','open-hardware','open-humanities','open-legislation','open-linguistics','open-personal-data','open-research-cam','open-science','open-science-de','open-science-dev','open-science-fi','open-science-it','Open-science-nl','open-spectrum','Open-sports','open-sustainability','open-sustainability-fi','open-transport','open-visualisation','openbiblio-dev','opendesign','openglam-at','openlawindex','openspending','openspending-dev','openspending-steering-group','oppilaitosverkosto-fi','os-datawrangling','outages','pd-discuss','product','publicdomainreview','ris','school-of-data','school-of-data-announce','school-of-data-network','science-at','Test-list','yourtopia']


def check_url(url):
	try:
  		f = urllib2.urlopen(urllib2.Request(url))
  		global deadLinkFound
		deadLinkFound = False
	except:
		global deadLinkFound
  		deadLinkFound = True

# gets all the latest message URLs
def getThisMonth(month):
	for wg in wgs:
		url = "https://lists.okfn.org/pipermail/%s/%s-%s/subject.html" % (wg, year, month)
		check_url(url)
		if deadLinkFound:
			print "%s has broken link" % wg
		else:			
			source = urllib2.urlopen(url).read()
			soup = BeautifulSoup(source)
			links = soup.findAll('a')
			indexUrls = []
			messageIds = []
			for link in links:
				indexUrls.append(str(link.get('href')))
			for url in indexUrls:
				if url.startswith('0'):
					messageIds.append(url)
					print url
				else:
					pass
			for messageId in messageIds:
				messageUrls.append("https://lists.okfn.org/pipermail/%s/%s-%s/%s" % (wg, year, month, messageId))
			print "finished searching %s" % wg

# checks the message URL for keywords
def keyCheck(messageUrl, keyword):
	source = urllib2.urlopen(messageUrl).read()
	soup = BeautifulSoup(source)
	if keyword in str(soup):
		subject = soup.h1
		subject = subject.renderContents()
		result = "<p><a href=\"%s\">%s</a></p>" % (messageUrl, subject)
		with open ('%s_%s_%s.html' % (keyword, year, month), 'a') as results:
			results.write(result)
		print 'found %s in %s' % (keyword, messageUrl)
		with open ("README.md", 'a') as readme:
			readme.write("[%s_%s_%s.html](http://rdbinns.github.io/okfn-mail-search/%s_%s_%s.html)\n" % (keyword, year, month, keyword, year, month))
	else:
		pass

keyword1 = str(raw_input("Enter one keyword to search: "))
keyword2 = str(raw_input("Enter another keyword to search: "))
keyword3 = str(raw_input("Enter another keyword to search: "))

keywords = [keyword1, keyword2, keyword3]

year = str(raw_input("Enter year: "))
month = str(raw_input("Enter month: "))

global messageUrls
messageUrls = []

getThisMonth(month)

for keyword in keywords:
	for messageUrl in messageUrls:
		keyCheck(messageUrl, keyword)


