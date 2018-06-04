from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from exercises.models import Article, Band, Album


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

