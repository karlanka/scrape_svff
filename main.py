# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import mysql.connector

from parse import parse_games, parse_players, parse_events
from mapgamenumber import gamenumber
from getgameid import get_game_id


def main():

    pw = 'anton'
    host_name = '127.0.0.1'

    source = 'gamexml/'
    cnx = mysql.connector.connect(user='root', password=pw, host=host_name, database='SVFF')
    cursor = cnx.cursor(buffered=True)
    game_id_list = []

    cursor.execute("SELECT GameID FROM games")

    for row in cursor.fetchall():
         game_id_list.append(row[0])

    comp_dict = gamenumber()

    #print game_id_list
    #exit()

    for root, dirs, filenames in os.walk(source):
        for f in filenames:
            year = f.split('-')[0]
            game_id = year + f[5:-4]

            if game_id not in game_id_list:
                print game_id
                try:
                    tree = ET.parse(source+f)

                except:
                    continue

                xmlroot = tree.getroot()
                parse_events(xmlroot, year, cursor, cnx, comp_dict)
                parse_games(xmlroot, year, cursor, cnx, comp_dict)
                parse_players(xmlroot, cursor, cnx)


    cursor.close()
    cnx.close()


if __name__ == '__main__':
    get_game_id()
    main()