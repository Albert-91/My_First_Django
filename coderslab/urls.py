"""coderslab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import re_path
from exercises.views import show_article, show_band, show_multiplication, show_form, convert, set_session, \
    show_session, delete_session, login, add_to_session, show_sessions, set_cookie, show_cookie, delete_cookie, \
    add_to_cookie, show_all_cookies, AddToCookie, hello_name, random_from_maxint, random_period, show_range
from football.views import league_table, games_played, add_game, modify_team, set_as_favourite, show_team_statistics

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    re_path(r'^articles$', show_article),
    re_path('^show_band/(?P<id>\d+)', show_band),
    # url('^showRange', show_range),
    re_path(r'^showRange/(?P<start>(\d)+)/(?P<end>(\d)+)', show_range),
    re_path(r'^showTable/(?P<width>(\d)+)/(?P<height>(\d)+)', show_multiplication),
    url('^table', league_table),
    re_path('^gamesPlayed/(?P<id>\d+)', games_played),
    re_path('^modifyTeam/(?P<id>\d+)', modify_team),
    re_path('^setAsFavourite/(?P<id>\d+)', set_as_favourite),
    re_path('^stats/(?P<id>\d+)', show_team_statistics),
    url('^addGame', add_game),
    url('^showTable', show_multiplication),
    url('^showForm', show_form),
    url('^showConvert', convert),
    url('^setSession', set_session),
    url('^showSession', show_session),
    url('^deleteSession', delete_session),
    url('^login', login),
    url('^addToSession', add_to_session),
    url('^showAllSession', show_sessions),
    url('^setCookie', set_cookie),
    url('^deleteCookie', delete_cookie),
    url('^showCookie', show_cookie),
    url('^addToCookie$', add_to_cookie),
    url('^addToCookieClass', AddToCookie.as_view()),
    url('^showAllCookies', show_all_cookies),
    re_path(r'^hello/(?P<name>([A-Z]{1})([a-z])+)', hello_name),
    re_path(r'^random/(?P<max_number>(\d)+)$', random_from_maxint),
    re_path(r'^random/(?P<min_number>(\d){2,4})/(?P<max_number>(\d{4})$)', random_period)
]

