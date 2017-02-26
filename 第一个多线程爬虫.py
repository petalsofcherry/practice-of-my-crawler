# -*- coding:utf-8 -*-
import threading
from bs4 import BeautifulSoup
from queue import Queue
import requests

class myThread(threading.Thread):
    def __init__(self, base_url, q):
        super(myThread, self).__init__()
        self.base_url = base_url
        self.q = q

    def run(self):
        while not exitFlag:
            queueLock.acquire()
            if not workQueue.empty():
                mypage = self.q.get()
                url = self.base_url + str(mypage)
                r = s.get(url)
                soup = BeautifulSoup(r.text, 'lxml')
                pos_list = soup.find_all('td', title='password_pos')
                password_list = soup.find_all('td', title='password_val')
                for i in range(len(pos_list)):
                    pos = int(pos_list[i].string)
                    num = str(password_list[i].string)
                    if password[pos-1] == 'x':
                        password[pos-1] = num
            else:
                queueLock.release()

def get_password(login_url, base_url):
    global s
    s = requests.session()
    s.get(login_url)
    token = s.cookies['csrftoken']
    myparams = {
        'username': 'petals',
        'password': '1579789801l',
        'csrfmiddlewaretoken': token
    }
    s.post(login_url, data=myparams)

    pages = range(1, 14)
    global queueLock
    queueLock = threading.Lock()
    global workQueue
    workQueue = Queue(13)
    global password
    password = ['x' for i in range(100)]
    threads = []
    global exitFlag
    exitFlag = 0

    for page in pages:
        thread = myThread(base_url, workQueue)
        thread.start()
        threads.append(thread)

    queueLock.acquire()
    for page in pages:
        workQueue.put(page)
    queueLock.release()

    while 'x' in password:
        pass

    exitFlag = 1

    for t in threads:
        t.join()

    password = ''.join(password)
    print(password)

if __name__ == '__main__':
    login_url = 'http://www.heibanke.com/accounts/login'
    base_url = 'http://www.heibanke.com/lesson/crawler_ex03/pw_list/?page='
    get_password(login_url, base_url)