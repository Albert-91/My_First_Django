import datetime

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from football.models import Teams, Games


def league_table(request):
    if request.COOKIES.get('favourite_team') is not None:
        favourite_team_id = int(request.COOKIES.get('favourite_team'))
    sorted_league_teams = Teams.objects.using('football').order_by('-points')
    form = """
            <html>
                <body>
                    <table>
                    {}
                    </table>
                </body>
            </html>
        """
    all_forms = ""

    for league_team in sorted_league_teams:
        if int(league_team.id) == favourite_team_id:
            bgcolor = "#FF0000"
        else:
            bgcolor = "#FFFFFF"
        all_forms += """
            <tr bgcolor={}>
                <td>{}</td>
                <td><a href="http://127.0.0.1:8000/gamesPlayed/{}">{}</a></td>
                <td>{}</td>
                <td><a href="http://127.0.0.1:8000/setAsFavourite/{}">zaznacz jako ulubiony</a></td>
            </tr>
        """.format(bgcolor, league_team.id, league_team.id, league_team.name, league_team.points, league_team.id)

    return HttpResponse(form.format(all_forms))


def games_played(request, id):
    teams = Teams.objects.using('football').get(id=id)
    result = """
        <html>
            <body> 
                <table border="1">
                  <tr><b>
                    <td>Team Home</td>
                    <td>Team Away</td>
                    <td>Score</td>
                  </b></tr> {}
        """
    team_table_home = ""
    for game in teams.team_home.all():
        team_table_home += """
            <tr>
                <td>{}</td>
                <td>{}</td>
                <td>{} : {}</td>
            </tr>""".format(game.team_home.name, game.team_away.name, game.team_home_goals, game.team_away_goals)

    result += """
        <tr>
            <td>Team Home</td>
            <td>Team Away</td>
            <td>Score</td>
        </tr> {}
        """
    team_table_away = ""

    for game in teams.team_away.all():
        team_table_away += """
            <tr>
                <td>{}</td>
                <td>{}</td>
                <td>{} : {}</td>
            </tr>""".format(game.team_home.name, game.team_away.name, game.team_home_goals, game.team_away_goals)

    result += """
                </table>
            <body/>
        <html/>"""

    return HttpResponse(result.format(team_table_home, team_table_away))


@csrf_exempt
def add_game(request):
    teams = Teams.objects.using('football').order_by('-points')
    games = Games.objects.using('football').all()
    form = """
        <form action="#" method="POST">
            <label>
                Klub gospodarzy:
                <br>
                <select name="id_home">
		            {}
                </select>
            </label>
            <label>
                <br>
                Klub gości:
                <br>
                <select name="id_away">
		            {}
                </select>
            </label>
            <label>
                <br>
                Nowy wynik:
                <br>
                <input name="home_points" size="5"> : <input name="away_points" size="5">
            </label>
            <br><br>
            <input type="submit" value="Dodaj wynik meczu">
        </form>
        """
    if request.method == 'GET':
        if request.session.get('team') is not None:
            last_id = int(request.session.get('team'))
        else:
            last_id = 1
        option_home = ''
        option_away = ''
        for i in teams.all():
            if int(i.id) == last_id:
                option_home += "<option value={} selected=""selected"">{}</option>".format(str(i.id), str(i.name))
            else:
                option_home += "<option value={}>{}</option>".format(str(i.id), str(i.name))
            option_away += "<option value={}>{}</option>".format(str(i.id), str(i.name))
        return HttpResponse(form.format(option_home, option_away))
    elif request.method == 'POST':
        id_home = int(request.POST.get("id_home"))
        id_away = int(request.POST.get("id_away"))
        points_away = int(request.POST.get("away_points"))
        points_home = int(request.POST.get("home_points"))
        if isinstance(points_home, int) and isinstance(points_away, int) and id_home != id_away:
            team_home = Teams.objects.using('football').get(id=id_home)
            team_away = Teams.objects.using('football').get(id=id_away)
            games.create(team_home=team_home, team_home_goals=points_home, team_away=team_away,
                         team_away_goals=points_away)
            request.session['team'] = id_home
            if points_home > points_away:
                winner = Teams.objects.using('football').get(id=id_home)
                winner.points += 3
                winner.save()
            elif points_away > points_home:
                winner = Teams.objects.using('football').get(id=id_away)
                winner.points += 3
                winner.save()
            else:
                winner_a = Teams.objects.using('football').get(id=id_home)
                winner_b = Teams.objects.using('football').get(id=id_away)
                winner_a.points += 1
                winner_b.points += 1
                winner_a.save()
                winner_b.save()
            return redirect("http://127.0.0.1:8000/gamesPlayed/{}".format(id_home))
        else:
            return HttpResponse('<h1>Błędnie wpisane dane!</h1>')


@csrf_exempt
def modify_team(request, id):
    teams = Teams.objects.using('football').get(id=id)
    form = """
            <form action="#" method="POST">
                <label>
                    Klub: {} 
                </label>
                <br>
                <label>
                    Liczba punktów:
                    <input name="new_points" size="5" value={}>
                </label>
                <br><br>
                <input type="submit" value="Modyfikuj punkty klubu">
            </form>
            """
    if request.method == 'GET':
        return HttpResponse(form.format(teams.name, teams.points))
    elif request.method == 'POST':
        new_points = int(request.POST.get("new_points"))
        if isinstance(new_points, int):
            teams.points = new_points
            teams.save()
            return redirect("http://127.0.0.1:8000/modifyTeam/{}".format(id))
        else:
            return HttpResponse('Błędnie wprowadzone dane')


def set_as_favourite(request, id):
    if not isinstance(int(id), int):
        return HttpResponse('Błędne ID')
    else:
        try:
            teams = Teams.objects.using('football').get(id=id)
            response = HttpResponse('Ustawiono ulubiony klub o id = {}'.format(id))
            expiry = datetime.datetime.today() + datetime.timedelta(365,0,0,0,0,0,0)
            response.set_cookie('favourite_team', value=id, expires=expiry)
        except Teams.DoesNotExist:
            raise Http404
        return response


def show_team_statistics(request, id):
    form = """
        <p>Nazwa klubu: {}</p>
        <p>Suma zdobytych goli: {}</p>
        <p>Suma straconych goli: {}</p>
        <p>Liczba meczów u siebie: {}</p>
        <p>Liczba meczów na wyjeździe: {}</p>
    """
    teams = Teams.objects.using('football').get(id=id)
    game_home = 0
    game_away = 0
    won_goals = 0
    lost_goals = 0
    for i in teams.team_home.all():
        game_home += 1
        won_goals += int(i.team_home_goals)
        lost_goals += int(i.team_away_goals)
    for j in teams.team_away.all():
        game_away += 1
        won_goals += int(j.team_away_goals)
        lost_goals += int(j.team_home_goals)
    return HttpResponse(form.format(teams.name, won_goals, lost_goals, game_home, game_away))

