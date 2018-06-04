from exercises.models import Band, Category, Article, Album
from random import randint, choice


def null_year():
    return Band.objects.filter(year=None)


def fill_year(bands):
    for band in bands:
        new_year = randint(1950, 2018)
        band.year = new_year
        band.save()


def fill_info(atr, options):
    bands = Band.objects.all()
    for band in bands:
        setattr(band, atr, choice(options))
        band.save()


def fill_category():
    category = Category.objects
    names = ['wywiad', 'fraszka', 'felieton', 'akcja', 'romans']
    descriptions = ['zabawny', 'krótki', 'długi', 'śmieszny', 'poważny']
    for i in range(5):
        category.create(name=names[i], description=descriptions[i])


def fill_articles():
    article = Article.objects
    article.create(title='spiderman', content="""
Did shy say mention enabled through elderly improve. 
As at so believe account evening behaved hearted is. 
House is tiled we aware. It ye greatest removing concerns 
an overcame appetite. Manner result square father boy behind
 its his. Their above spoke match ye mr right oh as first. 
 Be my depending to believing perfectly concealed household. Point could to built no hours smile sense. """, status=1)
    article.create(title='avengers', content="""one sufficient terminated frequently themselves. It more shed went up is roof if loud case. Delay music in lived noise an. Beyond genius really enough passed is up. """, status=2)
    article.create(title='star wars', content="""ex general nay certain. Mrs for recommend exquisite household eagerness preserved now. My improved honoured he am ecstatic quitting greatest formerly. 
""", status=3)
    article.create(title='spiderman2', content="""disposal my speaking. Direct wholly valley or uneasy it at really. Sir wish like said dull and need make. Sportsman one bed departure rapturous situation disposing his. Off say yet ample ten ought hence. Depending in newspaper an september do exist""", status=1)
    article.create(title='spiderman3', content="""might set along charm now equal green. Pleased yet equally correct colonel not one. Say anxious carried compact conduct sex general nay certain. Mrs for recommend exquisite household eagerness preserved now. My imp""", status=2)


def filter_1():
    bands = Band.objects.filter(name__contains="The")
    return bands


def filter_2():
    bands = Band.objects.filter(year__range=(1980, 1989)).filter(still_active=True)
    return bands


def filter_3():
    bands = Band.objects.filter(year__range=(1970, 1979)).filter(name__contains="The")
    return bands


def filter_4():
    bands = Band.objects.filter(year__range=(1980, 1989)).filter(still_active=False)
    return bands


def show_albums(band):
    albums = Album.objects.filter(year__range=(1970, 1979)).filter(name__contains="The")


