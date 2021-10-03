#!/usr/bin/env python
import xml.etree.ElementTree as ET
import httplib2
import urllib.request
import io, re, codecs, csv
from collections import namedtuple
import sqlite3




def downloadFile(URL=None):
	'''
		Enregistrer la page dont l'url est transmis
	'''
	url=URL 
	response = urllib.request.urlopen(url)
	data = response.read()      
	text = data.decode('utf-8') # on transforme le résultat en bytes précédent en string 
	h = httplib2.Http(".cache")
	resp, content = h.request(URL, "GET")
	return text

def parseHistory(GetPage):
	''' 
		Cette fonction analyse la page produite par l'API wikipedia et renvoie l'id du dernier enregistrement (lastID)
		ainsi que l'ensemble des lignes dans une liste (ligne)
	'''
	xml=ET.fromstring(GetPage)
	ligne=list()
	for api in xml.iter('api'):
		for query in api.iter('query'):
			for pages in query.iter('pages'):
				for page in pages.iter('page'):
					for revisions in page.iter('revisions'):
						lastId=""
						for rev in revisions.iter('rev'):
							comment=rev.attrib['comment']
							comment=re.sub("\"", "'", comment)
							comment=re.sub(";", ",", comment)
							size=rev.attrib['size'] # c'est mesuré en bytes
							revid=rev.attrib['revid']
							parentid=rev.attrib['parentid']
							user=rev.attrib['user']
							userid=rev.attrib['userid']
							timestamp=rev.attrib['timestamp']
							timestamp=re.sub("[TZ]", " ", timestamp)
							modif= [revid,parentid,user,userid,timestamp,comment,size] # on utilise un tuple
							ligne.append(modif)
							lastId=rev.attrib['revid']
	return ligne,lastId


def NewUrl(lastid,q, lg):
	nid= "&rvstartid=" + lastid
	url="https://" + lg + ".wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=ids|timestamp|user|userid|comment|size|flags|tags&format=xml&titles=" + q +"&rvlimit=500" + nid
	return url


# Un fois de plus les API pour être fonctionnelles limites leurs retours. Il faut donc itérer le processus de collection des données 
ligne=list()
#lg="en"
lg="fr"
separator=";"
#q="Jeanne d'Arc"
#q="Joan of Arc"
q="Discussion:Jeanne_d'Arc"
q=q.replace(" ", "_")
fileOutput="History"+q+".csv"
url="https://"+ lg +".wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=ids|timestamp|user|userid|comment|size|flags|tags&format=xml&titles="+ q +"&rvlimit=500"
print(url)
for i in range(20):
	if i==0:
		GetFile=downloadFile(url)
		text=parseHistory(GetFile)
		result=text[0]
		ThelastId=text[1]
		ligne.append(result)
	elif i>0:
		N=NewUrl(ThelastId,q, lg)
		GetFile=downloadFile(N)
		txt=parseHistory(GetFile)
		result=txt[0]
		ThelastId=txt[1]
		ligne.append(result)


Tofile = open(fileOutput, "w")
for r in ligne:
	for l in r :
		lgn=separator.join(l)
		lgn=re.sub(r"[\n\r]",r"",lgn)
		Tofile.write(lgn)
		Tofile.write("\n")

