import requests
from bs4 import BeautifulSoup
#from lxml.html import fromstring

URL = 'https://www.reddit.com/r/Python/'
MIN_COMM = 5

def get_html_from_url(url):
	headers = { 'User-Agent': 
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36' 
	}
	r = requests.get(url, headers = headers)
	list_html = r.text.encode('utf-8')
	return list_html


def choose_comments(l_html, min_comm):
	soup = BeautifulSoup(l_html, 'lxml')
	things = soup.find_all('div', {'class': 'thing'})
	for thing in things:
		comm_number = thing.get('data-comments-count')
		comm_link = 'https://www.reddit.com' + thing.get('data-permalink')
		if int(comm_number) >= min_comm:
			thread =  get_html_from_url(comm_link)
			print(comm_number + '\n')
			parse_comments(thread)

def parse_comments(l_html):
	soup = BeautifulSoup(l_html, 'lxml')
	entries = soup.find_all('div', {'class': 'entry unvoted'}) 
	for entry in entries:
		author = entry.find('a', {'class': 'author'})
		if author:
			author = author.text
			whole_comm = str(author) + ':'
			usercomms = entry.find('div', {'class': 'md'})
			if usercomms:
				usercomms = usercomms.find_all('p')
			
				for comm in usercomms:
					whole_comm += comm.text
		print(whole_comm)

def find_next_page_url(l_html):
	soup = BeautifulSoup(l_html, 'lxml')
	next_page = soup.find('span',{'class': 'next-button'})
	if next_page:
		next_page_url = next_page.find('a').get('href')
		return next_page_url
	return None


if __name__ == '__main__':
    l_html = get_html_from_url(URL)
    choose_comments(l_html, MIN_COMM)
    next_page = find_next_page_url(l_html)
    while next_page:
    	l_html = get_html_from_url(next_page)
    	choose_comments(l_html, MIN_COMM)
    	next_page = find_next_page_url(l_html)
    	print(next_page)
    
    #l = get_html_from_url('https://www.reddit.com/r/Python/comments/7xdi5r/is_sysexit_bad_practice/')
    #parse_comments(l)
