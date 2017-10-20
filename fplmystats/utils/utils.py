import urllib.request
import datetime
import sqlite3
import json

static_url = 'https://fantasy.premierleague.com/drf/bootstrap-static'
fixtures_url = 'https://fantasy.premierleague.com/drf/fixtures'

with open('/home/admin/fplmystats/fplmystats/utils/current_season.txt') as file:
# with open('C:\\Users\\seanh\\PycharmProjects\\fplmystats\\fplmystats\\utils\\current_season.txt') as file:
    for x in file:
        current_season = x

data_file = '/home/admin/fplmystats/FPLdb.sqlite'
# data_file = 'FPLdb.sqlite'

fixtures_file = '/home/admin/fplmystats/fplmystats/utils/fixtures.txt'
# fixtures_file = 'C:\\Users\\seanh\\PycharmProjects\\fplmystats\\fplmystats\\utils\\fixtures.txt'

field_type_INT = 'INTEGER'
field_type_TEXT = 'TEXT'

HOURS = 4  # number of hours since kickoff to still update table


def player_to_string(player_id):
    """
    Returns a string containing player's name, team and position
    """
    conn = sqlite3.connect(data_file)
    c = conn.cursor()

    table_name = '{}playerIDs'.format(str(current_season))
    c.execute('SELECT * FROM "{}" WHERE id = {}'.format(table_name, player_id))
    player = c.fetchone()

    if player[1] == player[3]:
        player_name = player[2] + ' ' + player[3]
    else:
        player_name = player[1]

    position = player[4]
    if position == 0:
        position_string = "GK"
    elif position == 1:
        position_string = "DEF"
    elif position == 2:
        position_string = "MID"
    else:
        position_string = "FWD"

    team_id = player[5]
    table_name = '{}teamIDs'.format(str(current_season))
    c.execute('SELECT name FROM "{}" WHERE id = {}'.format(table_name, team_id))
    team_string = c.fetchone()[0]

    conn.close()
    return "NAME: {}; TEAM: {}; POSITION: {}\n".format(player_name, team_string, position_string)


def create_season_tables():
    """
    Create table which maps team IDs to team names, run once at start of season
    Create table containing the names of every player, their ID number, position & team ID
    Run once at start of season, separate function for updating player table regularly
    """
    conn = sqlite3.connect(data_file)
    c = conn.cursor()

    with urllib.request.urlopen('{}'.format(static_url)) as url:
        data = json.loads(url.read().decode())

    # team ID table
    table_name = '{}teamIDs'.format(str(current_season))
    id_field = 'id'
    name_field = 'name'

    c.execute('CREATE TABLE "{tn}" ({idf} {fti} PRIMARY KEY, {nf} {ftt})'
              .format(tn=table_name, idf=id_field, nf=name_field, fti=field_type_INT, ftt=field_type_TEXT))

    for team in data['teams']:
        team_id = team['id']
        name = team['name']

        c.execute('INSERT INTO "{tn}" VALUES ({idv}, "{nv}")'.format(tn=table_name, idv=team_id, nv=name))

    # player ID table
    table_name = '{}playerIDs'.format(str(current_season))
    id_field = 'id'
    web_name_field = 'webname'
    first_name_field = 'firstname'
    second_name_field = 'secondname'
    position_field = 'position'
    team_id_field = 'teamID'

    c.execute('CREATE TABLE "{tn}" ({idf} {fti} PRIMARY KEY,\
                {wnf} {ftt}, {fnf} {ftt}, {snf} {ftt}, {psf} {fti}, {tmf} {fti})'
              .format(tn=table_name,
                      idf=id_field,
                      wnf=web_name_field,
                      fnf=first_name_field,
                      snf=second_name_field,
                      psf=position_field,
                      tmf=team_id_field,
                      fti=field_type_INT,
                      ftt=field_type_TEXT))
    conn.commit()
    conn.close()


