# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import StringIO
import gzip
import mysql.connector
import datetime


def date_list():
    pw = 'anton'
    host_name = 'localhost'

    cnx = mysql.connector.connect(user='root', password=pw, host=host_name, database='SVFF')
    cursor = cnx.cursor(buffered=True)

    cursor.execute("SELECT Date FROM games where Date is not null")

    most_recent_post = max(cursor.fetchall())

    latest = (most_recent_post[0]).strftime('%Y-%m-%d')

    cnx.commit()
    cursor.close()
    cnx.close()

    list_of_dates = []
    i = 1

    while True:
        day = (datetime.date.today() - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        i += 1
        if day == latest:
            return list_of_dates
        list_of_dates.append(day)


def get_game_id():

    dates = date_list()

    for date in dates:
        wd = webdriver.Chrome("/Users/antonkarling/Downloads/Chromedriver")
        url = "http://svenskfotboll.se/livescore/#?date="+date
        wd.get(url)

        try:
            WebDriverWait(wd, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "game-overview")))
        except:
            wd.quit()
            continue

        html_page = wd.page_source
        wd.quit()

        soup = BeautifulSoup(html_page, "html.parser")

        for link in soup.findAll('a',class_="cf"):
            game_url = str(link.get('href'))
            game_id = (game_url.split("="))[2]
            year = (game_url.split("="))[1][:4]
            name = year+"-"+game_id


            request = urllib2.Request("http://c03.fogis.se/fogistemplates.se/livescore/xml/game-info-"+game_id+".xml?year="+year+"&token=")
            request.add_header('Accept-encoding', 'gzip')
            response = urllib2.urlopen(request)

            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO.StringIO(response.read())
                f = gzip.GzipFile(fileobj=buf)
                content = f.read()
            else:
                content = response.read()

            wf = open('gamexml/'+name+'.xml', 'w')

            soup = BeautifulSoup(content, "html.parser")
            wf.write(soup.encode('utf-8'))
            wf.close()

    wd.quit()

#if __name__ == '__main__':
 #   main()