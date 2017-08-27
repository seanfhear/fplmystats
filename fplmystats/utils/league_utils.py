import urllib.request
import json
from collections import namedtuple
from fplmystats.utils import manager_utils

static_url = 'https://fantasy.premierleague.com/drf/bootstrap-static'
classic_league_info_url = 'https://fantasy.premierleague.com/drf/leagues-classic-standings/'
h2h_league_info_url = 'https://fantasy.premierleague.com/drf/leagues-h2h-standings/'

with urllib.request.urlopen('{}'.format(static_url)) as static_json:
    static_data = json.loads(static_json.read().decode())
current_week = 0
for entry in static_data['events']:
    if entry['is_current']:
        current_week = entry['id']


def get_league_name(league_id):
    """
    Return the name of the league
    """
    # TODO account for h2h leagues
    data_url = classic_league_info_url + str(league_id)
    with urllib.request.urlopen('{}'.format(data_url)) as url:
        data = json.loads(url.read().decode())

    return data['league']['name']


def get_stats(league_id):
    """
    Return the data for every table in the league view
    """
    table_data = namedtuple('table_data', ('headers', 'general_number_totals', 'general_number_max',
                                           'general_points_totals', 'general_points_max', 'positions_totals',
                                           'positions_max', 'team_selection_totals', 'team_selection_max'))
    manager_ids = []

    table_data.general_number_totals = []
    table_data.general_points_totals = []
    table_data.team_selection_totals = []

    table_data.general_number_max = []
    table_data.general_points_max = []

    table_data.headers = [0] * 6

    # max_number = [[0, '-']] * 12    doesn't work???
    max_number = [[0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'],
                  [0, '-'], [0, '-']]
    max_points = [[0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'],
                  [0, '-'], [0, '-']]
    #  0 - minutes
    #  1 - goals
    #  2 - assists
    #  3 - clean sheets
    #  4 - saves
    #  5 - goals conceded
    #  6 - penalties saved
    #  7 - yellow cards
    #  8 - red cards
    #  9 - penalties missed
    # 10 - own goals
    # 11 - bonus points

    have_leader = False

    data_url = classic_league_info_url + str(league_id)
    with urllib.request.urlopen('{}'.format(data_url)) as url:
        data = json.loads(url.read().decode())

    for entry in data['standings']['results']:
        manager_ids.append([entry['entry'], entry['player_name']])

    for manager_id in manager_ids:
        data = manager_utils.get_stats(manager_id[0])

        if not have_leader:
            table_data.headers[0] = manager_id[1]
            have_leader = True

        manager_general_number_totals = ([0] * 15)
        manager_general_number_totals[0] = manager_id[0]  # manager id
        manager_general_number_totals[1] = manager_id[1]  # manager name

        for i in range(2, 15):
            manager_general_number_totals[i] = data.general_number_totals[i - 2]
        table_data.general_number_totals.append(manager_general_number_totals)

        for i in range(12):
            if data.general_number_totals[i + 1] > max_number[i][0]:
                max_number[i][0] = data.general_number_totals[i + 1]
                max_number[i][1] = manager_id[1]

        manager_general_points_totals = ([0] * 15)
        manager_general_points_totals[0] = manager_id[0]  # manager id
        manager_general_points_totals[1] = manager_id[1]  # manager name

        for i in range(2, 15):
            manager_general_points_totals[i] = data.general_points_totals[i-2]
        table_data.general_points_totals.append(manager_general_points_totals)

        for i in range(12):
            if data.general_points_totals[i + 1] >= 0:
                if data.general_points_totals[i + 1] > max_points[i][0]:
                    max_points[i][0] = data.general_points_totals[i + 1]
                    max_points[i][1] = manager_id[1]
            else:  # if points are negative
                if data.general_points_totals[i + 1] < max_points[i][0]:
                    max_points[i][0] = data.general_points_totals[i + 1]
                    max_points[i][1] = manager_id[1]

        manager_team_selection_totals = ([0] * 12)
        manager_team_selection_totals[0] = manager_id[0]                   # manager id
        manager_team_selection_totals[1] = manager_id[1]                   # manager name
        manager_team_selection_totals[2] = data.headers[3]                 # preferred captain
        manager_team_selection_totals[3] = data.team_selection_totals[0]   # captain points
        manager_team_selection_totals[4] = data.headers[4]                 # season mvp
        manager_team_selection_totals[5] = data.headers[5]                 # mvp points
        manager_team_selection_totals[6] = data.team_selection_totals[2]   # captain points lost
        manager_team_selection_totals[7] = data.team_selection_totals[3]   # points on bench
        manager_team_selection_totals[8] = data.team_selection_totals[4]   # bench potential lost
        manager_team_selection_totals[9] = data.headers[0]                 # points
        manager_team_selection_totals[10] = data.team_selection_totals[5]  # max points
        manager_team_selection_totals[11] = data.team_selection_totals[6]  # potential lost

        table_data.team_selection_totals.append(manager_team_selection_totals)

    table_data.general_number_max = max_number
    table_data.general_points_max = max_points

    table_data.headers[1] = max_number[1][1]
    table_data.headers[2] = max_number[3][1]

    return table_data