def update_player_id_table():
    """
    Update the player ID table to include new players that have been added in to the game.
    Saves any changes to the database to a daily log file
    To be run once a day automatically.
    """
    conn = sqlite3.connect(data_file)
    c = conn.cursor()

    table_name = '{}playerIDs'.format(str(current_season))
    c.execute('SELECT id FROM "{}"'.format(table_name))
    c.execute('DELETE FROM "{}"'.format(table_name))

    with urllib.request.urlopen('{}'.format(static_url)) as url:
        data = json.loads(url.read().decode())

    for element in data['elements']:
        player_id = element['id']
        web_name = element['web_name'].replace("'", "''")
        first_name = element['first_name'].replace("'", "''")
        second_name = element['second_name'].replace("'", "''")
        position = element['element_type']
        team_id = element['team']

        c.execute('INSERT INTO "{tn}" VALUES ({idv}, "{wnv}", "{fnv}", "{snv}", {psv}, {tmv})'
                  .format(tn=table_name,
                          idv=player_id,
                          wnv=web_name,
                          fnv=first_name,
                          snv=second_name,
                          psv=position,
                          tmv=team_id))

    c.execute('SELECT id FROM "{}"'.format(table_name))

    conn.commit()
    conn.close()


def create_weekly_tables():
    """
    Create the weekly table for every week in the season to hold data from every player for that week
    Run once at start of season, separate function for updating tables regularly
    """
    conn = sqlite3.connect(data_file)
    c = conn.cursor()
    week = 1    # always starts at 1

    while week <= 38:
        table_name = '{}week{}'.format(str(current_season), str(week))
        fields = ['id', 'points', 'minutes', 'goals', 'assists', 'cleansheets', 'saves',
                  'goalsconceded', 'pensaves', 'yellows', 'reds', 'penmisses', 'owngoals', 'bonus', 'price']

        c.execute('CREATE TABLE "{tn}" ({} {ft} PRIMARY KEY, {} {ft}, {} {ft}, {} {ft}, {} {ft},'
                  '{} {ft}, {} {ft}, {} {ft}, {} {ft}, {} {ft}, {} {ft},{} {ft}, {} {ft}, {} {ft}, {} {ft})'
                  .format(tn=table_name, ft=field_type_INT, *fields))
        week += 1
    conn.commit()
    conn.close()


def update_weekly_table():
    """
    Populate the weekly data table with the latest data for that week
    To be run automatically multiple times per day where there is a game
    """
    with urllib.request.urlopen('{}'.format(static_url)) as static_json:
        static_data = json.loads(static_json.read().decode())
    current_week = 0
    for entry in static_data['events']:
        if entry['is_current']:
            current_week = entry['id']

    conn = sqlite3.connect(data_file)
    c = conn.cursor()
    weekly_table_name = '{}week{}'.format(str(current_season), str(current_week))
    c.execute('DELETE FROM "{}"'.format(weekly_table_name))

    player_table_name = '{}playerIDs'.format(str(current_season))
    c.execute('SELECT * from "{}"'.format(player_table_name))

    players = c.fetchall()
    for player in players:
        player_id = player[0]
        player_url = "https://fantasy.premierleague.com/drf/element-summary/{}".format(str(player_id))

        with urllib.request.urlopen('{}'.format(player_url)) as url:
            data = json.loads(url.read().decode())

        results = [0] * 15
        results[0] = player_id
        previous_price = 0.0
        for event in data['history']:
            if event['round'] == current_week:
                results[1] += event['total_points']
                results[2] += event['minutes']
                results[3] += event['goals_scored']
                results[4] += event['assists']
                results[5] += event['clean_sheets']
                results[6] += event['saves']
                results[7] += event['goals_conceded']
                results[8] += event['penalties_saved']
                results[9] += event['yellow_cards']
                results[10] += event['red_cards']
                results[11] += event['penalties_missed']
                results[12] += event['own_goals']
                results[13] += event['bonus']
                results[14] = event['value'] / 10.0

                # for some reason not all players are updated in time for the new gameweek
                # using this as a contingency prevents div by zero errors
                if results[14] == 0:
                    results = previous_price
                else:
                    previous_price = results

        c.execute('INSERT INTO "{tn}" VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'
                  .format(tn=weekly_table_name, *results))

    conn.commit()
    conn.close()


