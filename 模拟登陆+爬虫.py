# coding=utf-8
import requests
from bs4 import BeautifulSoup
import random

def get_password(login_url, base_url, headers):
    s = requests.session()
    s.get(login_url)
    token = s.cookies['csrftoken']
    myparams = {
        'username': 'petals',
        'password': '1579789801l',
        'csrfmiddlewaretoken': token
    }
    s.post(login_url, data=myparams, headers=headers)
    password = ['x' for i in range(100)]
    count = 0
    while count < 100:
        url = base_url + str(random.choice(list(range(1, 14))))
        r = s.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        pos_list = soup.find_all('td', title='password_pos')
        password_list = soup.find_all('td', title='password_val')
        for i in range(len(pos_list)):
            pos = int(pos_list[i].string)
            num = str(password_list[i].string)
            if password[pos-1] == 'x':
                password[pos-1] = num
                count += 1

    return ''.join(password)



if __name__ == '__main__':
    login_url = 'http://www.heibanke.com/accounts/login'
    base_url = 'http://www.heibanke.com/lesson/crawler_ex03/pw_list/?page='
    headers = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 56.0.2924.87 Safari / 537.36'
    }
    print(get_password(login_url, base_url, headers))


