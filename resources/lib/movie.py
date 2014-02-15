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
movie_id=0
movie=''
keyword_id=''
genre_id=''
current_keyword=''
current_genre=''
cast_member=''
cast_member_id=''
def startup():
    movie=tmdb.get_movie(movie_id)
    show_movie(movie)

def show_movie(movie):
    movie_window = movieWindow('script-movieDetailWindow.xml', addon_path,'default')
    movie_window.doModal()
    
class movieWindow(xbmcgui.WindowXMLDialog):  
    posters=[]
    poster_index=0
    backgrounds=[]
    similar=[]
    cast_movies=[]
    keywords=[]
    cast=[]
    genres=[]
    background_index=0
    mode='similar'
    file=''
    current_movie=''
    session_id=''
    def onInit(self):
        self.session_id=addon.getSetting('session_id')
        you_tube_base_url='plugin://plugin.video.youtube/?action=play_video&videoid='
        self.posters=[]
        str_similar=tmdb.get_similar_movies(movie_id,1)
        similar=str_similar['results']
        plot=self.getControl(103)
        tagline=self.getControl(108)
        runtime=self.getControl(109)
        title=xbmcgui.ControlButton(20,5,800,30,'','','',0,0,0,title_font,'ff606060','',0,'','ff606060')
        title=self.addControl(title)
        title=self.getControl(3001)
        movie=tmdb.get_movie(movie_id)
        self.current_movie=movie
        self.file=utils.find_xbmc_by_title(movie['title'],movie['release_date'][:4])
        if self.file!='':
            self.getControl(127).setLabel('Play')
        crew = movie['credits']['crew']
        cast = movie['credits']['cast']
        self.cast= sorted(cast, key=lambda k: k['order'])
        director=''
        writer=''
        genres=''
        for crew_member in crew:
            if crew_member['job'] =='Director':
                director=director+ crew_member['name'] + ", "
            if crew_member['department'] == 'Writing':
                writer=writer + crew_member['name'] + ", "
        director=director[:-2]
        writer=writer[:-2]
        studio=''
        for company in movie['production_companies']:
            studio=studio+company['name'] + ", "
        studio=studio[:-2]
        for genre in movie['genres']:
            genres=genres + genre['name'] + ' / '
        genres=genres[:-3]
        mpaa=''
        for release in movie['releases']['countries']:
            if release['iso_3166_1'] =='US':
                mpaa=release['certification']
        self.getControl(110).setLabel(director)
        self.getControl(112).setLabel(studio)
        self.getControl(113).setLabel(genres)
        self.getControl(114).setLabel(mpaa)
        self.getControl(115).setLabel(movie['status'])
        self.getControl(116).setLabel(utils.format_currency(movie['budget']))
        self.getControl(117).setLabel(utils.format_currency(movie['revenue']))
        self.getControl(118).setLabel(utils.format_date(movie['release_date']))
        self.getControl(111).setLabel(writer)
        title.setLabel(movie['title'])
        runtime.setLabel(str(movie['runtime']) +' min')
        tagline.setLabel(movie['tagline'])
        plot.setText(movie['overview'])
        self.getControl(102).setImage('')
        self.backgrounds=[]
        self.posters=[]
        if movie['poster_path']!=None:
            self.posters.append(movie['poster_path'])
        if movie['images']['posters']>0:
            for poster in movie['images']['posters']:
                if poster['iso_639_1']=='en':
                    if poster['file_path'] not in self.posters:
                        self.posters.append(poster['file_path'])
        xbmc.log('number of posters = ' + str(len(self.posters)))
        if len(self.posters) > 0:
            self.getControl(102).setImage('')
            self.getControl(101).setLabel('Loading')
            self.getControl(102).setImage('http://image.tmdb.org/t/p/w300' +self.posters[0])
        else:
            self.getControl(101).setLabel('')
        if movie['backdrop_path']!=None:
            self.backgrounds.append(movie['backdrop_path'])
        if movie['images']['backdrops']>0:
            for background in movie['images']['backdrops']:
                if background['file_path'] not in self.backgrounds:
                        self.backgrounds.append(background['file_path'])
        xbmc.log('number of backgrounds = ' + str(len(self.backgrounds)))
        if len(self.backgrounds) > 0:
            self.getControl(402).setImage('')
            self.getControl(401).setLabel('Loading')
            self.getControl(402).setImage('http://image.tmdb.org/t/p/w300' +self.backgrounds[0])
        else:
            self.getControl(401).setLabel('')
        self.getControl(107).setLabel('1 of ' + str(len(self.posters)))
        self.getControl(407).setLabel('1 of ' + str(len(self.backgrounds)))
        self.show_similar(similar)
        star=round(movie['vote_average'],2)
        if star >= .5: self.getControl(1001).setImage('half-star-icon-enable.png')
        if star >= 1: self.getControl(1001).setImage('star-icon-enable.png')
        if star >= 1.5: self.getControl(1002).setImage('half-star-icon-enable.png')
        if star >= 1: self.getControl(1002).setImage('star-icon-enable.png')
        if star >= 2.5: self.getControl(1003).setImage('half-star-icon-enable.png')
        if star >= 3: self.getControl(1003).setImage('star-icon-enable.png')
        if star >= 3.5: self.getControl(1004).setImage('half-star-icon-enable.png')
        if star >= 4: self.getControl(1004).setImage('star-icon-enable.png')
        if star >=4.5: self.getControl(1005).setImage('half-star-icon-enable.png')
        if star >= 5: self.getControl(1005).setImage('star-icon-enable.png')
        if star >= 5.5: self.getControl(1006).setImage('half-star-icon-enable.png')
        if star >= 6: self.getControl(1006).setImage('star-icon-enable.png')
        if star >= 6.5: self.getControl(1007).setImage('half-star-icon-enable.png')
        if star >= 7: self.getControl(1007).setImage('star-icon-enable.png')
        if star >= 7.5: self.getControl(1008).setImage('half-star-icon-enable.png')
        if star >= 8: self.getControl(1008).setImage('star-icon-enable.png')
        if star >= 8.5: self.getControl(1009).setImage('half-star-icon-enable.png')
        if star >= 9: self.getControl(1009).setImage('star-icon-enable.png')
        if star >= 9.5: self.getControl(1010).setImage('half-star-icon-enable.png')
        if star >= 10: self.getControl(1010).setImage('star-icon-enable.png')
        if self.session_id!='':
            states=tmdb.get_movie_account_states(movie_id,self.session_id)
            if states['favorite']:self.getControl(4011).setImage('favorite-enable.png')
            if states['watchlist']:self.getControl(5011).setImage('popcorn-enable.png')
            if states['rated']:
                self.getControl(131).setLabel(str(star)+'/10 (' + str(movie['vote_count']) + ' votes, you voted '+ str(states['rated']['value']) +')')
            else:
                self.getControl(131).setLabel(str(star)+'/10 (' + str(movie['vote_count']) + ' votes)')
        else:
            self.getControl(131).setLabel(str(star)+'/10 (' + str(movie['vote_count']) + ' votes)')

    def show_similar(self,similar):
        self.getControl(128).setLabel('Movies Similar to ' + self.current_movie['title'])
        x=10
        for i in range(0,x):
            self.getControl(300+i).setImage('')
            self.getControl(200+i).setLabel(' ')
            self.getControl(200+i).setEnabled(False)
        if len(similar) < 10:x=len(similar)
        for i in range(0,x):
            self.getControl(200+i).setEnabled(True)
            if similar[i]['poster_path']==None:
                self.getControl(300+i).setImage('no-poster-w92.jpg')
                self.getControl(200+i).setLabel(similar[i]['title'])
            else:
                self.getControl(300+i).setImage('http://image.tmdb.org/t/p/w92' + similar[i]['poster_path'])
        self.similar=similar

    def show_cast_movies(self,cast_movies):
        global cast_member
        global cast_member_id
        self.getControl(128).setLabel('Movies with ' + cast_member + ' in the Cast')
        x=10
        for i in range(0,x):
            self.getControl(300+i).setImage('')
            self.getControl(200+i).setLabel(' ')
            self.getControl(200+i).setEnabled(False)
        if len(cast_movies) < 10:x=len(cast_movies)
        for i in range(0,x):
            self.getControl(200+i).setEnabled(True)
            if cast_movies[i]['poster_path']==None:
                self.getControl(300+i).setImage('no-poster-w92.jpg')
                self.getControl(200+i).setLabel(cast_movies[i]['title'])
            else:
                self.getControl(300+i).setImage('http://image.tmdb.org/t/p/w92' + cast_movies[i]['poster_path'])
        self.cast_movies=cast_movies

    def show_cast(self,cast):
        self.getControl(128).setLabel('Cast From '+ self.current_movie['title'])
        x=10
        for i in range(0,x):
            self.getControl(300+i).setImage('')
            self.getControl(200+i).setLabel(' ')
            self.getControl(200+i).setEnabled(False)
        if len(cast) <10:x=len(cast)
        for i in range(0,x):
            self.getControl(200+i).setEnabled(True)
            if cast[i]['profile_path']==None:
                self.getControl(300+i).setImage('no-profile-w92.jpg')
                self.getControl(200+i).setLabel(cast[i]['name'])
            else:
                self.getControl(300+i).setImage('http://image.tmdb.org/t/p/w92' + cast[i]['profile_path'])
        self.cast=cast

    def show_keywords(self,keywords):
        global current_keyword
        self.getControl(128).setLabel('Movies with ' + current_keyword + ' Keyword')
        x=10
        for i in range(0,x):
            self.getControl(300+i).setImage('')
            self.getControl(200+i).setLabel(' ')
            self.getControl(200+i).setEnabled(False)
        if len(keywords) < 10:x=len(keywords)
        for i in range(0,x):
            self.getControl(200+i).setEnabled(True)
            if keywords[i]['poster_path']==None:
                self.getControl(300+i).setImage('no-poster-w92.jpg')
                self.getControl(200+i).setLabel(keywords[i]['title'])
            else:
                self.getControl(300+i).setImage('http://image.tmdb.org/t/p/w92' + keywords[i]['poster_path'])
        self.keywords=keywords

    def show_genre(self,genres):
        global current_genre
        self.getControl(128).setLabel(current_genre + ' Movies')
        x=10
        for i in range(0,x):
            self.getControl(300+i).setImage('')
            self.getControl(200+i).setLabel(' ')
            self.getControl(200+i).setEnabled(False)
        if len(genres) < 10:x=len(genres)
        for i in range(0,x):
            self.getControl(200+i).setEnabled(True)
            if genres[i]['poster_path']==None:
                self.getControl(300+i).setImage('no-poster-w92.jpg')
                self.getControl(200+i).setLabel(genres[i]['title'])
            else:
                self.getControl(300+i).setImage('http://image.tmdb.org/t/p/w92' + genres[i]['poster_path'])
        self.genres=genres

    def onFocus(self, control):
        xbmc.log('Focus='+str(control))
        if control in(200,201,202,203,204,205,206,207,208,209):
            if self.mode =='similar':
                self.getControl(126).setLabel(self.similar[control-200]['title'])
            elif self.mode=='keywords':
                self.getControl(126).setLabel(self.keywords[control-200]['title'])
            elif self.mode=='cast':
                self.getControl(126).setLabel(self.cast[control-200]['name'] + ' as ' + self.cast[control-200]['character'])
            elif self.mode=='cast_movies':
                self.getControl(126).setLabel(self.cast_movies[control-200]['title'])
        else:
            self.getControl(126).setLabel('')

    def onAction(self, action):
        if action == 10:
            d = xbmcgui.Dialog()
            ans=d.yesno('tmdb Browser','Exit themoviedb.org Browser?')
            if ans:
                xbmc.executebuiltin('Dialog.Close(all,true)')
        elif action == 92:
            self.close()

    def onClick(self,control):
        xbmc.log('you clicked '+ str(control))
        global movie_id
        global movie
        global cast_member
        global cast_member_id
        global genre_id
        global current_genre
        global keyword_id
        global current_keyword
        if control in(200,201,202,203,204,205,206,207,208,209):
            if self.mode=='similar':
                movie_id=self.similar[control-200]['id']
                startup()  
            elif self.mode=='cast':
               cast_member=self.cast[control-200]['name']
               cast_member_id=self.cast[control-200]['id']
               self.cast_movies=tmdb.getMoviesByActor(self.cast[control-200]['id'],1)
               self.mode='cast_movies'
               self.show_cast_movies(self.cast_movies)
            elif self.mode=='keywords':
               movie_id=self.keywords[control-200]['id']
               startup()  
            elif self.mode=='genre':  
                movie_id=self.genres[control-200]['id']
                startup()
            elif self.mode=='cast_movies':
                movie_id=self.cast_movies[control-200]['id']
                startup()

        if control in (50,51,52):
            dg = dialogWindow('dialog_select.xml',addon_path,'default')
            dg.curr_movie=self.current_movie
            if control==50:dg.mode='trailer'
            if control==51:dg.mode='keyword'
            if control==52:dg.mode='genre'
            dg.doModal()
            if control==51:
                if keyword_id!='':
                    self.mode='keywords'
                    self.keywords=tmdb.getMoviesByKeyword(keyword_id,1)
                    self.show_keywords(self.keywords)
            elif control==52:
                if genre_id!='':
                    self.mode='genre'
                    self.genres=tmdb.get_movies_by_genre(genre_id,1)['results']
                    self.show_genre(self.genres)
                                  
        if control == 105 or control == 106:
            if control==105:
                if self.poster_index==0:
                    self.poster_index=len(self.posters)-1
                else:
                    self.poster_index=self.poster_index-1
            if control==106:
                if self.poster_index==len(self.posters)-1:
                    self.poster_index=0
                else:
                    self.poster_index=self.poster_index+1
            self.getControl(102).setImage('')
            self.getControl(107).setLabel(str(self.poster_index+1) + ' of ' + str(len(self.posters)))
            self.getControl(101).setLabel('Loading')
            self.getControl(102).setImage('http://image.tmdb.org/t/p/w300' +self.posters[self.poster_index])

        if control == 122:
            self.getControl(126).setLabel('')
            self.mode='similar'
            str_similar=tmdb.get_similar_movies(self.current_movie['id'],1)
            self.similar=str_similar['results']
            self.show_similar(self.similar)

        if control == 124:
            self.getControl(126).setLabel('')
            self.mode = 'cast'
            self.show_cast(self.cast)
                
        if control ==127:
            if self.getControl(127).getLabel()=='Play':
                xbmc.Player().play(self.file)
                xbmc.executebuiltin('Dialog.Close(all,true)')
            else:
                xbmc.executebuiltin("XBMC.RunPlugin('plugin://plugin.video.couchpotato_manager/movies/add?title='" + self.current_movie['title']+ "')'")
        if control == 405 or control == 406:
            if control==405:
                if self.background_index==0:
                    self.background_index=len(self.backgrounds)-1
                else:
                    self.background_index=self.background_index-1
            if control==406 :
                if self.background_index==len(self.backgrounds)-1:
                    self.background_index=0
                else:
                    self.background_index=self.background_index+1

            self.getControl(402).setImage('')
            self.getControl(407).setLabel(str(self.background_index+1) + ' of ' + str(len(self.backgrounds)))
            self.getControl(401).setLabel('Loading')
            self.getControl(402).setImage('http://image.tmdb.org/t/p/w300' +self.backgrounds[self.background_index])


        if control==104:
            iw = imageWindow('image.xml', addon_path,'default')
            iw.images=self.posters
            iw.image_index=self.poster_index
            iw.doModal()
            del iw

        if control==404:
            iw = imageWindow('image.xml', addon_path,'default')
            iw.images=self.backgrounds
            iw.image_index=self.background_index
            iw.doModal()
            del iw
        
        if control==132:
            rw =  ratingWindow('rating_dialog.xml',addon_path,'default')
            rw.curr_movie=self.current_movie
            rw.doModal()

        if control==4001: #Favorite
            if self.session_id=='':
                session_id=utils.get_login()
                if session_id!='':self.session_id=session_id
            if self.session_id!='':
                res=tmdb.update_favorite_movie(self.current_movie['id'],addon.getSetting('session_id'))
                if res['success']:
                    if res['update']:
                        dialog = xbmcgui.Dialog()
                        dialog.notification('themoviedb.org Browser', 'Successfully Added ' + self.current_movie['title'] + ' to Favorites')
                        self.getControl(4011).setImage('favorite-enable.png')
                    else:
                        dialog = xbmcgui.Dialog()
                        dialog.notification('themoviedb.org Browser', 'Successfully Removed ' + self.current_movie['title'] + ' from Favorites')
                        self.getControl(4011).setImage('favorite-disable.png')

        if control==5001: #Watchlist
            if self.session_id=='':
                session_id=utils.get_login()
                if session_id!='':self.session_id=session_id
            if self.session_id!='':
                res=tmdb.update_watchlist_movie(self.current_movie['id'],addon.getSetting('session_id'))
                if res['success']:
                    if res['update']:
                        dialog = xbmcgui.Dialog()
                        dialog.notification('themoviedb.org Browser', 'Successfully Added ' + self.current_movie['title'] + ' to Watchlist')
                        self.getControl(5011).setImage('popcorn-enable.png')
                    else:
                        dialog = xbmcgui.Dialog()
                        dialog.notification('themoviedb.org Browser', 'Successfully Removed ' + self.current_movie['title'] + ' from Watchlist')
                        self.getControl(5011).setImage('popcorn-disable.png')
        if control==5020: #Show All
            from resources.lib import movies
            if self.mode=='genre':
                movies.genre_id=genre_id
                movies.genre_name=current_genre
                movies.page=1
                movies.source='genre'
                movies.show_movies_by_genre(genre_id)             
            if self.mode=='similar':
                movies.similar_name=self.current_movie['title']
                movies.similar_id=self.current_movie['id']
                movies.page=1
                movies.source='similar'
                movies.show_similar_movies(self.current_movie['id'])
            if self.mode=='cast_movies':
                movies.person_id=cast_member_id
                movies.person_name=cast_member
                movies.page=1
                movies.source='person'
                movies.show_movies_by_person(cast_member_id)
                
                            

