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
    tv_results=tmdb.get_tv_shows(source,page)
    tv_ids=tv_results['results']
    total_pages=tv_results['total_pages']
    if total_pages > page:
        tv_ids.append(tmdb.get_tv_shows(source,page+1)['results'][0])
    show_tv(tv_ids,source,page)

def show_tv(tv_show_ids,source,page):
    tv_window = tv_Window('script-tvWindow.xml', addon_path,'default')
    tv_window.tv_shows=tv_show_ids
    tv_window.doModal()
    del tv_window

class tv_Window(xbmcgui.WindowXMLDialog):
    tv_shows=[]
    controls=[]
    name=xbmcgui.ControlLabel
    tagline=xbmcgui.ControlLabel
    backdrop=xbmcgui.ControlImage

    def onInit(self):
        self.update_tv_shows(self.tv_shows)

    def update_tv_shows(self,tv_shows):
        self.getControl(32120).setLabel('Page ' + str(page) + ' of ' + str(maxpage))
        title=xbmcgui.ControlButton(90,175,1000,30,'','','',0,0,0,title_font,'ff606060','',0,'','ff606060')
        self.addControl(title)
        title=self.getControl(3001)
        title.setAnimations([('windowclose', 'effect=fade end=0 time=0',)])
        for i in range(0,21):
            if len(tv_shows)>i:
                self.getControl(i+500).setImage('no-poster-w92.jpg')
            else:
                self.getControl(i+400).setEnabled(False) 
        xbmc_tvShows=[]
        for i in range(0,21):
            if len(tv_shows)>i:
                if tv_shows[i]['first_air_date']!=None:
                    if tv_shows[i]['name'] + ' ('+ tv_shows[i]['first_air_date'][:4] +')' in xbmc_tvShows:
                        self.getControl(i+300).setImage('xbmc_icon.png')
                self.getControl(i+400).setEnabled(True)
                if tv_shows[i]['poster_path']==None:
                    self.getControl(i+200).setImage('no-poster-w92.jpg')
                else:
                    self.getControl(i+200).setImage('http://image.tmdb.org/t/p/w92' +tv_shows[i]['poster_path'])
                if i==0:self.onFocus(400)

        self.getControl(599).setVisible(True)
        if source=='popular':self.getControl(32111).setLabel('Popular TV Shows')
        if source=='top_rated':self.getControl(32111).setLabel('Top Rated')
        if source=='on_the_air':self.getControl(32111).setLabel('On the Air')
        if source=='airing_today':self.getControl(32111).setLabel('Airing Today')
        if source=='query':self.getControl(32111).setLabel('Search Results')
        

    def onFocus(self,control):
        show_id=''
        backdrop = self.getControl(32107)
        show_id=self.get_show_from_control(control)
        if show_id!='':
            cast=self.getControl(32109)
            plot=self.getControl(32108)
            show=tmdb.get_tv_show(show_id)
            actors = show['credits']['cast']
            actors=sorted(actors, key=lambda k: k['order'])
            a = ''
            i=0
            for actor in actors:
                i=i+1
                a=a + actor['name'] +", "
                if i==3:break
            cast.setLabel(a[:-2])
            try:
                self.getControl(3001).setLabel(show['name'] + ' ('+ show['first_air_date'][:4] +')')
            except:
                pass
            plot.setText(show['overview'])
            backdrop.setImage('')
            if show['backdrop_path']!=None:
                self.getControl(32121).setLabel('Loading')
                backdrop.setImage('http://image.tmdb.org/t/p/w300' +show['backdrop_path'])
            else:
                self.getControl(32121).setLabel('No Background Available')

    def onAction(self, action):
        if action == 10:
            d = xbmcgui.Dialog()
            ans=d.yesno('tmdb Browser','Exit themoviedb.org Browser?')
            if ans:
                xbmc.executebuiltin('Dialog.Close(all,true)')
        elif action == 92:
            self.close()
             
    def onClick(self,control):
        global exit_requested
        global source
        global query
        global page
        global maxpage
        do_tv_shows=False
        do_movies=False

        popular = 32101
        top_rated =  32102
        on_the_air = 32103
        airing_today = 32104
        query_btn = 32110
        previous = 32116
        next =32117
        movies_btn = 32113
        tv_btn=32114
        people_btn=32115

        if control == popular and source!='popular':
            source='popular'
            page=1
            do_tv_shows=True
        if control == top_rated and source!='top_rated':
            source='top_rated'
            do_tv_shows=True
            page=1
        if control == on_the_air and source!='on_the_air':
            source='on_the_air'
            do_tv_shows=True
            page=1
        if control == airing_today and source!='airing_today':
            source='airing_today'
            do_tv_shows=True
            page=1
        if control == query_btn:
            source='query'
            do_tv_shows=True
            page=1
        if control == next:
            if page < maxpage:
                page=page+1
                do_tv_shows=True
        if control == previous:
            if page > 1:
                page=page-1
                do_tv_shows=True
        if control == movies_btn:
            do_movies=True
        if control == people_btn:
            do_people=True

        xbmc.log('source ='+source)
        if do_tv_shows:
            if source=='query':
                if control==query_btn:
                    k=xbmc.Keyboard('','Enter TV Show Name to Search For')
                    k.doModal()
                    query=k.getText()
                if query!='':
                    tv_shows=tmdb.search_tv_shows(query,page)
                    maxpage=tv_shows['total_pages']
                    tv_shows=tv_shows['results']
                    if maxpage > page:
                        tv_shows.append(tmdb.search_tv_shows(query,page+1)['results'][0])
                    self.close()
                    show_tv(tv_shows,source,page)
            else:
                query=''
                tv_shows=tmdb.get_tv_shows(source,page)
                maxpage=10
                if source=='airing_today' or source=='on_the_air':maxpage=tv_shows['total_pages']
                total_pages=tv_shows['total_pages']
                tv_shows=tv_shows['results']
                if total_pages > page:
                    tv_shows.append(tmdb.get_tv_shows(source,page+1)['results'][0])
                self.close()
                show_tv(tv_shows,source,page)
        if do_movies:
            from resources.lib import movies
            movies.source='popular'
            movies.startup()
        if do_people:
            from resources.lib import people
            people.source='popular'
            people.startup()

    def get_show_from_control(self,control):
        movieid=''
        show_id=''
        if control==400:show_id=self.tv_shows[0]['id']
        if control==401:show_id=self.tv_shows[1]['id']
        if control==402:show_id=self.tv_shows[2]['id']
        if control==403:show_id=self.tv_shows[3]['id']
        if control==404:show_id=self.tv_shows[4]['id']
        if control==405:show_id=self.tv_shows[5]['id']
        if control==406:show_id=self.tv_shows[6]['id']
        if control==407:show_id=self.tv_shows[7]['id']
        if control==408:show_id=self.tv_shows[8]['id']
        if control==409:show_id=self.tv_shows[9]['id']
        if control==410:show_id=self.tv_shows[10]['id']
        if control==411:show_id=self.tv_shows[11]['id']
        if control==412:show_id=self.tv_shows[12]['id']
        if control==413:show_id=self.tv_shows[13]['id']
        if control==414:show_id=self.tv_shows[14]['id']
        if control==415:show_id=self.tv_shows[15]['id']
        if control==416:show_id=self.tv_shows[16]['id']
        if control==417:show_id=self.tv_shows[17]['id']
        if control==418:show_id=self.tv_shows[18]['id']
        if control==419:show_id=self.tv_shows[19]['id']
        if control==420:show_id=self.tv_shows[20]['id']
        return show_id