import xbmcgui
import xbmc
import xbmcaddon
import os
from resources.lib import utils
from resources.lib import tmdb

addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path')
resources_path = xbmc.translatePath( os.path.join( addon_path, 'resources' ) ).decode('utf-8')
media_path = xbmc.translatePath( os.path.join( resources_path, 'media' ) ).decode('utf-8')
title_font=utils.getTitleFont()
image_base_url=tmdb.get_image_base_url()
source='popular'
query=''
page=1
maxpage=10
genre_id=''
genre_name=''
year=''
person_id=''
person_name=''
def startup():
    movie_results=tmdb.get_movies(source,page)
    movie_ids=movie_results['results']
    total_pages=movie_results['total_pages']
    if total_pages > page:
        movie_ids.append(tmdb.get_movies(source,page+1)['results'][0])
        show_movies(movie_ids,source,page)

def doSearch(query):
    movie_results=tmdb.search_movies(query,1)
    maxpage=movie_results['total_pages']
    movie_ids=movie_results['results']
    if maxpage > page:
        movie_ids.append(tmdb.search_movies(query,page+1)['results'][0])    
    show_movies(movie_ids,'query',1)

def show_movies(movie_ids,source,page):
    movie_window = moviesWindow('script-movieWindow.xml', addon_path,'default')
    movie_window.source=source
    movie_window.movies=movie_ids
    movie_window.doModal()