class ratingWindow(xbmcgui.WindowXMLDialog):
    curr_movie=''
    def onInit(self):
        self.getControl(1001).setLabel(self.curr_movie['title'])

    def onClick(self,control):
        session_id=addon.getSetting('session_id')
        #No session id lets rate movie as guest
        if session_id=='':
            session_id=addon.getSetting('guest_session_id')
            if session+id=='':session_id=tmdb.get_guest_session_id()
        value=self.getControl(1002).getLabel()
        res=tmdb.rate_movie(self.curr_movie['id'],value,session_id)
        if res:
            dialog = xbmcgui.Dialog()
            dialog.notification('themoviedb.org Browser', 'Successfully Rated '+self.curr_movie['title'], xbmcgui.NOTIFICATION_INFO, 5000)
            #if we rated movie as a guest lets save the guest session id to use later.
            if addon.getSetting('session_id')=='':addon.setSetting('guest_session_id',session_id)
        else:
            dialog = xbmcgui.Dialog()
            dialog.notification('themoviedb.org Browser', 'Failed to Rated '+self.curr_movie['title'], xbmcgui.NOTIFICATION_ERROR, 5000)
        self.close()

    def onFocus(self,control):
        if control==1005:self.getControl(1002).setLabel('.5')
        if control==1010:self.getControl(1002).setLabel('1')
        if control==1015:self.getControl(1002).setLabel('1.5')
        if control==1020:self.getControl(1002).setLabel('2')
        if control==1025:self.getControl(1002).setLabel('2.5')
        if control==1030:self.getControl(1002).setLabel('3')
        if control==1035:self.getControl(1002).setLabel('3.5')
        if control==1040:self.getControl(1002).setLabel('4')
        if control==1045:self.getControl(1002).setLabel('4.5')
        if control==1050:self.getControl(1002).setLabel('5')
        if control==1055:self.getControl(1002).setLabel('5.5')
        if control==1060:self.getControl(1002).setLabel('6')
        if control==1065:self.getControl(1002).setLabel('6.5')
        if control==1070:self.getControl(1002).setLabel('7')
        if control==1075:self.getControl(1002).setLabel('7.5')
        if control==1080:self.getControl(1002).setLabel('8')
        if control==1085:self.getControl(1002).setLabel('8.5')
        if control==1090:self.getControl(1002).setLabel('9')
        if control==1095:self.getControl(1002).setLabel('9.5')
        if control==1100:self.getControl(1002).setLabel('10')

