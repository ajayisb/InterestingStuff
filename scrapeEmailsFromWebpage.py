import urllib,re
link="https://www.university.youth4work.com/lnct_lakshmi-narain-college-of-technology"
sites = [link]
for site in sites:
	f = urllib.request.urlopen(site)
	s = f.read().decode('utf-8')
	emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",s)
	print(emails)