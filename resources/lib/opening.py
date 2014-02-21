import xbmc
import xbmcgui
import xbmcaddon
from resources.lib import tmdb

addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path')
do_home=False

def startup():
    opening_window = openingWindow('script-openingWindow.xml', addon_path,'default')
    opening_window.doModal()
    del opening_window

class openingWindow(xbmcgui.WindowXMLDialog):
    def onInit(self):
        self.do_now_playing()

    def do_now_playing(self):
        self.getControl(108).setVisible(False)
        self.getControl(107).setVisible(True)
        li=xbmcgui.ListItem
        movies =tmdb.get_movies('now_playing',1)
        self.getControl(201).reset()
        for movie in movies['results']:
            li=xbmcgui.ListItem(movie['title'])
            if movie['poster_path']==None:
                li.setIconImage('no-poster-w92.jpg')
            else:
                li.setIconImage('http://image.tmdb.org/t/p/w92' + movie['poster_path'])
            li.setProperty('movie_id',str(movie['id']))
            self.getControl(201).addItem(li)

    def do_popular(self):
        self.getControl(108).setVisible(True)
        self.getControl(107).setVisible(False)
        li=xbmcgui.ListItem
        movies =tmdb.get_movies('popular',1)
        self.getControl(201).reset()
        for movie in movies['results']:
            li=xbmcgui.ListItem(movie['title'])
            if movie['poster_path']==None:
                li.setIconImage('no-poster-w92.jpg')
            else:
                li.setIconImage('http://image.tmdb.org/t/p/w92' + movie['poster_path'])
            li.setProperty('movie_id',str(movie['id']))
            self.getControl(201).addItem(li)

    def onClick(self,control):
        xbmc.log(str(control))
        if control==104:
            self.do_now_playing()

        if control==105:
            self.do_popular()

        if control==201:
            li=self.getControl(201).getSelectedItem()
            movie_id=int(li.getProperty('movie_id'))
            from resources.lib import movie
            movie.movie_id=movie_id
            movie.startup()

        if control==101:
            from resources.lib import movies
            movies.source='popular'
            movies.page=1
            movies.startup()

        if control==102:
            from resources.lib import tvshows
            tvshows.source='popular'
            tvshows.page=1
            tvshows.startup()

        if control==103:
            from resources.lib import people
            people.source='popular'
            people.page=1
            people.startup()

        if control==99:
            xbmc.log('query=' + self.getControl(100).getText())
            from resources.lib import movies
            movies.source='query'
            movies.doSearch(self.getControl(100).getText())
