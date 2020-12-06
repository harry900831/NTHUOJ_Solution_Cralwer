from requests_html import HTMLSession
import getpass
import os
import json
import codecs
from bs4 import BeautifulSoup



url = 'https://acm.cs.nthu.edu.tw/users/login/'
username = input('username: ')
password = getpass.getpass('password: ')
session = HTMLSession()
r = session.get(url)

payload = {
	'username': username,
	'password': password,
	'csrfmiddlewaretoken': session.cookies['csrftoken']
}

headers = {
	'Referer': url,
}

res = session.post(url, headers=headers, data=payload)

if res.status_code == 200:
	print('Login successfully')


contest_id = input("input contest id: ")
page_count = int(input("input page count: "))

try:
	os.mkdir('code')
except FileExistsError:
	pass

	
def getcode(sid):
	response = session.get('https://acm.cs.nthu.edu.tw/status/view_code/' + sid)
	response.html.render()
	soup = BeautifulSoup(response.text, "html.parser")
	code = soup.find('textarea').text.replace('\\r\\n', '\n')
	return code


for pid in range(1, page_count + 1):
	print('Crawling page ' + str(pid) + '...')
	response = session.get('https://acm.cs.nthu.edu.tw/status/?username=&status=&pid=&page=' + str(pid) + '&cid=' + contest_id)

	soup = BeautifulSoup(response.text, "html.parser")
	result = soup.find_all('tr', {'class' : 'success'})
	for res in result:
		sub = res.find_all('td')
		sub_id = sub[0].text.strip()
		sub_user = sub[2].text.strip()
		code = getcode(sub_id)
		with open('code/' + sub_user + '_' + sub_id + '.c', 'w') as f :
			f.write(code)
	
