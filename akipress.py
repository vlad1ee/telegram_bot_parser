import requests
from bs4 import BeautifulSoup

def get_html(url):
    r = requests.get(url)
    return r.text

def get_data(html):
    soup =  BeautifulSoup(html, 'lxml')
    titles = soup.find('ul', class_='topic_list view_lenta').find_all('li', limit=20)
    list1 = []
    for i in titles:
        list1.append(i.find('span', class_='n').text)
    return list1

def news_info(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        photo = soup.find('div', class_='i').find('a').get('href')
    except:
        photo = 'фото отсутствует'
    try:
        description = soup.find('div', class_="topic-text").text
    except:
        description = 'описание отсутствует'
    
    return {'Photo': photo, 'Description': description}

def get_info(html):
    soup = BeautifulSoup(html, 'lxml')
    new = soup.find('ul', class_= 'topic_list view_lenta').find_all('div', class_="t f_medium", limit = 20)
    list1 = []
    for i in new:
        list1.append(i.find('a').get('href'))
    return list1 

def main():
    url = 'https://kaktus.media/?date=2020-05-26&lable=8&order=main'
    list_news = get_data(get_html(url))
    list1 = get_info(get_html(url))
    list3 = []
    list_info = ['0']
    for i in list1:
        list_info.append(news_info(get_html(i)))
    for count, item in enumerate(list_news, 1):
        list3.append((f'{count}.{item}'))
    string1 = '\n'.join(list3)
    return string1, list_info
    
if __name__ == '__main__':
    main()