#!/usr/bin/env python

import mechanize
from bs4 import BeautifulSoup, SoupStrainer
import re
import MySQLdb
import time
import datetime

#Create Browser needed to login and navigate
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [("User-agent", "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]  

#Sign into mTurk
sign_in = br.open('https://www.mturk.com/mturk/beginsignin')  

br.select_form(name="signIn")  
br["email"] = 'gmail.com' 
br["password"] = 'pass'
logged_in = br.submit()

#Connect to MySQL and create cursor object for executing queries
db = MySQLdb.connect(host="localhost", user="mturk", passwd="mturk", db="mturk")
cur = db.cursor()

#Go to search
searchWords = ""
minReward = ""
qualifiedFor = ""
iterate = 0
ignore_list = ['CrowdSource','Turk Experiment','Jon Brelig']
while True:
	cur.execute("""SELECT hitLink FROM `mturk`.`tickerdb` ORDER BY postedTime DESC LIMIT 7;""")
	current_links = cur.fetchall()
	delete_list=[]
	for link in current_links:
		check_link = br.open(str(link[0]))
		check_soup = check_link.read()
		check_soup = BeautifulSoup(check_soup)
		check_res = check_soup.find_all(id="alertboxHeader")
		if len(check_res) > 0 and "There are no more available HITs" in check_res[0].contents:
			cur.execute("""DELETE FROM tickerdb WHERE hitLink = %s;""", link)
		else: pass
	db.commit()
	search = br.open('https://www.mturk.com/mturk/searchbar?selectedSearchType=hitgroups&searchWords=&sortType=LastUpdatedTime%3A1&minReward=0.03&qualifiedFor=on')

	#Insert search into BeautifulSoup
	search_soup = search.read()
	search_soup = BeautifulSoup(search_soup)

	#Begin parsing search
	title_res = search_soup.find_all(attrs={"class": "capsulelink"})

	hit_dict = {}

	title_count = 0
	link_list = []
	for x in title_res:
		title_count += 1
		if title_count%2==0:
			mover = BeautifulSoup(str(x))
			mover = mover.find_all('a', href=True)
			link_list.append(mover[0]['href'])
		else:
			link_list.append(str(x.contents[0]).strip())

	search_res = search_soup.find_all("td", {"class": "capsule_field_text"})
	try:
		hit_dict[link_list[1]] = ["https://www.mturk.com" + str(link_list[1]).encode('utf-8'), str(search_res[0].contents[1].contents[0]).strip(), str(search_res[2].contents[0]).strip(), str(search_res[3].contents[0]).strip().strip('<span class="reward">').strip('</span>'), str(search_res[4].contents[0]).strip(), str(link_list[0])]
		hit_dict[link_list[3]] = ["https://www.mturk.com" + str(link_list[3]).encode('utf-8'), str(search_res[7].contents[1].contents[0]).strip(), str(search_res[9].contents[0]).strip(), str(search_res[10].contents[0]).strip().strip('<span class="reward">').strip('</span>'), str(search_res[11].contents[0]).strip(), str(link_list[2])]
		hit_dict[link_list[5]] = ["https://www.mturk.com" + str(link_list[5]).encode('utf-8'), str(search_res[14].contents[1].contents[0]).strip(), str(search_res[16].contents[0]).strip(), str(search_res[17].contents[0]).strip().strip('<span class="reward">').strip('</span>'), str(search_res[18].contents[0]).strip(), str(link_list[4])]
		hit_dict[link_list[7]] = ["https://www.mturk.com" + str(link_list[7]).encode('utf-8'), str(search_res[21].contents[1].contents[0]).strip(), str(search_res[23].contents[0]).strip(), str(search_res[24].contents[0]).strip().strip('<span class="reward">').strip('</span>'), str(search_res[25].contents[0]).strip(), str(link_list[6])]
		hit_dict[link_list[9]] = ["https://www.mturk.com" + str(link_list[9]).encode('utf-8'), str(search_res[28].contents[1].contents[0]).strip(), str(search_res[30].contents[0]).strip(), str(search_res[31].contents[0]).strip().strip('<span class="reward">').strip('</span>'), str(search_res[32].contents[0]).strip(), str(link_list[8])]
		hit_dict[link_list[11]] = ["https://www.mturk.com" + str(link_list[11]).encode('utf-8'), str(search_res[35].contents[1].contents[0]).strip(), str(search_res[37].contents[0]).strip(), str(search_res[38].contents[0]).strip().strip('<span class="reward">').strip('</span>'), str(search_res[39].contents[0]).strip(), str(link_list[10])]
		hit_dict[link_list[13]] = ["https://www.mturk.com" + str(link_list[13]).encode('utf-8'), str(search_res[42].contents[1].contents[0]).strip(), str(search_res[44].contents[0]).strip(), str(search_res[45].contents[0]).strip().strip('<span class="reward">').strip('</span>'), str(search_res[46].contents[0]).strip(), str(link_list[12])]
		hit_dict[link_list[15]] = ["https://www.mturk.com" + str(link_list[15]).encode('utf-8'), str(search_res[49].contents[1].contents[0]).strip(), str(search_res[51].contents[0]).strip(), str(search_res[52].contents[0]).strip().strip('<span class="reward">').strip('</span>'), str(search_res[53].contents[0]).strip(), str(link_list[14])]
		hit_dict[link_list[17]] = ["https://www.mturk.com" + str(link_list[17]).encode('utf-8'), str(search_res[56].contents[1].contents[0]).strip(), str(search_res[58].contents[0]).strip(), str(search_res[59].contents[0]).strip().strip('<span class="reward">').strip('</span>'), str(search_res[60].contents[0]).strip(), str(link_list[16])]
		hit_dict[link_list[19]] = ["https://www.mturk.com" + str(link_list[19]).encode('utf-8'), str(search_res[63].contents[1].contents[0]).strip(), str(search_res[65].contents[0]).strip(), str(search_res[66].contents[0]).strip().strip('<span class="reward">').strip('</span>'), str(search_res[67].contents[0]).strip(), str(link_list[18])]
	except: 
		print link_list
		print len(link_list)
		print search_res
		print len(search_res)
	for x,y in hit_dict.iteritems():
		if y[1] in ignore_list: print y[1]
		else:
			replace_statement = "REPLACE INTO mturk.tickerdb(hitLink,requesterName,hitTimer,hitReward,hitCount,hitTitle,postedTime) VALUES(%s, %s, %s, %s, %s, %s, NOW());"
			cur.execute(replace_statement, (y[0],y[1],y[2],y[3],y[4],y[5]))
	db.commit()
	time.sleep(5)
	iterate += 1
