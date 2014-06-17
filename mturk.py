#!/usr/bin/env python

import mechanize
from bs4 import BeautifulSoup, SoupStrainer
import re
import MySQLdb

#Create Browser needed to login and navigate
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [("User-agent", "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]  

#Connect to MySQL and create cursor object for executing queries
db = MySQLdb.connect(host="localhost", user="mturk", passwd="mturk", db="mturk")
cur = db.cursor()

#Sign into mTurk
sign_in = br.open('https://mturk.com/mturk/beginsignin')  

br.select_form(name="signIn")  
br["email"] = 'user@example.com'
br["password"] = 'password'
logged_in = br.submit()


#Go to Dashboard
dashboard = br.open('https://mturk.com/mturk/dashboard')

#Insert Dashboard into BeautifulSoup
dash_soup = dashboard.read()
dash_soup = BeautifulSoup(dash_soup)

#Begin parsing Dashbaord
#approved = str(dash_soup.find_all(id='approved_hits_earnings_amount')[0].text).strip("$").encode("utf-8")
bonus = str(dash_soup.find_all(id='bonus_earnings_amount')[0].text).strip("$").encode("utf-8")
#total = str(dash_soup.find_all(id='total_earnings_amount')[0].text).strip("$").encode("utf-8")
transfer = str(dash_soup.find_all(id='transfer_earnings')[0].text).strip("$").encode("utf-8")

#Get worker ID, and name, store worker values to list
worker_ID = str(dash_soup.find_all('span','orange_text_right')[0].text).strip('Your Worker ID: ').encode("utf-8")
worker_name = str(dash_soup.find_all('span','title_orange_text_bold')[0].text).strip('Dashboard - ').encode("utf-8")
worker_values = [worker_ID,worker_name,bonus,transfer]

#Update/insert worker data into database
worker_statement = """REPLACE INTO mturk.workerdb(workerId,workerName,bonus,transfer) VALUES(%s, %s, %s, %s);"""
cur.execute(worker_statement, [worker_values[0],worker_values[1],worker_values[2],worker_values[3]])

#Begin parsing Hits

#Find dates to update
cur.execute("""SELECT DISTINCT date FROM hitdb WHERE status NOT IN ('Paid','Rejected') AND workerID = %s ORDER BY date;""", [worker_ID])
pending_hits_list = cur.fetchall()
pending_date_list = []
pending_link_list = []

pending_status = br.open('https://mturk.com/mturk/status')
status_soup = pending_status.read()
status_soup = BeautifulSoup(status_soup, parse_only=SoupStrainer('a'))

def gather_status_links():
        for pending_date in pending_hits_list:
                pending_date = str(pending_date[0])
                hitattr = pending_date.split("-")
                dateswap = hitattr[1] + hitattr[2] + hitattr[0]
                pending_date_list.append(dateswap)

        for pending_link in status_soup:
                if pending_link.has_attr('href'):
                        if "statusdetail?encodedDate" in pending_link['href'] and pending_link['href'].split('=')[-1] > max(pending_date_list): pending_link_list.append(pending_link['href'])
                        for pending_date in pending_date_list:
                                if pending_date not in pending_link['href'] or pending_link['href'].split('=')[-1] > max(pending_date_list): continue
                                else: pending_link_list.append(pending_link['href'])


if len(pending_hits_list) == 0:
	cur.execute("""SELECT COUNT(*) FROM hitdb;""")
	hitcount = cur.fetchall()
	if hitcount[0][0] > 0: pass
	else:
		for pending_link in status_soup:
			if pending_link.has_attr('href'):
				if "statusdetail?encodedDate" in pending_link['href']: pending_link_list.append(pending_link['href'])	
else: gather_status_links()


#Find pages that need hits updated
pending_status_list = []
pending_status_temp = []
last_page_picker = []
last_page = 0
for pending_date in pending_link_list:
	pending_status_list.append(pending_date)
	pending_date_link = "https://mturk.com" + pending_date
	page_date_soup = br.open(pending_date_link)
	page_date_soup = page_date_soup.read()
	page_date_soup = BeautifulSoup(page_date_soup, parse_only=SoupStrainer('a'))
	pending_status_temp = []
	for date_chk in page_date_soup:
		if date_chk.has_attr('href'):
			if "pageNumber" not in date_chk['href'] and "statusdetail?encodedDate" not in date_chk['href']: pass
			elif "pageNumber" not in date_chk['href'] and "statusdetail?encodedDate" in date_chk['href']:  pending_status_list.append(date_chk['href'])
			elif "pageNumber" in date_chk['href']: pending_status_temp.append(date_chk['href'])
			else: pass
		else: pass
	last_page_picker = []
	for each in pending_status_temp:
		last_page_picker.append(int(each.split("=")[2].strip('&encodeDate')))
	if len(pending_status_temp) == 0: pass
	else: last_page = max(last_page_picker)
	for i in range(last_page):
		try: pending_date_breaker = pending_status_temp[1].split("&")
		except: pass
		if len(pending_date_breaker) < 2 or i == 0: pass
		else:
			fixer = str(pending_date_breaker[1])
			fixer = fixer.split("=")
			fixer[1] = str(i + 1)
			fixed = "=".join(fixer)
			pending_date_breaker[1] = fixed
			pending_status_list.append("&".join(pending_date_breaker))


#Iterate over found pages and parse hit's to a dict
parsed_dict = {}
parsed_num = 1
for parse_page in pending_status_list:
	print "Parsing " + str(parsed_num) + "... out of " + str(len(pending_status_list))
	parsed_num += 1 
	parsing = "https://mturk.com" + parse_page
	hitdate = parse_page[-8:]
	hmonth = hitdate[:-6]
	hday = hitdate[2:-4]
	hyear = hitdate[4:]
	hitdate = [hyear,hmonth,hday]
	hitdate = "-".join(hitdate)
        parse_soup = br.open(parsing)
        parse_soup = parse_soup.read()
	parse_soup = BeautifulSoup(parse_soup)	
	parse_odd = parse_soup.find_all('tr','odd')
	parse_even = parse_soup.find_all('tr','even')
	for unparsed in parse_odd:
		unparsed = str(unparsed)
		unparsed = BeautifulSoup(unparsed)
                req_and_hitid = unparsed.find_all(href=True)
                req_and_hitid = str(req_and_hitid[0]).split('=')
                hitid = req_and_hitid[2].strip('Regarding+Amazon+Mechanical+Turk+HIT+')
                hitid = hitid.strip('&amp;requesterId').encode("utf-8")
		if len(hitid) < 30: hitid = (hitid + "I").encode("utf-8")
                reqid = req_and_hitid[3].strip('&amp;requesterName').encode("utf-8")
		reqname = unparsed.find_all(text=True)[2].strip().encode("utf-8")
		title = unparsed.find_all(text=True)[5].strip().encode("utf-8")
		reward = unparsed.find_all(text=True)[7].strip('$').encode("utf-8")
		status = unparsed.find_all(text=True)[9].strip().encode("utf-8")
		if "Payment" in status: status = "Approved - Pending Payment"
		feedback = unparsed.find_all(text=True)[11].strip().encode("utf-8")
		parsed_dict[hitid] = [hitid,hitdate,reqname,reqid,title,reward,status,feedback,worker_ID]
        for unparsed in parse_even:
                unparsed = str(unparsed)
                unparsed = BeautifulSoup(unparsed)
                req_and_hitid = unparsed.find_all(href=True)
                req_and_hitid = str(req_and_hitid[0]).split('=')
                hitid = req_and_hitid[2].strip('Regarding+Amazon+Mechanical+Turk+HIT+')
                hitid = hitid.strip('&amp;requesterId').encode("utf-8")
                if len(hitid) < 30: hitid = (hitid + "I").encode("utf-8")
                reqid = req_and_hitid[3].strip('&amp;requesterName').encode("utf-8")
                reqname = unparsed.find_all(text=True)[2].strip().encode("utf-8")
                title = unparsed.find_all(text=True)[5].strip().encode("utf-8")
                reward = unparsed.find_all(text=True)[7].strip('$').encode("utf-8")
                status = unparsed.find_all(text=True)[9].strip().encode("utf-8")
		if "Payment" in status: status = "Approved - Pending Payment"
                feedback = unparsed.find_all(text=True)[11].strip().encode("utf-8")
                parsed_dict[hitid] = [hitid,hitdate,reqname,reqid,title,reward,status,feedback,worker_ID]

#Preparing SQL for insertion and commit to database
for key,value in parsed_dict.iteritems():
	replace_statement = "REPLACE INTO mturk.hitdb(hitId, date, requesterName, requesterId, title, reward, status, feedback, workerId) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
	cur.execute(replace_statement, [value[0],value[1],value[2],value[3],value[4],value[5],value[6],value[7],value[8]])
db.commit()
