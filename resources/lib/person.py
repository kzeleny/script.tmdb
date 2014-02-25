import xbmcgui
import xbmc
import xbmcaddon
import os
import urllib
from resources.lib import utils
from resources.lib import tmdb

addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path')
resources_path = xbmc.translatePath( os.path.join( addon_path, 'resources' ) ).decode('utf-8')
use_chrome=addon.getSetting('chrome')
title_font=utils.getTitleFont()
image_base_url=tmdb.get_image_base_url()

person_id=''
person=''

def startup():
    person=tmdb.get_person(person_id)
    show_person(person)

def show_person(person):
    person_window = personWindow('script-personDetailWindow.xml', addon_path,'default')
    person_window.doModal()
    
class personWindow(xbmcgui.WindowXMLDialog): 
    posters=[]
    poster_index=0
    movie_cast=[]
    movie_crew=[]
    tv_cast=[]
    tv_crew=[]
    movie_direction=[]
    movie_production=[]
    movie_writing=[]
    tv_direction=[]
    tv_production=[]
    tv_writing=[]
    mode='actor_movies'
    total_results=0
    current_person=''
    def onInit(self):
        self.posters=[]
        self.getControl(129).setVisible(False)
        self.getControl(5020).setVisible(False)
        self.getControl(116).setSelected(True)
        person=tmdb.get_person(person_id)
        self.current_person=person
        if use_chrome=='true' and person['homepage']!='':self.getControl(129).setVisible(True)
        bio=self.getControl(103)
        title=xbmcgui.ControlButton(220,15,800,30,'','','',0,0,0,title_font,'ff606060','',0,'','ff606060')
        title=self.addControl(title)
        title=self.getControl(3001)
        title.setAnimations([('windowclose', 'effect=fade end=0 time=0',)])
        birthday=self.getControl(111)
        credits=self.getControl(110)
        birthplace=self.getControl(112)
        self.current_person=person
        self.movie_crew = person['movie_credits']['crew']
        self.movie_cast = person['movie_credits']['cast']
        self.tv_crew = person['tv_credits']['crew']
        self.tv_cast = person['tv_credits']['cast']
        bio.setText(person['biography'])
        title.setLabel(person['name'])
        birthday.setLabel(person['birthday'])
        birthplace.setLabel(person['place_of_birth'])
        credits.setLabel('Movie: ' + str(len(self.movie_cast)) + ' TV: ' + str(len(self.tv_cast)))
        self.movie_direction=[]
        self.movie_production=[]
        self.movie_writing=[]
        self.tv_direction=[]
        self.tv_production=[]
        self.tv_writing=[]
        for crew in self.movie_crew:
            if crew['department']=='Production':self.movie_production.append(crew)
            if crew['department']=='Writing':self.movie_writing.append(crew)
            if crew['department']=='Directing':self.movie_direction.append(crew)
        for crew in self.tv_crew:
            if crew['department']=='Production':self.tv_production.append(crew)
            if crew['department']=='Writing':self.tv_writing.append(crew)
            if crew['department']=='Directing':self.tv_direction.append(crew)

        if len(self.movie_cast)>0:
            li=xbmcgui.ListItem('Actor ('+ str(len(self.movie_cast))+')')
            self.getControl(115).addItem(li)
        if len(self.movie_direction) > 0:
            li=xbmcgui.ListItem('Director (' + str(len(self.movie_direction)) +')')
            self.getControl(115).addItem(li)
        if len(self.movie_production) > 0:
            li=xbmcgui.ListItem('Producer (' + str(len(self.movie_production)) +')')
            self.getControl(115).addItem(li)
        if len(self.movie_writing) > 0:
            li=xbmcgui.ListItem('Writer (' + str(len(self.movie_writing)) +')')
            self.getControl(115).addItem(li)
                
        for image in person['images']['profiles']:
            self.posters.append(image['file_path'])
        if len(self.posters) > 0:
            self.getControl(102).setImage('')
            self.getControl(101).setLabel('Loading')
            self.getControl(102).setImage('http://image.tmdb.org/t/p/original' +self.posters[0])
            self.getControl(901).setImage('http://image.tmdb.org/t/p/original' +self.posters[0])
        else:
            self.getControl(101).setLabel('')
        self.getControl(107).setLabel('1 of ' + str(len(self.posters)))
        self.show_person_movies(person)
        self.onFocus(200)
    def onClick(self,control):
        if control == 115: 
            li=xbmcgui.ListItem
            li=self.getControl(115).getSelectedItem()
            label=li.getLabel()
            if self.getControl(116).isSelected()==True:
                mode='movies'
            else:
                mode='tv'
            if 'Actor' in label:
                self.mode='actor_'+ mode
                if mode=='movies':
                    self.show_person_movies(self.current_person)
                else:
                    self.show_person_tv(self.current_person)
            if 'Director' in label:
                self.mode='director_'+ mode
                if mode=='movies':
                    self.show_director_movies(self.current_person)
                else:
                    self.show_director_tv(self.current_person)
            if 'Producer' in label:
                self.mode='producer_'+ mode
                if mode=='movies':
                    self.show_producer_movies(self.current_person)
                else:
                    self.show_producer_tv(self.current_person)
            if 'Writer' in label:
                self.mode='writer_'+ mode
                if mode=='movies':
                    self.show_writer_movies(self.current_person)
                else:
                    self.show_writer_tv(self.current_person)

        if control in(200,201,202,203,204,205,206,207,208,209):
            movie_id=''
            tv_id=''
            if self.mode=='actor_movies':movie_id=self.movie_cast[control-200]['id']
            if self.mode=='director_movies':movie_id=self.movie_direction[control-200]['id']
            if self.mode=='producer_movies':movie_id=self.movie_production[control-200]['id']
            if self.mode=='writer_movies':movie_id=self.movie_writing[control-200]['id']
            if movie_id!='':
                from resources.lib import movie
                movie.movie_id=movie_id
                movie_window = movie.movieWindow('script-movieDetailWindow.xml', addon_path,'default')
                movie_window.doModal()
                del movie_window
        if control==116:
            self.mode='actor_movies'
            self.getControl(117).setSelected(False)
            self.getControl(116).setSelected(True)
            self.update_mode()
        if control==117:
            self.mode='actor_tv'
            self.getControl(117).setSelected(True)
            self.getControl(116).setSelected(False)
            self.update_mode()
        if control==104:
            iw = imageWindow('image.xml', addon_path,'default')
            iw.images=self.posters
            iw.image_index=self.poster_index
            iw.doModal()
            del iw

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
            self.getControl(102).setImage('http://image.tmdb.org/t/p/original' +self.posters[self.poster_index])
            self.getControl(901).setImage('http://image.tmdb.org/t/p/original' +self.posters[self.poster_index])

    def onFocus(self, control):
        if control in(200,201,202,203,204,205,206,207,208,209):
            movies=[]
            if self.mode=='actor_movies':movies=self.movie_cast
            if self.mode=='actor_tv':movies=self.tv_cast
            if self.mode=='director_movies':movies=self.movie_direction
            if self.mode=='director_tv':movies=self.tv_direction
            if self.mode=='producer_movies':movies=self.movie_production
            if self.mode=='producer_tv':movies=self.tv_production
            if self.mode=='writer_movies':movies=self.movie_writing
            if self.mode=='writer_tv':movies=self.tv_writing
            if 'actor_tv' == self.mode:
                if movies[control-200]['character']=='':
                    self.getControl(126).setLabel('[B]'+movies[control-200]['name'] +'[/B]')
                else:
                    self.getControl(126).setLabel('[B]'+movies[control-200]['name'] + ' as ' + movies[control-200]['character'] +'[/B]')
            elif 'actor_movies' == self.mode:
                if movies[control-200]['character']=='':
                    self.getControl(126).setLabel('[B]'+movies[control-200]['name'] +'[/B]')
                else:
                    self.getControl(126).setLabel('[B]'+movies[control-200]['title'] + ' as ' + movies[control-200]['character']+'[/B]')
            elif 'tv' in self.mode:
                self.getControl(126).setLabel('[B]'+movies[control-200]['name'] +'[/B]')
            elif 'movies' in self.mode:
                self.getControl(126).setLabel('[B]'+movies[control-200]['title'] +'[/B]')
        else:
            self.getControl(126).setLabel('')

    def update_mode(self):
        self.getControl(115).reset()
        if self.mode=='actor_movies':
            if len(self.movie_cast)>0:
                li=xbmcgui.ListItem('Actor ('+ str(len(self.movie_cast))+')')
                self.getControl(115).addItem(li)
            if len(self.movie_direction) > 0:
                li=xbmcgui.ListItem('Director (' + str(len(self.movie_direction)) +')')
                self.getControl(115).addItem(li)
            if len(self.movie_production) > 0:
                li=xbmcgui.ListItem('Producer (' + str(len(self.movie_production)) +')')
                self.getControl(115).addItem(li)
            if len(self.movie_writing) > 0:
                li=xbmcgui.ListItem('Writer (' + str(len(self.movie_writing)) +')')
                self.getControl(115).addItem(li)
            self.show_person_movies(self.current_person)
        if self.mode=='actor_tv':
            if len(self.tv_cast)>0:
                li=xbmcgui.ListItem('Actor ('+ str(len(self.tv_cast))+')')
                self.getControl(115).addItem(li)
            if len(self.tv_direction) > 0:
                li=xbmcgui.ListItem('Director (' + str(len(self.tv_direction)) +')')
                self.getControl(115).addItem(li)
            if len(self.tv_production) > 0:
                li=xbmcgui.ListItem('Producer (' + str(len(self.tv_production)) +')')
                self.getControl(115).addItem(li)
            if len(self.tv_writing) > 0:
                li=xbmcgui.ListItem('Writer (' + str(len(self.tv_writing)) +')')
                self.getControl(115).addItem(li)
            self.show_person_tv(self.current_person)

    def show_person_movies(self,person):
        movies=person['movie_credits']['cast']
        self.getControl(5020).setVisible(True)
        self.getControl(128).setLabel('Top 10 of '+ str(len(movies)) + ' Movies with ' + person['name'] + ' in the Cast')
        if len(movies) < 10:
            self.getControl(128).setLabel('Top '+str(len(movies)) +' of '+ str(len(movies)) + ' Movies with ' + person['name'] + ' in the Cast')
        else:
            self.getControl(128).setLabel('Top 10 of '+ str(len(movies)) + ' Movies with ' + person['name'] + ' in the Cast')
        x=10
        for i in range(0,x):
            self.getControl(300+i).setImage('')
            self.getControl(200+i).setLabel(' ')
            self.getControl(200+i).setEnabled(False) 
        if len(movies) < 10:x=len(movies)
        for i in range(0,x):
            self.getControl(200+i).setEnabled(True)
            if movies[i]['poster_path']==None:
                self.getControl(300+i).setImage('no-poster-w92.jpg')
                self.getControl(200+i).setLabel(movies[i]['title'])
            else:
                self.getControl(300+i).setImage('http://image.tmdb.org/t/p/w92' + movies[i]['poster_path'])

    def show_director_movies(self,person):
        movies=self.movie_direction
        self.getControl(5020).setVisible(True)
        if len(movies) < 10:
            self.getControl(128).setLabel('Top '+str(len(movies)) +' of '+ str(len(movies)) + ' Movies Directed by ' + person['name'])
        else:
            self.getControl(128).setLabel('Top 10 of '+ str(len(movies)) + ' Movies Directed by ' + person['name'])
        x=10
        for i in range(0,x):
            self.getControl(300+i).setImage('')
            self.getControl(200+i).setLabel(' ')
            self.getControl(200+i).setEnabled(False)
        if len(movies) < 10:x=len(movies)
        for i in range(0,x):
            self.getControl(200+i).setEnabled(True)
            if movies[i]['poster_path']==None:
                self.getControl(300+i).setImage('no-poster-w92.jpg')
                self.getControl(200+i).setLabel(movies[i]['title'])
            else:
                self.getControl(300+i).setImage('http://image.tmdb.org/t/p/w92' + movies[i]['poster_path'])

    def show_producer_movies(self,person):
        movies=self.movie_production
        self.getControl(5020).setVisible(True)
        if len(movies) < 10:
            self.getControl(128).setLabel('Top '+str(len(movies)) +' of '+ str(len(movies)) + ' Movies Produced by ' + person['name'])
        else:
            self.getControl(128).setLabel('Top 10 of '+ str(len(movies)) + ' Movies Produced by ' + person['name'])
        x=10
        for i in range(0,x):
            self.getControl(300+i).setImage('')
            self.getControl(200+i).setLabel(' ')
            self.getControl(200+i).setEnabled(False)
        if len(movies) < 10:x=len(movies)
        for i in range(0,x):
            self.getControl(200+i).setEnabled(True)
            if movies[i]['poster_path']==None:
                self.getControl(300+i).setImage('no-poster-w92.jpg')
                self.getControl(200+i).setLabel(movies[i]['title'])
            else:
                self.getControl(300+i).setImage('http://image.tmdb.org/t/p/w92' + movies[i]['poster_path'])

    def show_writer_movies(self,person):
        movies=self.movie_writing
        self.getControl(5020).setVisible(True)
        if len(movies) < 10:
            self.getControl(128).setLabel('Top '+str(len(movies)) +' of '+ str(len(movies)) + ' Movies Written by ' + person['name'])
        else:
            self.getControl(128).setLabel('Top 10 of '+ str(len(movies)) + ' Movies Written by ' + person['name'])
        x=10
        for i in range(0,x):
            self.getControl(300+i).setImage('')
            self.getControl(200+i).setLabel(' ')
            self.getControl(200+i).setEnabled(False)
        if len(movies) < 10:x=len(movies)
        for i in range(0,x):
            self.getControl(200+i).setEnabled(True)
            if movies[i]['poster_path']==None:
                self.getControl(300+i).setImage('no-poster-w92.jpg')
                self.getControl(200+i).setLabel(movies[i]['title'])
            else:
                self.getControl(300+i).setImage('http://image.tmdb.org/t/p/w92' + movies[i]['poster_path'])

    def show_person_tv(self,person):
        shows=person['tv_credits']['cast']
        self.getControl(5020).setVisible(True)
        if len(shows) > 10:
            self.getControl(128).setLabel('Top 10 of '+ str(len(shows)) + ' TV Shows with ' + person['name'] + ' in the Cast')
        else:
            self.getControl(128).setLabel('Top ' + str(len(shows)) + ' of ' + str(len(shows)) + ' TV Shows with ' + person['name'] + ' in the Cast')
        x=10
        for i in range(0,x):
            self.getControl(300+i).setImage('')
            self.getControl(200+i).setLabel(' ')
            self.getControl(200+i).setEnabled(False)
        if len(shows) < 10:x=len(shows)
        for i in range(0,x):
            self.getControl(200+i).setEnabled(True)
            if shows[i]['poster_path']==None:
                self.getControl(300+i).setImage('no-poster-w92.jpg')
                self.getControl(200+i).setLabel(shows[i]['name'])
            else:
                self.getControl(300+i).setImage('http://image.tmdb.org/t/p/w92' + shows[i]['poster_path'])

    def show_director_tv(self,person):
        shows=self.tv_direction
        self.getControl(5020).setVisible(True)
        if len(shows) < 10:
            self.getControl(128).setLabel('Top '+str(len(shows)) +' of '+ str(len(shows)) + ' TV Shows Directed by ' + person['name'])
        else:
            self.getControl(128).setLabel('Top 10 of '+ str(len(shows)) + ' TV Shows Directed by ' + person['name'])
        x=10
        for i in range(0,x):
            self.getControl(300+i).setImage('')
            self.getControl(200+i).setLabel(' ')
            self.getControl(200+i).setEnabled(False)
        if len(shows) < 10:x=len(shows)
        for i in range(0,x):
            self.getControl(200+i).setEnabled(True)
            if shows[i]['poster_path']==None:
                self.getControl(300+i).setImage('no-poster-w92.jpg')
                self.getControl(200+i).setLabel(shows[i]['name'])
            else:
                self.getControl(300+i).setImage('http://image.tmdb.org/t/p/w92' + shows[i]['poster_path'])

    def show_producer_tv(self,person):
        shows=self.tv_production
        self.getControl(5020).setVisible(True)
        if len(shows) < 10:
            self.getControl(128).setLabel('Top '+str(len(shows)) +' of '+ str(len(shows)) + ' TV Shows Produced by ' + person['name'])
        else:
            self.getControl(128).setLabel('Top 10 of '+ str(len(shows)) + ' TV Shows Produced by ' + person['name'])
        x=10
        for i in range(0,x):
            self.getControl(300+i).setImage('')
            self.getControl(200+i).setLabel(' ')
            self.getControl(200+i).setEnabled(False)
        if len(shows) < 10:x=len(shows)
        for i in range(0,x):
            self.getControl(200+i).setEnabled(True)
            if shows[i]['poster_path']==None:
                self.getControl(300+i).setImage('no-poster-w92.jpg')
                self.getControl(200+i).setLabel(shows[i]['name'])
            else:
                self.getControl(300+i).setImage('http://image.tmdb.org/t/p/w92' + shows[i]['poster_path'])

    def show_writer_tv(self,person):
        shows=self.tv_writing
        self.getControl(5020).setVisible(True)
        if len(shows) < 10:
            self.getControl(128).setLabel('Top '+str(len(shows)) +' of '+ str(len(shows)) + ' TV Shows Written by ' + person['name'])
        else:
            self.getControl(128).setLabel('Top 10 of '+ str(len(shows)) + ' TV Shows Written by ' + person['name'])
        x=10
        for i in range(0,x):
            self.getControl(300+i).setImage('')
            self.getControl(200+i).setLabel(' ')
            self.getControl(200+i).setEnabled(False)
        if len(shows) < 10:x=len(shows)
        for i in range(0,x):
            self.getControl(200+i).setEnabled(True)
            if shows[i]['poster_path']==None:
                self.getControl(300+i).setImage('no-poster-w92.jpg')
                self.getControl(200+i).setLabel(shows[i]['name'])
            else:
                self.getControl(300+i).setImage('http://image.tmdb.org/t/p/w92' + shows[i]['poster_path'])

class imageWindow(xbmcgui.WindowXMLDialog):
    images=[]
    image_index=0
    def onInit(self):
        self.getControl(100).setImage('http://image.tmdb.org/t/p/original' + self.images[self.image_index])     