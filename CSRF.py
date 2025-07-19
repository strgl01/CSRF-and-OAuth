import requests
from bs4 import BeautifulSoup as bs

s = requests.session()
res = s.get('https://quotes.toscrape.com/login')
soup = bs(res.text, 'lxml')
csrf = soup.find('input', attrs={'name' : 'csrf_token'})['value']
print(csrf)
payload = {'username' : 'username',
           'password' : 'password',
           'csrf_token' : csrf}
res2 = s.post('https://quotes.toscrape.com/login', data = payload)
if "Top Ten tags" in res2.text:
    print("✅ Login successful!")
else:
    print("❌ Login failed.")