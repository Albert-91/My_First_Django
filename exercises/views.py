from random import randint

from django.http import HttpResponse

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from exercises.models import Article, Band


def show_article(request):
    articles = Article.objects.filter(status=3)
    form = """
        <html>
            <body>
                {}
            </body>
        </html>
    """
    all_forms = ""
    for article in articles:
        all_forms += str(article.title)
        all_forms += str(article.status)
        all_forms += str(article.date_added)
        all_forms += str(article.content)

    return HttpResponse(form.format(all_forms))


def show_band(request, id):
    bands = Band.objects.filter(id=id)
    form = """
            <html>
                <body>
                    Band information:
                    <br>
                    {}
                    Albums:
                    <br>
                    {}
                    Songs:
                    <br>
                    {}
                </body>
            </html>
        """
    all_forms = ""
    all_albums = ""
    all_songs = ""
    for band in bands:
        all_forms += str(band.name) + "<br>"
        all_forms += str(band.get_genre_display()) + "<br>"
        all_forms += str(band.year) + "<br>"
        all_forms += str(band.still_active) + "<br>"
        albums = band.album_set.all()
        for album in albums:
            all_albums += str(album) + "<br>"
            for song in album.song_set.all():
                all_songs += str(song.title) + "<br>"

    return HttpResponse(form.format(all_forms, all_albums, all_songs))


def show_range(request, start, end):
    if request.method == 'GET':
        # start = int(request.GET.get("start"))
        # end = int(request.GET.get("end"))
        result = ""
        for i in range(int(start), int(end)+1):
            result += str(i) + ", "
    else:
        result = 'Not GET method'
    return HttpResponse(result)


def show_multiplication(request, width, height):
    answer = "<html><head></head><body><table border=3>"
    # width = int(request.GET["width"])
    # height = int(request.GET["height"])

    for i in range(1, int(height)+1):
        answer += "<tr>"
        for j in range(1, int(width)+1):
            answer += '<td>{}</td>'.format(i*j)
        answer += "</tr>"
    answer += "<table></body></html>"
    return HttpResponse(answer)


@csrf_exempt
def show_form(request):
    form = """
    <form action="#" method="POST">
        <label>
            Imię
            <input type="text" name="userName">
        </label>
        <label>
            Nazwisko
            <input type="text" name="userSurname">
        </label>
        <label>
            Imię
            <input type="submit" value="Wyślij">
        </label>
    </form>
    """
    result = """
        <p>
            Witaj {} {}!
        </p>
    """
    if request.method == 'GET':
        return HttpResponse(form)
    elif request.method == 'POST':
        name = request.POST.get("userName")
        surname = request.POST.get("userSurname")
        if name and surname:
            return HttpResponse(result.format(name, surname))
        else:
            return HttpResponse('Źle wprowadzone dane <br>' + form)


@csrf_exempt
def convert(request):
    form = '''
    <form action="#" method="POST">
        <label>
            Temperatura:
            <input type="number" min="0.00" step="0.01" name="degrees">
        </label>
        <input type="submit" name="convertionType" value="celcToFahr">
        <input type="submit" name="convertionType" value="FahrToCelc">
    </form>
    '''
    result_form = '''
    <p>
        Temperatura to {:.1f} {}
    </p>
    '''
    if request.method == 'GET':
        return HttpResponse(form)
    elif request.method == 'POST':
        button = request.POST.get("convertionType")
        degrees = float(request.POST.get("degrees"))

        if button == 'celcToFahr':
            unit = ' °F'
            result = float(32 + (9/5 * degrees))
            result = result
        else:
            unit = ' °C'
            result = float(5 / 9 * (degrees - 32))
            result = result

        return HttpResponse(result_form.format(result, unit))


'''sessions'''


def set_session(request):
    if request.session.get('counter') is None:
        response = 'Counter has been set'
        request.session['counter'] = 0
    else:
        response = 'Counter was there already'
    return HttpResponse(response)


def show_session(request):
    result = request.session['counter']
    result += 1
    request.session['counter'] = result
    return HttpResponse('Licznik wynosi {}'.format(result))


def delete_session(request):
    if request.session.get('counter') is not None:
        request.session.pop('counter', None)
    # request.session.pop('loggedUser')
    return HttpResponse('Dane z sesji zostały usunięte')


