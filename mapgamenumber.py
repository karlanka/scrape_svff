import os

def gamenumber():
    path = "matchnummer files/"

    comp_dict = {}

    for root, dirs, filenames in os.walk(path):
        for f in filenames:
            season = open(path+f, 'r')

            numbers = season.read().splitlines()

            for number in numbers:
                competition = f[:-5]
                gameid = f[-4:]+number

                comp_dict[gameid] = competition

    return comp_dict


