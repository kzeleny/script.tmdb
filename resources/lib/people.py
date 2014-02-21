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
no_profile_path = xbmc.translatePath( os.path.join( media_path, 'no-profile-w92.jpg' ) ).decode('utf-8')
title_font=utils.getTitleFont()
image_base_url=tmdb.get_image_base_url()
source='popular'
query=''
page=1
maxpage=10

def startup():
    people_results=tmdb.get_people(source,page)
    person_ids=people_results['results']
    total_pages=people_results['total_pages']
    if total_pages > page:
        person_ids.append(tmdb.get_people(source,page+1)['results'][0])
        show_people(person_ids,source,page)

def show_people(person_ids,source,page):
    people_window = peopleWindow('script-peopleWindow.xml', addon_path,'default')
    people_window.people=person_ids
    people_window.doModal()
    del people_window

class peopleWindow(xbmcgui.WindowXMLDialog):  
    people=[]
    controls=[]
    title=xbmcgui.ControlLabel
    backdrop=xbmcgui.ControlImage

    def onInit(self):
        base_font=utils.getBaseFont()
        self.update_people(self.people)

    def update_people(self,people):
        self.getControl(32120).setLabel('Page ' + str(page) + ' of ' + str(maxpage))
        title=xbmcgui.ControlButton(135,175,1000,30,'','','',0,0,0,title_font,'ff606060','',0,'','ff606060')
        self.addControl(title)
        title=self.getControl(3001)
        title.setAnimations([('windowclose', 'effect=fade end=0 time=0',)])
        for i in range(0,21):
            if len(people)>i:
                self.getControl(i+500).setImage('no-profile-w92.jpg')
            else:
                self.getControl(i+400).setEnabled(False) 
        for i in range(0,21):
            if len(people)>i:
                self.getControl(i+400).setEnabled(True)
                if people[i]['profile_path']==None:
                    self.getControl(i+200).setImage('no-profile-w92.jpg')
                else:
                    self.getControl(i+200).setImage('http://image.tmdb.org/t/p/w92' +people[i]['profile_path'])
                if i==0:self.onFocus(400)

        if source=='popular':self.getControl(32111).setLabel('Popular people')
        if source=='query':self.getControl(32111).setLabel('Search Results')

    def onFocus(self,control):
        xbmc.log(str(control))
        person_id=''
        backdrop = self.getControl(32107)
        person_id=self.get_person_from_control(control)

        if person_id!='':
            plot=self.getControl(32108)
            title=self.getControl(3001)
            person=tmdb.get_person(person_id)
            title.setLabel(person['name'])
            plot.setText(person['biography'])
            backdrop.setImage('')
            if person['profile_path']!=None:
                self.getControl(32121).setLabel('Loading')
                backdrop.setImage('http://image.tmdb.org/t/p/w130' +person['profile_path'])
            else:
                self.getControl(32121).setLabel('No Photo Available')
    def onAction(self, action):
        if action == 10:
            d = xbmcgui.Dialog()
            ans=d.yesno('tmdb Browser','Exit themoviedb.org Browser?')
            if ans:
                xbmc.executebuiltin('Dialog.Close(all,true)')
        elif action == 92:
            self.close()
        elif action==159:
            xbmc.executebuiltin('Dialog.Close(all,true)')
            from resources.lib import opening
            opening.startup()
                            
    def onClick(self,control):
        global exit_requested
        global source
        global query
        global page
        global maxpage
        do_tv=False
        do_people=False
        do_movies=False

        popular = 32101
        query_btn = 32110
        previous = 32116
        next =32117
        tv_shows = 32114
        movies = 32113
        people = 32115

        if control == popular:
            source='popular'
            page=1
            do_people=True
        if control == query_btn:
            source='query'
            do_people=True
            page=1
        if control == next:
            if page < maxpage:
                page=page+1
                do_people=True
        if control == previous:
            if page > 1:
                page=page-1
                do_people=True
        if control == tv_shows:
            do_tv=True
        if control == movies:
            do_movies=True

        if do_people:
            if source=='query':
                if control==query_btn:
                    k=xbmc.Keyboard('','Enter person Title to Search For')
                    k.doModal()
                    query=k.getText()
                if query!='':
                    people=tmdb.search_people(query,page)
                    maxpage=people['total_pages']
                    people=people['results']
                    if maxpage > page:
                        people.append(tmdb.search_people(query,page+1)['results'][0])    
                    self.close()
                    show_people(people,source,page)
            else:
                query=''
                xbmc.log(source)
                people=tmdb.get_people(source,page)
                total_pages=people['total_pages']
                maxpage=10
                if source=='upcoming' or source=='now_playing':maxpage=people['total_pages']
                people=people['results']
                if total_pages > page:
                    people.append(tmdb.get_people(source,page+1)['results'][0])
                self.close()
                show_people(people,source,page)
        if do_tv:
            from resources.lib import tvshows
            tvshows.source='popular'
            tvshows.startup()
        if do_movies:
            from resources.lib import movies
            movies.source='popular'
            movies.startup()

    def get_person_from_control(self,control):
        person_id=''
        if control==400:person_id=self.people[0]['id']
        if control==401:person_id=self.people[1]['id']
        if control==402:person_id=self.people[2]['id']
        if control==403:person_id=self.people[3]['id']
        if control==404:person_id=self.people[4]['id']
        if control==405:person_id=self.people[5]['id']
        if control==406:person_id=self.people[6]['id']
        if control==407:person_id=self.people[7]['id']
        if control==408:person_id=self.people[8]['id']
        if control==409:person_id=self.people[9]['id']
        if control==410:person_id=self.people[10]['id']
        if control==411:person_id=self.people[11]['id']
        if control==412:person_id=self.people[12]['id']
        if control==413:person_id=self.people[13]['id']
        if control==414:person_id=self.people[14]['id']
        if control==415:person_id=self.people[15]['id']
        if control==416:person_id=self.people[16]['id']
        if control==417:person_id=self.people[17]['id']
        if control==418:person_id=self.people[18]['id']
        if control==419:person_id=self.people[19]['id']
        if control==420:person_id=self.people[20]['id']
        return person_id

