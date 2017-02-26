from bs4 import BeautifulSoup
import requests
import os
import re

def get_all_url():
    indoor_url = 'http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000'
    r = requests.get(indoor_url)
    data = r.text

    soup = BeautifulSoup(data, 'lxml')
    myul = soup.select('ul[style="margin-right:-15px;"]')[0]
    pattern = re.compile('<a href="(.*?)">')
    all_url = re.findall(pattern, str(myul))

    base_url = 'http://www.liaoxuefeng.com'
    for url in all_url:
        url = base_url + url
        yield url

def get_each_url_content(url):
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'lxml')
    mydiv = soup.select('div[class="x-content"]')[0]
    content = []
    for child in mydiv.descendants:
        mycontent = str(child.string)
        content.append(mycontent)
    mycontent = []
    for c in content:
        if c not in mycontent:
            mycontent.append(c)
    mycontent = '\n'.join(mycontent)
    return mycontent


def main():
    os.chdir(r'C:\Users\asus\Desktop')
    if not os.path.exists(r'C:\Users\asus\Desktop\廖雪峰'): os.mkdir('廖雪峰')
    os.chdir(r'C:\Users\asus\Desktop\廖雪峰')

    count = 0
    for url in get_all_url():
        each_content = get_each_url_content(url)
        with open(str(count), 'w') as file:
            file.write(each_content)
        count += 1

if __name__ == '__main__':
    main()
