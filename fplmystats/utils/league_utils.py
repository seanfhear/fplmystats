from fplmystats.utils import manager_utils
from urllib.error import HTTPError
from collections import namedtuple
import urllib.request
import json

static_url = 'https://fantasy.premierleague.com/drf/bootstrap-static'
classic_league_info_url = 'https://fantasy.premierleague.com/drf/leagues-classic-standings/'
h2h_league_info_url = 'https://fantasy.premierleague.com/drf/leagues-h2h-standings/'

with urllib.request.urlopen('{}'.format(static_url)) as static_json:
    static_data = json.loads(static_json.read().decode())
current_week = 0
for week in static_data['events']:
    if week['is_current']:
        current_week = week['id']


def get_league_name(league_id):
    """
    Return the name of the league
    """
    try:
        data_url = classic_league_info_url + str(league_id)
        with urllib.request.urlopen('{}'.format(data_url)) as url:
            data = json.loads(url.read().decode())
    except HTTPError:
        data_url = h2h_league_info_url + str(league_id)
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
    table_data.positions_totals = []
    table_data.team_selection_totals = []

    table_data.general_number_max = []
    table_data.general_points_max = []
    table_data.positions_max = []
    table_data.team_selection_max = []

    table_data.headers = [0] * 12

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
    max_positions = [[0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-']]
    max_team_selection = [[0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-'], [0, '-']]
    max_team_value = [0, '']
    max_captains = [0, '']
    max_num_players = [0, '']

    have_leader = False

    try:
        data_url = classic_league_info_url + str(league_id)
        with urllib.request.urlopen('{}'.format(data_url)) as url:
            data = json.loads(url.read().decode())
    except HTTPError:
        data_url = h2h_league_info_url + str(league_id)
        with urllib.request.urlopen('{}'.format(data_url)) as url:
            data = json.loads(url.read().decode())

    for entry in data['standings']['results']:
        manager_ids.append([entry['entry'], entry['player_name']])

    for manager_id in manager_ids:
        data = manager_utils.get_stats(manager_id[0])

        if not have_leader:
            table_data.headers[0] = manager_id[1]
            table_data.headers[1] = data.headers[0]
            have_leader = True

        # general number
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

        # general points
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

        # positions
        manager_positions_totals = ([0] * 13)
        manager_positions_totals[0] = manager_id[0]    # manager id
        manager_positions_totals[1] = manager_id[1]    # manager name
        manager_positions_totals[2] = data.headers[6]  # preferred formation

        team_value = data.positions[-1][2]  # team value at latest gameweek
        if team_value > max_team_value[0]:
            max_team_value[0] = team_value
            max_team_value[1] = manager_id[1]
        manager_positions_totals[3] = team_value
        max_positions[0][0] = max_team_value[0]
        max_positions[0][1] = max_team_value[1]

        for i in range(4, 13):
            manager_positions_totals[i] = data.positions_totals[i-3]
        table_data.positions_totals.append(manager_positions_totals)

        for i in range(1, 10):
            if data.positions_totals[i] > max_positions[i][0]:
                max_positions[i][0] = data.positions_totals[i]
                max_positions[i][1] = manager_id[1]

        # team selection
        manager_team_selection_totals = ([0] * 13)
        manager_team_selection_totals[0] = manager_id[0]                   # manager id
        manager_team_selection_totals[1] = manager_id[1]                   # manager name
        manager_team_selection_totals[2] = data.team_selection_totals[0]   # transfer cost
        if max_team_selection[0][0] < data.team_selection_totals[0]:
            max_team_selection[0][0] = data.team_selection_totals[0]
            max_team_selection[0][1] = manager_id[1]

        manager_team_selection_totals[3] = data.headers[3]                 # preferred captain
        manager_team_selection_totals[4] = data.team_selection_totals[1]   # captain points
        if max_team_selection[1][0] < data.team_selection_totals[1]:
            max_team_selection[1][0] = data.team_selection_totals[1]
            max_team_selection[1][1] = manager_id[1]

        manager_team_selection_totals[5] = data.headers[4]                 # season mvp
        manager_team_selection_totals[6] = data.headers[5]                 # mvp points
        if max_team_selection[2][0] < data.headers[5]:
            max_team_selection[2][0] = data.headers[5]
            max_team_selection[2][1] = manager_id[1]

        manager_team_selection_totals[7] = data.team_selection_totals[3]   # captain points lost
        if max_team_selection[3][0] < data.team_selection_totals[3]:
            max_team_selection[3][0] = data.team_selection_totals[3]
            max_team_selection[3][1] = manager_id[1]

        manager_team_selection_totals[8] = data.team_selection_totals[4]   # points on bench
        manager_team_selection_totals[9] = data.team_selection_totals[5]   # bench potential lost
        if max_team_selection[4][0] < data.team_selection_totals[5]:
            max_team_selection[4][0] = data.team_selection_totals[5]
            max_team_selection[4][1] = manager_id[1]

        manager_team_selection_totals[10] = data.headers[0]                # points
        manager_team_selection_totals[11] = data.team_selection_totals[6]  # max points
        if max_team_selection[5][0] < data.team_selection_totals[6]:
            max_team_selection[5][0] = data.team_selection_totals[6]
            max_team_selection[5][1] = manager_id[1]

        manager_team_selection_totals[12] = data.team_selection_totals[7]  # potential lost
        if max_team_selection[6][0] < data.team_selection_totals[7]:
            max_team_selection[6][0] = data.team_selection_totals[7]
            max_team_selection[6][1] = manager_id[1]

        table_data.team_selection_totals.append(manager_team_selection_totals)

        # headers
        captain_points = data.team_selection_totals[1]
        if captain_points > max_captains[0]:
            max_captains[0] = captain_points
            max_captains[1] = manager_id[1]

        num_players = len(data.squad_stats_players)
        if num_players > max_num_players[0]:
            max_num_players[0] = num_players
            max_num_players[1] = manager_id[1]

    table_data.general_number_max = max_number
    table_data.general_points_max = max_points
    table_data.positions_max = max_positions
    table_data.team_selection_max = max_team_selection

    table_data.headers[2] = max_number[1][1]     # most goals
    table_data.headers[3] = max_number[1][0]
    table_data.headers[4] = max_number[3][1]     # most clean sheets
    table_data.headers[5] = max_number[3][0]
    table_data.headers[6] = max_captains[1]      # best captains
    table_data.headers[7] = max_captains[0]
    table_data.headers[8] = max_team_value[1]    # highest team value
    table_data.headers[9] = max_team_value[0]
    table_data.headers[10] = max_num_players[1]  # most unique players
    table_data.headers[11] = max_num_players[0]

    return table_data
