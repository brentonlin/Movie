from mysql.connector.errors import _ERROR_EXCEPTIONS
import requests
import mysql.connector
from lxml import etree




cnx = mysql.connector.connect(user='root', password='A1234567BB', host='127.0.0.1', database='movie')
cursor = cnx.cursor()
sql = "insert into table1(name, number, article, link, satisfaction) values(%s, %s, %s, %s, %s)"


response = requests.get("https://movies.yahoo.com.tw/movie_thisweek.html")
content = response.content.decode()
html = etree.HTML(content)

li_list = html.xpath('//*[@id="content_l"]/div[2]/ul/li ')

for li_data in li_list:    
    moviename = li_data.xpath("div[2]/div[1]/div[1]/a/text()")[0]
    try:
        percent1 = li_data.xpath("div[2]/div[1]/div[1]/dl/dt/div[2]/span/text()")[0]
    except Exception as e:
        percent1 = ('No value')
    try:
        percent2 = li_data.xpath('div[2]/div[1]/div[1]/dl/dd/div[2]/span')[0]
        num = dict(getattr(percent2, 'attrib'))['data-num']
    except Exception as e:
        num = ('No value')   
    address = li_data.xpath("div[2]/div[1]/div[1]/div/a")[0]  
    add = dict(getattr(address, 'attrib'))['href']
    response2 = requests.get(add)
    content2 = response2.content.decode()
    html2 = etree.HTML(content2)
    art = html2.xpath('//*[@id="story"]/text()')
    art = ', '.join(art)


    cursor.execute(sql, (moviename.strip(), percent1.strip(), art.strip(), add, num.strip()))


    
cnx.commit()

cursor.close()
cnx.close()

