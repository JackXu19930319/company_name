import requests
from faker import Faker

fake = Faker()
url = 'https://www.google.com/search?q=%E6%98%93%E5%8B%9D&oq=%E6%98%93%E5%8B%9D&ie=UTF-8'
headers = {
    'User-Agent': fake.user_agent()
}
page = requests.get(url, headers=headers)
print(page.text)
