from django.shortcuts import redirect, render
from fplmystats.utils import manager_utils

# TODO scroll headers with window
# TODO for squad statistics, include captain points for players


def search(request):
    manager_id = request.POST['manager_id']
    return redirect('manager:detail', manager_id)


def detail(request, manager_id):
    # TODO Error checking user input

    names = manager_utils.get_name_and_team(manager_id)
    name = names.manager_name
    team = names.team_name

    stats = manager_utils.get_stats(manager_id)
    headers = stats.headers
    string_headers = []
    for item in headers:
        try:
            string_headers.append("{:,}".format(item))
        except ValueError:
            string_headers.append(item)

    general_number = stats.general_number
    general_number_totals = stats.general_number_totals
    general_number_string_totals = []
    for number in general_number_totals:
        general_number_string_totals.append("{:,}".format(number))

    general_points = stats.general_points
    general_points_totals = stats.general_points_totals
    general_points_string_totals = []
    for number in general_points_totals:
        general_points_string_totals.append("{:,}".format(number))

    positions = stats.positions
    positions_totals = stats.positions_totals
    positions_string_totals = []
    for number in positions_totals:
        positions_string_totals.append("{:,}".format(number))

    team_selection = stats.team_selection
    team_selection_totals = stats.team_selection_totals
    team_selection_string_totals = []
    for number in team_selection_totals:
        team_selection_string_totals.append("{:,}".format(number))
    max_teams = stats.max_teams

    squad_stats_players = stats.squad_stats_players
    squad_stats_teams = stats.squad_stats_teams

    context = {'manager_id': manager_id,
               'manager_name': name,
               'team_name': team,
               'headers': string_headers,
               'general_number': general_number,
               'general_number_totals': general_number_string_totals,
               'general_points': general_points,
               'general_points_totals': general_points_string_totals,
               'positions': positions,
               'positions_totals': positions_string_totals,
               'team_selection': team_selection,
               'team_selection_totals': team_selection_string_totals,
               'max_teams': max_teams,
               'squad_stats_players': squad_stats_players,
               'squad_stats_teams': squad_stats_teams}
    return render(request, 'manager/detail.html', context)
