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
    cast_movies=[]
    mode='movies'
    total_results=0
    current_person=''
    def onInit(self):
        self.posters=[]
        self.getControl(129).setVisible(False)
        self.getControl(5020).setVisible(False)
        person=tmdb.get_person(person_id)
        if use_chrome=='true' and person['homepage']!='':self.getControl(129).setVisible(True)
        bio=self.getControl(103)
        title=xbmcgui.ControlButton(60,5,800,30,'','','',0,0,0,title_font,'ff606060','',0,'','ff606060')
        title=self.addControl(title)
        title=self.getControl(3001)
        title.setAnimations([('windowclose', 'effect=fade end=0 time=0',)])
        self.current_person=person
        movie_crew = person['movie_credits']['crew']
        movie_cast = person['movie_credits']['cast']
        tv_crew = person['movie_credits']['crew']
        tv_cast = person['movie_credits']['cast']
        bio.setText(person['biography'])
        title.setLabel(person['name'])
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

    def show_person_movies(self,person):
        movies=person['movie_credits']['cast']
        self.getControl(5020).setVisible(True)
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