def create_manager_id_table():
    """
    Create a seasonal table to hold the manager IDs and corresponding manager and team names
    Run once at start of season, tables are updated as managers search for their ID
    """
    conn = sqlite3.connect(data_file)
    c = conn.cursor()

    table_name = '{}managerIDs'.format(str(current_season))
    fields = ['id', 'name', 'team']

    c.execute('CREATE TABLE "{tn}" ({} {fti} PRIMARY KEY , {} {ftt}, {} {ftt})'
              .format(tn=table_name,
                      fti=field_type_INT,
                      ftt=field_type_TEXT,
                      *fields))
    conn.commit()
    conn.close()


def create_manager_tables():
    """
    Create weekly tables that hold the necessary data for managers
    Run once at start of season, tables are updated as managers search for their ID
    """
    conn = sqlite3.connect(data_file)
    c = conn.cursor()
    week = 1    # always starts at 1

    while week <= 38:
        table_name = '{}manager{}'.format(str(current_season), str(week))
        fields = ['id', 'complete', 'pos1', 'mul1', 'pos2', 'mul2', 'pos3', 'mul3', 'pos4', 'mul4', 'pos5', 'mul5', 'pos6', 'mul6',
                  'pos7', 'mul7', 'pos8', 'mul8', 'pos9', 'mul9', 'pos10', 'mul10', 'pos11', 'mul11', 'pos12', 'mul12',
                  'pos13', 'mul13', 'pos14', 'mul14', 'pos15', 'mul15']

        c.execute('CREATE TABLE "{tn}" ({} {ft} PRIMARY KEY, {} {ft}, {} {ft}, {} {ft}, {} {ft}, {} {ft}, {} {ft},'
                  '{} {ft},' '{} {ft}, {} {ft}, {} {ft}, {} {ft}, {} {ft}, {} {ft},{} {ft}, {} {ft}, {} {ft}, {} {ft},'
                  '{} {ft},' '{} {ft}, {} {ft}, {} {ft}, {} {ft}, {} {ft}, {} {ft}, {} {ft}, {} {ft}, {} {ft}, {} {ft},'
                  '{} {ft},' '{} {ft}, {} {ft}, {c} {ft}, {vc} {ft}, {p} {ft}, {r} {ft}, {t} {ft}, {v} {ft},'
                  '{ch} {ftt})'
                  .format(tn=table_name, ft=field_type_INT, ftt=field_type_TEXT, *fields,
                          c='captain',
                          vc='vicecaptain',
                          p='points',
                          r='rank',
                          t='transfercost',
                          v='value',
                          ch='chip'))
        week += 1
    conn.commit()
    conn.close()


def get_all_fixtures():
    """
    Saves a list of every unique kickoff time in the year to a file
    To be run every day since fixtures change over the season
    """
    with urllib.request.urlopen('{}'.format(fixtures_url)) as url:
        data = json.loads(url.read().decode())

    fixtures_list = []

    for item in data:
        kickoff_time = item['kickoff_time'][0:10] + '-' + item['kickoff_time_formatted'][-5:]
        if kickoff_time not in fixtures_list:
            fixtures_list.append(kickoff_time)

    with open(fixtures_file, 'r+') as fixtures:
        fixtures.truncate()
        for item in fixtures_list:
            fixtures.write(item + '\n')


def check_for_fixture():
    """
    Updates the weekly table if there is a kickoff within the last 4 hours
    Run automatically every 15 minutes
    """

    today = datetime.date.today()
    now = datetime.datetime.now()
    with open(fixtures_file, 'r') as fixtures:
        for item in fixtures:
            year = int(item[0:4])
            month = int(item[5:7])
            day = int(item[8:10])
            hour = int(item[11:13])
            minute = int(item[14:16])

            kickoff_date = datetime.date(year, month, day)
            if kickoff_date == today:
                kickoff_time = datetime.datetime(year, month, day, hour, minute)
                if now > kickoff_time and (now - kickoff_time < datetime.timedelta(hours=HOURS)):
                    update_weekly_table()
                    return


def count_database_ids():
    conn = sqlite3.connect(data_file)
    c = conn.cursor()

    table_name = "{}managerIDs".format(current_season)
    c.execute('SELECT id from "{}"'.format(table_name))
    results = c.fetchall()
    print(len(results))

    conn.close()