@csrf_exempt
def login(request):
    form = '''
    <form action="#" method="POST">
        <label>
            Imię:
            <input type="text" name="name" value="{}">
        </label>
        <input type="submit" name="convertionType">
        <br>
        <label>
            Zapamiętaj mnie
            <input type="checkbox" name="rememberMe">
        </label>
    </form>
    '''
    form_with_logout = """
    <form action="#" method="POST">
        <label>
            Witaj {}!
            <input type="submit" name="convertionType" value="Wyloguj">
        </label>
    </form>
    """
    if request.COOKIES.get('User') is not None:
        answer = request.COOKIES.get('User')
    else:
        answer = ""

    if request.method == 'GET' and request.session.get('loggedUser') is None:
        result = form.format(answer)

    elif request.method == 'GET':
        name = request.session.get('loggedUser')
        result = form_with_logout.format(name)

    elif request.method == 'POST' and request.session.get('loggedUser') is not None:
        request.session.pop('loggedUser')
        result = form.format(answer)

    elif request.method == 'POST':
        remember_me = request.POST.get("rememberMe")
        name = request.POST.get("name")
        if name is not None:
            request.session['loggedUser'] = name
        if remember_me:
            response = HttpResponse()
            response.set_cookie('User', value='Albert')
        result = form.format()

    return HttpResponse(result)


def dict_form_html():
    form = '''
    <form action="#" method="POST">
        <label>
            Klucz:
            <input type="text" name="key">
        </label>
        <label>
            Wartość:
            <input type="text" name="value">
        </label>
        <input type="submit" name="convertionType">
    </form>
    '''
    return form


def wrap_form(func):
    def wrap(request):
        answer = '<p>Zastosowano wrap</p>'
        return HttpResponse(func(request) + answer)
    return wrap


@csrf_exempt
def add_to_session(request):
    if request.method == 'GET':
        return HttpResponse(dict_form_html())
    elif request.method == 'POST':
        key = request.POST.get("key")
        value = request.POST.get("value")
        if key and value is not None:
            request.session[key] = value
            answer = '{} => {} dodane do sesji'.format(key, value)
        return HttpResponse(answer)


@wrap_form
def show_sessions(request):
    answer = '<table>'
    for key, value in request.session.items():
        answer += '<tr><td>{} {}</td></tr>'.format(key, value)
    answer += '</answer>'

    return answer


"""cookies"""


def set_cookie(request):
    response = HttpResponse('Ciasteczko ustawione')
    response.set_cookie('User', value='Albert')
    return response


def show_cookie(request):
    if request.COOKIES.get('User') is None:
        answer = 'Brak ciasteczka'
    else:
        answer = request.COOKIES.get('User')
    return HttpResponse(answer)


def delete_cookie(request):
    response = HttpResponse('Ciasteczko usunięte')
    response.delete_cookie('User')
    return response


@csrf_exempt
def add_to_cookie(request):
    if request.method == 'GET':
        response = HttpResponse(dict_form_html())
    elif request.method == 'POST':
        key = request.POST.get('key')
        value = request.POST.get('value')
        response = HttpResponse()
        response.set_cookie(key, value=value)
        response.write('Dodano ciasteczko')
    return response


@method_decorator(csrf_exempt, name='dispatch')
class AddToCookie(View):
    def get(self, request):
        return HttpResponse(dict_form_html())

    def post(self, request):
        key = request.POST.get('key')
        value = request.POST.get('value')
        response = HttpResponse()
        response.set_cookie(key, value=value)
        response.write('Dodano ciasteczko')
        return response


def show_all(dictionary):
    answer = '<table>'
    for key, value in dictionary.items():
        answer += '<tr><td>{} {}</td></tr>'.format(key, value)
    answer += '</answer>'
    return answer


def show_all_cookies(request):
    result = show_all(request.COOKIES)
    return HttpResponse(result)


def random_from_maxint(request, max_number):
    max_int = int(max_number)
    result = randint(0, max_int)
    return HttpResponse('Użytkownik podał wartość {}. Wylosowano liczbę: {}'.format(max_int, result))


def random_period(request, min_number, max_number):
    min_int = int(min_number)
    max_int = int(max_number)
    result = randint(min_int, max_int)
    return HttpResponse('Użytkownik podał wartośći {} i {}. Wylosowano liczbę: {}'.format(min_int, max_int, result))


def hello_name(request, name):
    return HttpResponse('Witaj {}'.format(name))