class dialogWindow(xbmcgui.WindowXMLDialog):
    curr_movie=''
    mode=''
    def onInit(self):
        if self.mode=='trailer':
            self.getControl(1).setLabel('Trailers')
            for trailer in self.curr_movie['trailers']['youtube']:
               li=xbmcgui.ListItem(trailer['name'])
               li.setProperty('url','plugin://plugin.video.youtube/?action=play_video&videoid='+trailer['source'])
               self.getControl(300).addItem(li)
        elif self.mode=='keyword':
            self.getControl(1).setLabel('Serch for Movies by Keywords')
            for keyword in self.curr_movie['keywords']['keywords']:
                li=xbmcgui.ListItem(keyword['name'])
                li.setProperty('id',str(keyword['id']))
                self.getControl(300).addItem(li)
        elif self.mode=='genre':
            self.getControl(1).setLabel('Search for Movies by Genre')
            for genre in self.curr_movie['genres']:
                li=xbmcgui.ListItem(genre['name'])
                li.setProperty('id',str(genre['id']))
                self.getControl(300).addItem(li)

    def onClick(self,control):
        global keyword_id
        global genre_id
        global current_genre
        global current_keyword
        if control==300:
            if self.mode=='trailer':
                li= self.getControl(300).getSelectedItem()
                vw=videoWindow('script-videoPlayerWindow.xml',addon_path,'Default')
                vw.url=li.getProperty('url')
                vw.doModal()
            elif self.mode=='keyword':
                li=self.getControl(300).getSelectedItem()
                keyword_id=li.getProperty('id')
                current_keyword=li.getLabel()
                self.close()
            elif self.mode=='genre':
                li=self.getControl(300).getSelectedItem()
                genre_id=li.getProperty('id')
                current_genre=li.getLabel()
                self.close()

class videoWindow(xbmcgui.WindowXMLDialog):
    url=''
    def onInit(self):
        xbmc.Player().play(self.url)
        while xbmc.Player().isPlaying():
            xbmc.sleep(250)
        self.close()

class imageWindow(xbmcgui.WindowXMLDialog):
    images=[]
    image_index=0
    def onInit(self):
        self.getControl(100).setImage('http://image.tmdb.org/t/p/original' + self.images[self.image_index])      
