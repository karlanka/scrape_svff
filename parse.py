# -*- coding: utf-8 -*-
import mysql.connector
import xml.etree.ElementTree as ET
import os

def parse_games(xmlroot, year, cursor, cnx, comp_dict):
    for game in xmlroot.iter('game'):
        gid = year + game.get('id')
        _date = game.get('date')

    try:
        comp = comp_dict[gid]
    except:
        comp = "unknown"


    for created in xmlroot.iter('game-info'):
        game_created = created.get('created')

        supplier = created.get('supplier')

    for team in xmlroot.iter('team'):
        teams = team.get('short-name')
        team_long = team.get('long-name')
        h_or_a = team.get('home-team')
        teamid = team.get('id')

        if h_or_a == 'True':
            home_team = teams
            homeid = teamid
            home_team_long = team_long

        if h_or_a == 'False':
            away_team = teams
            awayid = teamid
            away_team_long = team_long

    for score in xmlroot.iter('score'):
        home_scoreFT = score.get('home-team')
        away_scoreFT = score.get('away-team')
        home_scoreHT = score.get('home-team-half-time')
        away_scoreHT = score.get('away-team-half-time')


    sql_add_data = ("""INSERT IGNORE INTO games
            (GameID, Competition, Supplier, Date, Created, HomeTeam, home_team_long, HomeTeamID, AwayTeam, away_team_long, AwayTeamID, HomeTeamFT, AwayTeamFT, HomeTeamHT, AwayTeamHT)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")

    data_arg = (gid, comp, supplier, _date, game_created, home_team, home_team_long, homeid, away_team, away_team_long, awayid, home_scoreFT, away_scoreFT, home_scoreHT, away_scoreHT)

    cursor.execute(sql_add_data, data_arg)

    cnx.commit()

def parse_players(xmlroot, cursor, cnx):

    for event in xmlroot.iter('event'):

        for part in event.iter('participant'):
            first_name = part.get('given-name')
            surname = part.get('surname')
            _id = part.get('id')
            fogis_id = part.get('fogis-id')

            sql_add_data = ("""INSERT IGNORE INTO players
            (First_Name, Surname, FogisID, SiteID)
            VALUES (%s, %s, %s, %s)""")

            data_arg = (first_name, surname, fogis_id, _id)

            cursor.execute(sql_add_data, data_arg)

            cnx.commit()


def parse_events(xmlroot, year, cursor, cnx, comp_dict):

    supplier = None

    for game in xmlroot.iter('game'):
        gid = year + game.get('id')
        _date = game.get('date')

    try:
        comp = comp_dict[gid]
    except:
        comp = "unknown"

    for created in xmlroot.iter('game-info'):
        game_created = created.get('created')

        if _date == None:
            _date = game_created

        supplier = created.get('supplier')

    for team in xmlroot.iter('team'):
        teams = team.get('short-name')
        h_or_a = team.get('home-team')
        teamid = team.get('id')

        if h_or_a == 'True':
            home_team = teams
            homeid = teamid

        if h_or_a == 'False':
            away_team = teams
            awayid = teamid

    for event in xmlroot.iter('event'):

        away_score = None
        home_score = None
        event_id = None
        _type = None
        type_desc = None
        gametime = None
        xpos = None
        ypos = None
        home = None
        goal = None
        phase = None
        hot = None
        event_id = None
        _id = None
        fogis_id = None
        part_type_desc = None
        subbed_in = None
        subbed_out = None
        fk_for = None
        fk_against = None
        scorer = None
        assister = None
        pen_against = None
        pen_for = None
        yellow_card = None
        red_card = None
        player_offside = None
        finisher = None
        penalty_miss = None
        pen_miss_type = None


        away_score = event.get('away-score')
        home_score = event.get('home-score')
        event_id = event.get('id')
        event_id += gid
        _type = event.get('type')
        type_desc = event.get('type-desc')
        #_date = event.get('date')
        gametime = event.get('game-time')
        xpos = event.get('x-position')
        ypos = event.get('y-position')
        home = event.get('home-team')
        goal = event.get('goal-type-desc')
        phase = event.get('phase')

        if home == "True":
            hot = "home"
        elif home == "False":
            hot = "away"
        else:
            hot = None

        if hot == "home":
            team = home_team
            event_team_id = homeid
        else:
            team = away_team
            event_team_id = awayid


        for part in event.iter('participant'):
            _id = part.get('id')
            fogis_id = part.get('fogis-id')
            part_type_desc = part.get('type-desc')
            part_type = part.get('type')

            if type_desc.startswith("Pen") and part_type == "P" or part_type == "S" or part_type.startswith("Sh"): #aString.startswith("hello")
                penalty_miss = fogis_id
                pen_miss_type = part_type_desc

            if part_type_desc == "Substitutes in":
                subbed_in = fogis_id
            if part_type_desc == "Substitutes out":
                subbed_out = fogis_id

            if part_type_desc == "Freekick for":
                fk_for = fogis_id
            if part_type_desc == "Freekick against":
                fk_against = fogis_id

            if part_type_desc == "Scorer":
                scorer = fogis_id
            if part_type_desc == "Assister":
                assister = fogis_id

            if part_type_desc == "Penalty against":
                pen_against = fogis_id
            if part_type_desc == "Penalty for":
                pen_for = fogis_id

            if part_type_desc == "Yellow card":
                yellow_card = fogis_id
            if part_type_desc == "Red card":
                red_card = fogis_id

            if part_type_desc == "Offside":
                player_offside = fogis_id

            if _type == "F":
                finisher = fogis_id

        sql_add_data = ("""INSERT IGNORE INTO events
                (Supplier, Competition, GameID, EventID, Date, Team, TeamID, Type_, TypeDesc, GameTime, AwayScore, HomeScore, Phase, Xpos, Ypos, GoalType, HomeTeam, EventPartID, PartTypeDesc, Finisher, Subbed_in, Subbed_out, FK_for, FK_against, Scorer, Assister, Pen_against, Pen_for, Pen_finisher, Pen_miss, Yellow_card, Red_card, PlayerOffs)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")

        data_arg = (supplier, comp, gid, event_id, _date, team, event_team_id, _type, type_desc, gametime, away_score, home_score, phase, xpos, ypos, goal, hot, _id, part_type_desc, finisher, subbed_in, subbed_out, fk_for, fk_against, scorer, assister, pen_against, pen_for, penalty_miss, pen_miss_type, yellow_card, red_card, player_offside)

        cursor.execute(sql_add_data, data_arg)

        cnx.commit()