class moviesWindow(xbmcgui.WindowXMLDialog):  
    movies=[]
    controls=[]
    title=xbmcgui.ControlLabel
    backdrop=xbmcgui.ControlImage
    session_id=''
    
    def onInit(self):
        self.getControl(599).setVisible(False)
        self.session_id=addon.getSetting('session_id')
        self.update_movies(self.movies)
    def update_movies(self,movies):
        self.getControl(32120).setLabel('Page ' + str(page) + ' of ' + str(maxpage))
        title=xbmcgui.ControlButton(85,175,1000,30,'','','',0,0,0,title_font,'ff606060','',0,'','ff606060')
        self.addControl(title)
        for i in range(0,21):
            if len(movies)>i:
                self.getControl(i+500).setImage('loading-w92.jpg')
            else:
                self.getControl(i+400).setEnabled(False) 
        xbmc_movies=utils.get_xbmc_movies()
        for i in range(0,21):
            if len(movies)>i:
                if movies[i]['release_date']!=None:
                    if movies[i]['title'] + ' ('+ movies[i]['release_date'][:4] +')' in xbmc_movies:
                        self.getControl(i+300).setImage('xbmc_icon.png')
                self.getControl(i+400).setEnabled(True)
                if movies[i]['poster_path']==None:
                    self.getControl(i+200).setImage('no-poster-w92.jpg')
                else:
                    self.getControl(i+200).setImage('http://image.tmdb.org/t/p/w92' +movies[i]['poster_path'])
                if i==0:self.onFocus(400)
        self.getControl(599).setVisible(True)
        xbmc.log(source)
        if source=='popular':self.getControl(32111).setLabel('Popular Movies')
        if source=='top_rated':self.getControl(32111).setLabel('Top Rated Movies')
        if source=='upcoming':self.getControl(32111).setLabel('Upcoming Movies')
        if source=='now_playing':self.getControl(32111).setLabel('Now Playing Movies')
        if source=='query':self.getControl(32111).setLabel('Search Results')
        if source=='favorites':self.getControl(32111).setLabel('Favorite Movies')
        if source=='watchlist':self.getControl(32111).setLabel('Movies on Watchlist')
        if source=='rated':self.getControl(32111).setLabel('Rated Movies')
        if source=='genre':self.getControl(32111).setLabel(genre_name + ' Movies')
        if source=='years':self.getControl(32111).setLabel('Movies From ' + year)
        if source=='person':self.getControl(32111).setLabel('Movies with ' + person_name)

    def onAction(self, action):
        if action == 10:
            d = xbmcgui.Dialog()
            ans=d.yesno('tmdb Browser','Exit themoviedb.org Browser?')
            if ans:
                xbmc.executebuiltin('Dialog.Close(all,true)')
        elif action == 92:
            self.close()

    def onFocus(self,control):
        movieid=''
        backdrop = self.getControl(32107)
        movieid=self.get_movieid_from_control(control)
        if movieid!='':
            cast=self.getControl(32109)
            plot=self.getControl(32108)
            movie=tmdb.get_movie(movieid)
            actors = movie['credits']['cast']
            actors=sorted(actors, key=lambda k: k['order'])
            a = ''
            i=0
            for actor in actors:
                i=i+1
                a=a + actor['name'] +", "
                if i==3:break
            cast.setLabel(a[:-2])
            try:
                self.getControl(3001).setLabel(movie['title'] + ' ('+ movie['release_date'][:4] +')')
            except:
                pass
            plot.setText(movie['overview'])
            backdrop.setImage('')
            if movie['backdrop_path']!=None:
                self.getControl(32121).setLabel('Loading')
                backdrop.setImage('http://image.tmdb.org/t/p/w300' +movie['backdrop_path'])
            else:
                self.getControl(32121).setLabel('No Background Available')
    
    def onClick(self,control):
        global source
        global query
        global page
        global maxpage
        global genre_id
        global genre_name
        global year
        global person_id
        global person_name
        movieid=''
        movieid=self.get_movieid_from_control(control)
        do_movies=False
        do_tv=False
        do_people=False

        popular = 32101
        top_rated =  32102
        upcoming = 32103
        now_playing = 32104
        favorites = 33105
        watchlist = 33106
        rated = 33107
        query_btn = 81
        previous = 32116
        next =32117
        tv_shows = 32114
        people = 32115
        genre_btn=82
        year_btn=83
        person_btn=84

        if movieid!='':
            from resources.lib import movie
            movie.movie_id=movieid
            movie_window = movie.movieWindow('script-movieDetailWindow.xml', addon_path,'default')
            movie_window.doModal()
            del movie_window

        if control == popular:
            source='popular'
            page=1
            do_movies=True
        if control == top_rated:
            source='top_rated'
            do_movies=True
            page=1
        if control == upcoming:
            source='upcoming'
            do_movies=True
            page=1
        if control == now_playing:
            source='now_playing'
            do_movies=True
            page=1
        if control == favorites:
            do_movies=True
            source = 'favorites'
            page=1
        if control == watchlist:
            do_movies=True
            source = 'watchlist'
            page=1
        if control == rated:
            do_movies=True
            source = 'rated'
            page=1
        if control == query_btn:
            source='query'
            do_movies=True
            page=1
        if control == genre_btn:
            source='genre'
            page=1
            genre_id=''
            do_movies=True
        if control == year_btn:
            source='years'
            page=1
            year=''
            do_movies=True
        if control == person_btn:
            source='person'
            page=1
            person_id=''
            person_name=''
            do_movies=True
        if control == next:
            if page < maxpage:
                page=page+1
                do_movies=True
        if control == previous:
            if page > 1:
                page=page-1
                do_movies=True
        if control == tv_shows:
            do_tv=True
        if control ==people:
            do_people=True

        if do_movies:
            ans=True
            if source=='query':
                self.getControl(80).setVisible(True)
                if control==query_btn:
                    k=xbmc.Keyboard('','Enter Movie Title to Search For')
                    k.doModal()
                    query=k.getText()
                if query!='':
                    movies=tmdb.search_movies(query,page)
                    maxpage=movies['total_pages']
                    movies=movies['results']
                    if maxpage > page:
                        movies.append(tmdb.search_movies(query,page+1)['results'][0])    
                    self.close()
                    show_movies(movies,source,page)
            elif source=='favorites':
                if self.session_id=='':
                    session_id=utils.get_login()
                    if session_id!='':self.session_id=session_id
                if self.session_id!='':
                    movies=tmdb.get_favorite_movies(self.session_id,page)
                    total_pages=movies['total_pages']     
                    maxpage=total_pages
                    movies=movies['results']
                    if total_pages > page:
                        movies.append(tmdb.get_favorite_movies(self.session_id,page+1)['results'][0])
                    self.close()
                    show_movies(movies,source,page) 
            elif source=='watchlist':
                if self.session_id=='':
                    session_id=utils.get_login()
                    if session_id!='':self.session_id=session_id
                if self.session_id!='':
                    movies=tmdb.get_watchlist_movies(self.session_id,page)
                    total_pages=movies['total_pages']     
                    maxpage=total_pages
                    movies=movies['results']
                    if total_pages > page:
                        movies.append(tmdb.get_watchlist_movies(self.session_id,page+1)['results'][0])
                    self.close()
                    show_movies(movies,source,page) 
            elif source=='rated':
                if self.session_id=='':
                    session_id=utils.get_login()
                    if session_id!='':self.session_id=session_id
                if self.session_id!='':
                    movies=tmdb.get_rated_movies(self.session_id,page)
                    total_pages=movies['total_pages']     
                    maxpage=total_pages
                    movies=movies['results']
                    if total_pages > page:
                        movies.append(tmdb.get_rated_movies(self.session_id,page+1)['results'][0])
                    self.close()
                    show_movies(movies,source,page)  
            elif source=='genre':
                if genre_id=='':
                    dg=dialogWindow('dialog_select.xml',addon_path,'Default')
                    dg.mode='genre'
                    dg.doModal() 
                if genre_id!='':
                    movies=tmdb.get_movies_by_genre(genre_id,page)  
                    total_pages=movies['total_pages']
                    movies=movies['results']
                    maxpage=total_pages 
                    if total_pages > page:
                        movies.append(tmdb.get_movies_by_genre(genre_id,page+1)['results'][0])
                    self.close()
                    show_movies(movies,source,page) 
            elif source == 'years':
                if year=='':
                    kb=xbmc.Keyboard('','Enter Year')
                    kb.doModal()
                    year=kb.getText()
                movies=tmdb.get_movies_by_year(year,page)
                total_pages=movies['total_pages']
                movies=movies['results']
                maxpage=total_pages
                if total_pages > page:
                    movies.append(tmdb.get_movies_by_year(year,page+1)['results'][0])
                self.close()
                show_movies(movies,source,page)
            elif source=='person': 
                if person_id=='':
                    kb=xbmc.Keyboard('','Enter Persons Name')
                    kb.doModal()
                    person_name=kb.getText()
                    if person_name !='':
                        dg=dialogWindow('dialog_select.xml',addon_path,'Default')
                        dg.mode='people'
                        dg.doModal() 
                movies=tmdb.getMoviesByActor(person_id,page)
                pages=len(movies) / 20
                if len(movies) % 20 > 0:pages=pages+1
                total_pages=pages
                xbmc.log(str(len(movies)))
                maxpage=total_pages
                self.close()
                movies=sorted(movies, key=lambda k: k['release_date'],reverse=True)
                person_movies=[]
                if page > 1:
                    for i in range((page * 20)-20,(page * 20)+1):
                        if i < len(movies):
                            person_movies.append(movies[i])
                    movies=person_movies
                show_movies(movies,source,page)                             
            else:
                query=''
                xbmc.log(source)
                movies=tmdb.get_movies(source,page)
                total_pages=movies['total_pages']
                maxpage=10
                if source=='upcoming' or source=='now_playing':maxpage=movies['total_pages']
                movies=movies['results']
                if total_pages > page:
                    movies.append(tmdb.get_movies(source,page+1)['results'][0])
                self.close()
                show_movies(movies,source,page)
        elif do_tv:
            from resources.lib import tvshows
            self.close()
            tvshows.startup()
        elif do_people:
            from resources.lib import people
            self.close()
            people.startup()

    def get_movieid_from_control(self,control):
        movieid=''
        if control==400:movieid=self.movies[0]['id']
        if control==401:movieid=self.movies[1]['id']
        if control==402:movieid=self.movies[2]['id']
        if control==403:movieid=self.movies[3]['id']
        if control==404:movieid=self.movies[4]['id']
        if control==405:movieid=self.movies[5]['id']
        if control==406:movieid=self.movies[6]['id']
        if control==407:movieid=self.movies[7]['id']
        if control==408:movieid=self.movies[8]['id']
        if control==409:movieid=self.movies[9]['id']
        if control==410:movieid=self.movies[10]['id']
        if control==411:movieid=self.movies[11]['id']
        if control==412:movieid=self.movies[12]['id']
        if control==413:movieid=self.movies[13]['id']
        if control==414:movieid=self.movies[14]['id']
        if control==415:movieid=self.movies[15]['id']
        if control==416:movieid=self.movies[16]['id']
        if control==417:movieid=self.movies[17]['id']
        if control==418:movieid=self.movies[18]['id']
        if control==419:movieid=self.movies[19]['id']
        if control==420:movieid=self.movies[20]['id']
        return movieid

class dialogWindow(xbmcgui.WindowXMLDialog):
    mode=''
    def onInit(self):
        global person_name
        if self.mode=='genre':
            self.getControl(1).setLabel('Search for Movies by Genre')
            for genre in tmdb.get_genres():
                li=xbmcgui.ListItem(genre['name'])
                li.setProperty('id',str(genre['id']))
                self.getControl(300).addItem(li)
        if self.mode=='people':
            self.getControl(1).setLabel('Select Person')
            for person in tmdb.search_people(person_name,1)['results']:     
                li=xbmcgui.ListItem(person['name'])
                li.setProperty('id',str(person['id']))
                self.getControl(300).addItem(li)

    def onClick(self,control):
        global genre_id
        global genre_name
        global person_id
        global person_name
        if self.mode=='genre':
            genre_id=self.getControl(300).getSelectedItem().getProperty('id')
            genre_name=self.getControl(300).getSelectedItem().getLabel()
        if self.mode=='people':
            person_id=self.getControl(300).getSelectedItem().getProperty('id')
            person_name=self.getControl(300).getSelectedItem().getLabel()
        self.close()