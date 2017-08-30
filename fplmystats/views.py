from django.shortcuts import render


def index(request):
    context = {'manager_error': False,
               'league_error': False}
    return render(request, 'index.html', context)


def index_error(request, manager_error, league_error):
    if manager_error == '1':
        manager_error = True
    else:
        manager_error = False
    if league_error == '1':
        league_error = True
    else:
        league_error = False

    context = {'manager_error': manager_error,
               'league_error': league_error}
    return render(request, 'index.html', context)
