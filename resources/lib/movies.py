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
no_poster_path = xbmc.translatePath( os.path.join( media_path, 'no-poster-w92.jpg' ) ).decode('utf-8')
no_background_path = xbmc.translatePath( os.path.join( media_path, 'no-background-w300.jpg' ) ).decode('utf-8')
title_font=utils.getTitleFont()
image_base_url=tmdb.get_image_base_url()
source='popular'
query=''
page=1
maxpage=10

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
        self.session_id=addon.getSetting('session_id')
        xbmc.log('init window')
        base_font=utils.getBaseFont()
        self.update_movies(self.movies)

    def update_movies(self,movies):
        b0=xbmcgui.ControlLabel(0,0,0,0,'')
        b1=xbmcgui.ControlLabel(0,0,0,0,'')
        b2=xbmcgui.ControlLabel(0,0,0,0,'')
        b3=xbmcgui.ControlLabel(0,0,0,0,'')
        b4=xbmcgui.ControlLabel(0,0,0,0,'')
        b5=xbmcgui.ControlLabel(0,0,0,0,'')
        b6=xbmcgui.ControlLabel(0,0,0,0,'')
        b7=xbmcgui.ControlLabel(0,0,0,0,'')
        b8=xbmcgui.ControlLabel(0,0,0,0,'')
        b9=xbmcgui.ControlLabel(0,0,0,0,'')
        b10=xbmcgui.ControlLabel(0,0,0,0,'')
        b11=xbmcgui.ControlLabel(0,0,0,0,'')
        b12=xbmcgui.ControlLabel(0,0,0,0,'')
        b13=xbmcgui.ControlLabel(0,0,0,0,'')
        b14=xbmcgui.ControlLabel(0,0,0,0,'')
        b15=xbmcgui.ControlLabel(0,0,0,0,'')
        b16=xbmcgui.ControlLabel(0,0,0,0,'')
        b17=xbmcgui.ControlLabel(0,0,0,0,'')
        b18=xbmcgui.ControlLabel(0,0,0,0,'')
        b19=xbmcgui.ControlLabel(0,0,0,0,'')
        b20=xbmcgui.ControlLabel(0,0,0,0,'')
        xbmc.log('Updating Movies')
        self.getControl(32120).setLabel('Page ' + str(page) + ' of ' + str(maxpage))

        self.removeControls(self.controls)
        if len(movies)>0:
            if movies[0]['poster_path']==None:
                b0=xbmcgui.ControlButton(466,225,92,138,movies[0]['title'],no_poster_path,no_poster_path)
            else:
                b0=xbmcgui.ControlButton(466,225,92,138,'','http://image.tmdb.org/t/p/w92' +movies[0]['poster_path'],'http://image.tmdb.org/t/p/w92' + movies[0]['poster_path'])
        if len(movies) > 1:
            if movies[1]['poster_path']==None:
                b1=xbmcgui.ControlButton(578,225,92,138,movies[1]['title'],no_poster_path,no_poster_path)
            else:
                b1=xbmcgui.ControlButton(578,225,92,138,'','http://image.tmdb.org/t/p/w92' +movies[1]['poster_path'],'http://image.tmdb.org/t/p/w92' + movies[1]['poster_path'])
        if len(movies) > 2:
            if movies[2]['poster_path']==None:
                b2=xbmcgui.ControlButton(690,225,92,138,movies[2]['title'],no_poster_path,no_poster_path)
            else:        
                b2=xbmcgui.ControlButton(690,225,92,138,'','http://image.tmdb.org/t/p/w92' +movies[2]['poster_path'],'http://image.tmdb.org/t/p/w92' + movies[2]['poster_path'])
        if len(movies) > 3:
            if movies[3]['poster_path']==None:
                b3=xbmcgui.ControlButton(802,225,92,138,movies[3]['title'],no_poster_path,no_poster_path)
            else:        
                b3=xbmcgui.ControlButton(802,225,92,138,'','http://image.tmdb.org/t/p/w92' +movies[3]['poster_path'],'http://image.tmdb.org/t/p/w92' + movies[3]['poster_path'])
        if len(movies) > 4:
            if movies[4]['poster_path']==None:
                b4=xbmcgui.ControlButton(914,225,92,138,movies[4]['title'],no_poster_path,no_poster_path)
            else: 
                b4=xbmcgui.ControlButton(914,225,92,138,'','http://image.tmdb.org/t/p/w92' +movies[4]['poster_path'],'http://image.tmdb.org/t/p/w92' + movies[4]['poster_path'])
        if len(movies) > 5:
            if movies[5]['poster_path']==None:
                b5=xbmcgui.ControlButton(1026,225,92,138,movies[5]['title'],no_poster_path,no_poster_path)
            else: 
                b5=xbmcgui.ControlButton(1026,225,92,138,'','http://image.tmdb.org/t/p/w92' +movies[5]['poster_path'],'http://image.tmdb.org/t/p/w92' + movies[5]['poster_path'])
        if len(movies) > 6:
            if movies[6]['poster_path']==None:
                b6=xbmcgui.ControlButton(1138,225,92,138,movies[6]['title'],no_poster_path,no_poster_path)
            else: 
                b6=xbmcgui.ControlButton(1138,225,92,138,'','http://image.tmdb.org/t/p/w92' +movies[6]['poster_path'],'http://image.tmdb.org/t/p/w92' + movies[6]['poster_path'])
        if len(movies) > 7:
            if movies[7]['poster_path']==None:
                b7=xbmcgui.ControlButton(466,383,92,138,movies[7]['title'],no_poster_path,no_poster_path)
            else: 
                b7=xbmcgui.ControlButton(466,383,92,138,'','http://image.tmdb.org/t/p/w92' +movies[7]['poster_path'],'http://image.tmdb.org/t/p/w92' + movies[7]['poster_path'])
        if len(movies) > 8:
            if movies[8]['poster_path']==None:
                b8=xbmcgui.ControlButton(578,383,92,138,movies[8]['title'],no_poster_path,no_poster_path)
            else: 
                b8=xbmcgui.ControlButton(578,383,92,138,'','http://image.tmdb.org/t/p/w92' +movies[8]['poster_path'],'http://image.tmdb.org/t/p/w92' + movies[8]['poster_path'])
        if len(movies) > 9:
            if movies[9]['poster_path']==None:
                b9=xbmcgui.ControlButton(690,383,92,138,movies[9]['title'],no_poster_path,no_poster_path)
            else: 
                b9=xbmcgui.ControlButton(690,383,92,138,'','http://image.tmdb.org/t/p/w92' +movies[9]['poster_path'],'http://image.tmdb.org/t/p/w92' + movies[9]['poster_path'])
        if len(movies) > 10:
            if movies[10]['poster_path']==None:
                b10=xbmcgui.ControlButton(802,383,92,138,movies[10]['title'],no_poster_path,no_poster_path)
            else: 
                b10=xbmcgui.ControlButton(802,383,92,138,'','http://image.tmdb.org/t/p/w92' +movies[10]['poster_path'],'http://image.tmdb.org/t/p/w92' + movies[10]['poster_path'])
        if len(movies) > 11:
            if movies[11]['poster_path']==None:
                b11=xbmcgui.ControlButton(914,383,92,138,movies[11]['title'],no_poster_path,no_poster_path)
            else:  
                b11=xbmcgui.ControlButton(914,383,92,138,'','http://image.tmdb.org/t/p/w92' +movies[11]['poster_path'],'http://image.tmdb.org/t/p/w92' + movies[11]['poster_path'])
        if len(movies) > 12:
            if movies[12]['poster_path']==None:
                b12=xbmcgui.ControlButton(1026,383,92,138,movies[12]['title'],no_poster_path,no_poster_path)
            else:  
                b12=xbmcgui.ControlButton(1026,383,92,138,'','http://image.tmdb.org/t/p/w92' +movies[12]['poster_path'],'http://image.tmdb.org/t/p/w92' + movies[12]['poster_path'])
        if len(movies) > 13:
            if movies[13]['poster_path']==None:
                b13=xbmcgui.ControlButton(1138,383,92,138,movies[13]['title'],no_poster_path,no_poster_path)
            else:  
                b13=xbmcgui.ControlButton(1138,383,92,138,'','http://image.tmdb.org/t/p/w92' +movies[13]['poster_path'],'http://image.tmdb.org/t/p/w92' + movies[13]['poster_path'])
        if len(movies) > 14:
            if movies[14]['poster_path']==None:
                b14=xbmcgui.ControlButton(466,541,92,138,movies[14]['title'],no_poster_path,no_poster_path)
            else:  
                b14=xbmcgui.ControlButton(466,541,92,138,'','http://image.tmdb.org/t/p/w92' +movies[14]['poster_path'],'http://image.tmdb.org/t/p/w92' + movies[14]['poster_path'])
        if len(movies) > 15:
            if movies[15]['poster_path']==None:
                b15=xbmcgui.ControlButton(578,541,92,138,movies[15]['title'],no_poster_path,no_poster_path)
            else:  
                b15=xbmcgui.ControlButton(578,541,92,138,'','http://image.tmdb.org/t/p/w92' +movies[15]['poster_path'],'http://image.tmdb.org/t/p/w92' + movies[15]['poster_path'])
        if len(movies) > 16:
            if movies[16]['poster_path']==None:
                b16=xbmcgui.ControlButton(690,541,92,138,movies[16]['title'],no_poster_path,no_poster_path)
            else:  
                b16=xbmcgui.ControlButton(690,541,92,138,'','http://image.tmdb.org/t/p/w92' +movies[16]['poster_path'],'http://image.tmdb.org/t/p/w92' + movies[16]['poster_path'])
        if len(movies) > 17:
            if movies[17]['poster_path']==None:
                b17=xbmcgui.ControlButton(802,541,92,138,movies[17]['title'],no_poster_path,no_poster_path)
            else:  
                b17=xbmcgui.ControlButton(802,541,92,138,'','http://image.tmdb.org/t/p/w92' +movies[17]['poster_path'],'http://image.tmdb.org/t/p/w92' + movies[17]['poster_path'])
        if len(movies) > 18:
            if movies[18]['poster_path']==None:
                b18=xbmcgui.ControlButton(914,541,92,138,movies[18]['title'],no_poster_path,no_poster_path)
            else:  
                b18=xbmcgui.ControlButton(914,541,92,138,'','http://image.tmdb.org/t/p/w92' +movies[18]['poster_path'],'http://image.tmdb.org/t/p/w92' + movies[18]['poster_path'])
        if len(movies) > 19:
            if movies[19]['poster_path']==None:
                b19=xbmcgui.ControlButton(1026,541,92,138,movies[19]['title'],no_poster_path,no_poster_path)
            else:  
                b19=xbmcgui.ControlButton(1026,541,92,138,'','http://image.tmdb.org/t/p/w92' +movies[19]['poster_path'],'http://image.tmdb.org/t/p/w92' + movies[19]['poster_path'])
        if len(movies) > 20:
            if movies[20]['poster_path']==None:
                b20=xbmcgui.ControlButton(1138,541,92,138,movies[20]['title'],no_poster_path,no_poster_path)
            else:  
                b20=xbmcgui.ControlButton(1138,541,92,138,'','http://image.tmdb.org/t/p/w92' +movies[20]['poster_path'],'http://image.tmdb.org/t/p/w92' + movies[20]['poster_path'])
        title=xbmcgui.ControlButton(85,175,1000,30,'','','',0,0,0,title_font,'ff606060','',0,'','ff606060')

        
        controls=[]
        xbmc.log(media_path)
        controls.append(b0)
        controls.append(b1)
        controls.append(b2)
        controls.append(b3)
        controls.append(b4)
        controls.append(b5)
        controls.append(b6)
        controls.append(b7)
        controls.append(b8)
        controls.append(b9)
        controls.append(b10)
        controls.append(b11)
        controls.append(b12)
        controls.append(b13)
        controls.append(b14)
        controls.append(b15)
        controls.append(b16)
        controls.append(b17)
        controls.append(b18)
        controls.append(b19)
        controls.append(b20)
        controls.append(title)
        self.addControls(controls)

        b0.setAnimations([('focus','effect=zoom center=auto end=115 time=200')])
        b1.setAnimations([('focus','effect=zoom center=auto end=115 time=200')])
        b2.setAnimations([('focus','effect=zoom center=auto end=115 time=200')])
        b3.setAnimations([('focus','effect=zoom center=auto end=115 time=200')])
        b4.setAnimations([('focus','effect=zoom center=auto end=115 time=200')])
        b5.setAnimations([('focus','effect=zoom center=auto end=115 time=200')])
        b6.setAnimations([('focus','effect=zoom center=auto end=115 time=200')])
        b7.setAnimations([('focus','effect=zoom center=auto end=115 time=200')])
        b8.setAnimations([('focus','effect=zoom center=auto end=115 time=200')])
        b9.setAnimations([('focus','effect=zoom center=auto end=115 time=200')])
        b10.setAnimations([('focus','effect=zoom center=auto end=115 time=200')])
        b11.setAnimations([('focus','effect=zoom center=auto end=115 time=200')])
        b12.setAnimations([('focus','effect=zoom center=auto end=115 time=200')])
        b13.setAnimations([('focus','effect=zoom center=auto end=115 time=200')])
        b14.setAnimations([('focus','effect=zoom center=auto end=115 time=200')])
        b15.setAnimations([('focus','effect=zoom center=auto end=115 time=200')])
        b16.setAnimations([('focus','effect=zoom center=auto end=115 time=200')])
        b17.setAnimations([('focus','effect=zoom center=auto end=115 time=200')])
        b18.setAnimations([('focus','effect=zoom center=auto end=115 time=200')])
        b19.setAnimations([('focus','effect=zoom center=auto end=115 time=200')])
        b20.setAnimations([('focus','effect=zoom center=auto end=115 time=200')])

        m1=self.getControl(32101)
        m1.controlDown(b0)
        m2=self.getControl(32102)
        m2.controlDown(b0)
        m3=self.getControl(32103)
        m3.controlDown(b0)
        m4=self.getControl(32104)
        m4.controlDown(b0)
        prev=self.getControl(32116)
        next=self.getControl(32117)
        prev.controlUp(b19)
        prev.controlDown(m1)
        prev.controlRight(next)
        next.controlUp(b19)
        next.controlDown(m1)
        next.controlLeft(prev)
        #Row 1
        b0.controlRight(b1)
        b0.controlLeft(b0)
        b0.controlDown(b7)
        b0.controlUp(m1)

        b1.controlRight(b2)
        b1.controlLeft(b0)
        b1.controlDown(b8)
        b1.controlUp(m1)

        b2.controlRight(b3)
        b2.controlLeft(b1)
        b2.controlDown(b9)
        b2.controlUp(m1)

        b3.controlRight(b4)
        b3.controlLeft(b2)
        b3.controlDown(b10)
        b3.controlUp(m1)

        b4.controlRight(b5)
        b4.controlLeft(b3)
        b4.controlDown(b11)
        b4.controlUp(m1)

        b5.controlRight(b6)
        b5.controlLeft(b4)
        b5.controlDown(b12)
        b5.controlUp(m1)

        b6.controlRight(b7)
        b6.controlLeft(b5)
        b6.controlDown(b13)
        b6.controlUp(m1)
        #row 2
        b7.controlRight(b8)
        b7.controlLeft(b6)
        b7.controlDown(b14)
        b7.controlUp(b0)

        b8.controlRight(b9)
        b8.controlLeft(b7)
        b8.controlDown(b15)
        b8.controlUp(b1)

        b9.controlRight(b10)
        b9.controlLeft(b8)
        b9.controlDown(b16)
        b9.controlUp(b2)

        b10.controlRight(b11)
        b10.controlLeft(b9)
        b10.controlDown(b17)
        b10.controlUp(b3)

        b11.controlRight(b12)
        b11.controlLeft(b10)
        b11.controlDown(b18)
        b11.controlUp(b4)

        b12.controlRight(b13)
        b12.controlLeft(b11)
        b12.controlDown(b19)
        b12.controlUp(b5)

        b13.controlRight(b14)
        b13.controlLeft(b12)
        b13.controlDown(b20)
        b13.controlUp(b6)
        #row 3
        b14.controlRight(b15)
        b14.controlLeft(b13)
        b14.controlDown(b1)
        b14.controlUp(b7)

        b15.controlRight(b16)
        b15.controlLeft(b14)
        b15.controlDown(b2)
        b15.controlUp(b8)

        b16.controlRight(b17)
        b16.controlLeft(b15)
        b16.controlDown(b3)
        b16.controlUp(b9)

        b17.controlRight(b18)
        b17.controlLeft(b16)
        b17.controlDown(b4)
        b17.controlUp(b10)

        b18.controlRight(b19)
        b18.controlLeft(b17)
        b18.controlDown(b5)
        b18.controlUp(b11)

        b19.controlRight(b20)
        b19.controlLeft(b18)
        b19.controlDown(next)
        b19.controlUp(b12)

        b20.controlRight(b0)
        b20.controlLeft(b19)
        b20.controlDown(next)
        b20.controlUp(b12)

        if source=='popular':self.getControl(32111).setLabel('Popular Movies')
        if source=='top_rated':self.getControl(32111).setLabel('Top Rated Movies')
        if source=='upcoming':self.getControl(32111).setLabel('Upcoming Movies')
        if source=='now_playing':self.getControl(32111).setLabel('Now Playing Movies')
        if source=='query':self.getControl(32111).setLabel('Search Results')
        if source=='favorites':self.getControl(32111).setLabel('Favorite Movies')
        if source=='watchlist':self.getControl(32111).setLabel('Movies on Watchlist')
        if source=='rated':self.getControl(32111).setLabel('Rated Movies')

        self.setFocus(b0)

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
            title=self.getControl(3022)
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
            title.setLabel(movie['title'] + ' ('+ movie['release_date'][:4] +')')
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
        query_btn = 32110
        previous = 32116
        next =32117
        tv_shows = 32114
        people = 32115

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
        if control == watchlist:
            do_movies=True
            source = 'watchlist'
        if control == rated:
            do_movies=True
            source = 'rated'
        if control == query_btn:
            source='query'
            do_movies=True
            page=1
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
        if control==3001:movieid=self.movies[0]['id']
        if control==3002:movieid=self.movies[1]['id']
        if control==3003:movieid=self.movies[2]['id']
        if control==3004:movieid=self.movies[3]['id']
        if control==3005:movieid=self.movies[4]['id']
        if control==3006:movieid=self.movies[5]['id']
        if control==3007:movieid=self.movies[6]['id']
        if control==3008:movieid=self.movies[7]['id']
        if control==3009:movieid=self.movies[8]['id']
        if control==3010:movieid=self.movies[9]['id']
        if control==3011:movieid=self.movies[10]['id']
        if control==3012:movieid=self.movies[11]['id']
        if control==3013:movieid=self.movies[12]['id']
        if control==3014:movieid=self.movies[13]['id']
        if control==3015:movieid=self.movies[14]['id']
        if control==3016:movieid=self.movies[15]['id']
        if control==3017:movieid=self.movies[16]['id']
        if control==3018:movieid=self.movies[17]['id']
        if control==3019:movieid=self.movies[18]['id']
        if control==3020:movieid=self.movies[19]['id']
        if control==3021:movieid=self.movies[20]['id']
        return movieid