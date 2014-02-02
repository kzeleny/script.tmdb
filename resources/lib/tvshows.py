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

        self.removeControls(self.controls)
        if len(tv_shows)>0:
            if tv_shows[0]['poster_path']==None:
                b0=xbmcgui.ControlButton(466,225,92,138,tv_shows[0]['name'],no_poster_path,no_poster_path)
            else:
                b0=xbmcgui.ControlButton(466,225,92,138,'','http://image.tmdb.org/t/p/w92' +tv_shows[0]['poster_path'],'http://image.tmdb.org/t/p/w92' + tv_shows[0]['poster_path'])
        if len(tv_shows) > 1:
            if tv_shows[1]['poster_path']==None:
                b1=xbmcgui.ControlButton(578,225,92,138,tv_shows[1]['name'],no_poster_path,no_poster_path)
            else:
                b1=xbmcgui.ControlButton(578,225,92,138,'','http://image.tmdb.org/t/p/w92' +tv_shows[1]['poster_path'],'http://image.tmdb.org/t/p/w92' + tv_shows[1]['poster_path'])
        if len(tv_shows) > 2:
            if tv_shows[2]['poster_path']==None:
                b2=xbmcgui.ControlButton(690,225,92,138,tv_shows[2]['name'],no_poster_path,no_poster_path)
            else:        
                b2=xbmcgui.ControlButton(690,225,92,138,'','http://image.tmdb.org/t/p/w92' +tv_shows[2]['poster_path'],'http://image.tmdb.org/t/p/w92' + tv_shows[2]['poster_path'])
        if len(tv_shows) > 3:
            if tv_shows[3]['poster_path']==None:
                b3=xbmcgui.ControlButton(802,225,92,138,tv_shows[3]['name'],no_poster_path,no_poster_path)
            else:        
                b3=xbmcgui.ControlButton(802,225,92,138,'','http://image.tmdb.org/t/p/w92' +tv_shows[3]['poster_path'],'http://image.tmdb.org/t/p/w92' + tv_shows[3]['poster_path'])
        if len(tv_shows) > 4:
            if tv_shows[4]['poster_path']==None:
                b4=xbmcgui.ControlButton(914,225,92,138,tv_shows[4]['name'],no_poster_path,no_poster_path)
            else: 
                b4=xbmcgui.ControlButton(914,225,92,138,'','http://image.tmdb.org/t/p/w92' +tv_shows[4]['poster_path'],'http://image.tmdb.org/t/p/w92' + tv_shows[4]['poster_path'])
        if len(tv_shows) > 5:
            if tv_shows[5]['poster_path']==None:
                b5=xbmcgui.ControlButton(1026,225,92,138,tv_shows[5]['name'],no_poster_path,no_poster_path)
            else: 
                b5=xbmcgui.ControlButton(1026,225,92,138,'','http://image.tmdb.org/t/p/w92' +tv_shows[5]['poster_path'],'http://image.tmdb.org/t/p/w92' + tv_shows[5]['poster_path'])
        if len(tv_shows) > 6:
            if tv_shows[6]['poster_path']==None:
                b6=xbmcgui.ControlButton(1138,225,92,138,tv_shows[6]['name'],no_poster_path,no_poster_path)
            else: 
                b6=xbmcgui.ControlButton(1138,225,92,138,'','http://image.tmdb.org/t/p/w92' +tv_shows[6]['poster_path'],'http://image.tmdb.org/t/p/w92' + tv_shows[6]['poster_path'])
        if len(tv_shows) > 7:
            if tv_shows[7]['poster_path']==None:
                b7=xbmcgui.ControlButton(466,383,92,138,tv_shows[7]['name'],no_poster_path,no_poster_path)
            else: 
                b7=xbmcgui.ControlButton(466,383,92,138,'','http://image.tmdb.org/t/p/w92' +tv_shows[7]['poster_path'],'http://image.tmdb.org/t/p/w92' + tv_shows[7]['poster_path'])
        if len(tv_shows) > 8:
            if tv_shows[8]['poster_path']==None:
                b8=xbmcgui.ControlButton(578,383,92,138,tv_shows[8]['name'],no_poster_path,no_poster_path)
            else: 
                b8=xbmcgui.ControlButton(578,383,92,138,'','http://image.tmdb.org/t/p/w92' +tv_shows[8]['poster_path'],'http://image.tmdb.org/t/p/w92' + tv_shows[8]['poster_path'])
        if len(tv_shows) > 9:
            if tv_shows[9]['poster_path']==None:
                b9=xbmcgui.ControlButton(690,383,92,138,tv_shows[9]['name'],no_poster_path,no_poster_path)
            else: 
                b9=xbmcgui.ControlButton(690,383,92,138,'','http://image.tmdb.org/t/p/w92' +tv_shows[9]['poster_path'],'http://image.tmdb.org/t/p/w92' + tv_shows[9]['poster_path'])
        if len(tv_shows) > 10:
            if tv_shows[10]['poster_path']==None:
                b10=xbmcgui.ControlButton(802,383,92,138,tv_shows[10]['name'],no_poster_path,no_poster_path)
            else: 
                b10=xbmcgui.ControlButton(802,383,92,138,'','http://image.tmdb.org/t/p/w92' +tv_shows[10]['poster_path'],'http://image.tmdb.org/t/p/w92' + tv_shows[10]['poster_path'])
        if len(tv_shows) > 11:
            if tv_shows[11]['poster_path']==None:
                b11=xbmcgui.ControlButton(914,383,92,138,tv_shows[11]['name'],no_poster_path,no_poster_path)
            else:  
                b11=xbmcgui.ControlButton(914,383,92,138,'','http://image.tmdb.org/t/p/w92' +tv_shows[11]['poster_path'],'http://image.tmdb.org/t/p/w92' + tv_shows[11]['poster_path'])
        if len(tv_shows) > 12:
            if tv_shows[12]['poster_path']==None:
                b12=xbmcgui.ControlButton(1026,383,92,138,tv_shows[12]['name'],no_poster_path,no_poster_path)
            else:  
                b12=xbmcgui.ControlButton(1026,383,92,138,'','http://image.tmdb.org/t/p/w92' +tv_shows[12]['poster_path'],'http://image.tmdb.org/t/p/w92' + tv_shows[12]['poster_path'])
        if len(tv_shows) > 13:
            if tv_shows[13]['poster_path']==None:
                b13=xbmcgui.ControlButton(1138,383,92,138,tv_shows[13]['name'],no_poster_path,no_poster_path)
            else:  
                b13=xbmcgui.ControlButton(1138,383,92,138,'','http://image.tmdb.org/t/p/w92' +tv_shows[13]['poster_path'],'http://image.tmdb.org/t/p/w92' + tv_shows[13]['poster_path'])
        if len(tv_shows) > 14:
            if tv_shows[14]['poster_path']==None:
                b14=xbmcgui.ControlButton(466,541,92,138,tv_shows[14]['name'],no_poster_path,no_poster_path)
            else:  
                b14=xbmcgui.ControlButton(466,541,92,138,'','http://image.tmdb.org/t/p/w92' +tv_shows[14]['poster_path'],'http://image.tmdb.org/t/p/w92' + tv_shows[14]['poster_path'])
        if len(tv_shows) > 15:
            if tv_shows[15]['poster_path']==None:
                b15=xbmcgui.ControlButton(578,541,92,138,tv_shows[15]['name'],no_poster_path,no_poster_path)
            else:  
                b15=xbmcgui.ControlButton(578,541,92,138,'','http://image.tmdb.org/t/p/w92' +tv_shows[15]['poster_path'],'http://image.tmdb.org/t/p/w92' + tv_shows[15]['poster_path'])
        if len(tv_shows) > 16:
            if tv_shows[16]['poster_path']==None:
                b16=xbmcgui.ControlButton(690,541,92,138,tv_shows[16]['name'],no_poster_path,no_poster_path)
            else:  
                b16=xbmcgui.ControlButton(690,541,92,138,'','http://image.tmdb.org/t/p/w92' +tv_shows[16]['poster_path'],'http://image.tmdb.org/t/p/w92' + tv_shows[16]['poster_path'])
        if len(tv_shows) > 17:
            if tv_shows[17]['poster_path']==None:
                b17=xbmcgui.ControlButton(802,541,92,138,tv_shows[17]['name'],no_poster_path,no_poster_path)
            else:  
                b17=xbmcgui.ControlButton(802,541,92,138,'','http://image.tmdb.org/t/p/w92' +tv_shows[17]['poster_path'],'http://image.tmdb.org/t/p/w92' + tv_shows[17]['poster_path'])
        if len(tv_shows) > 18:
            if tv_shows[18]['poster_path']==None:
                b18=xbmcgui.ControlButton(914,541,92,138,tv_shows[18]['name'],no_poster_path,no_poster_path)
            else:  
                b18=xbmcgui.ControlButton(914,541,92,138,'','http://image.tmdb.org/t/p/w92' +tv_shows[18]['poster_path'],'http://image.tmdb.org/t/p/w92' + tv_shows[18]['poster_path'])
        if len(tv_shows) > 19:
            if tv_shows[19]['poster_path']==None:
                b19=xbmcgui.ControlButton(1026,541,92,138,tv_shows[19]['name'],no_poster_path,no_poster_path)
            else:  
                b19=xbmcgui.ControlButton(1026,541,92,138,'','http://image.tmdb.org/t/p/w92' +tv_shows[19]['poster_path'],'http://image.tmdb.org/t/p/w92' + tv_shows[19]['poster_path'])
        if len(tv_shows) > 20:
            if tv_shows[20]['poster_path']==None:
                b19=xbmcgui.ControlButton(1138,541,92,138,tv_shows[19]['name'],no_poster_path,no_poster_path)
            else:  
                b20=xbmcgui.ControlButton(1138,541,92,138,'','http://image.tmdb.org/t/p/w92' +tv_shows[20]['poster_path'],'http://image.tmdb.org/t/p/w92' + tv_shows[20]['poster_path'])
        name=xbmcgui.ControlButton(90,175,1000,30,'','','',0,0,0,title_font,'ff606060','',0,'','ff606060')
        
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
        controls.append(name)
        self.controls=controls

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
        b20.controlUp(b13)

        if source=='popular':self.getControl(32111).setLabel('Popular TV Shows')
        if source=='top_rated':self.getControl(32111).setLabel('Top Rated')
        if source=='upcoming':self.getControl(32111).setLabel('On the Air')
        if source=='now_playing':self.getControl(32111).setLabel('Airing Today')
        if source=='query':self.getControl(32111).setLabel('Search Results')
        
        self.setFocus(b0)

    def onFocus(self,control):
        tv_show_id=''
        backdrop = self.getControl(32107)
        if control==3001:tv_show_id=self.tv_shows[0]['id']
        if control==3002:tv_show_id=self.tv_shows[1]['id']
        if control==3003:tv_show_id=self.tv_shows[2]['id']
        if control==3004:tv_show_id=self.tv_shows[3]['id']
        if control==3005:tv_show_id=self.tv_shows[4]['id']
        if control==3006:tv_show_id=self.tv_shows[5]['id']
        if control==3007:tv_show_id=self.tv_shows[6]['id']
        if control==3008:tv_show_id=self.tv_shows[7]['id']
        if control==3009:tv_show_id=self.tv_shows[8]['id']
        if control==3010:tv_show_id=self.tv_shows[9]['id']
        if control==3011:tv_show_id=self.tv_shows[10]['id']
        if control==3012:tv_show_id=self.tv_shows[11]['id']
        if control==3013:tv_show_id=self.tv_shows[12]['id']
        if control==3014:tv_show_id=self.tv_shows[13]['id']
        if control==3015:tv_show_id=self.tv_shows[14]['id']
        if control==3016:tv_show_id=self.tv_shows[15]['id']
        if control==3017:tv_show_id=self.tv_shows[16]['id']
        if control==3018:tv_show_id=self.tv_shows[17]['id']
        if control==3019:tv_show_id=self.tv_shows[18]['id']
        if control==3020:tv_show_id=self.tv_shows[19]['id']
        if control==3021:tv_show_id=self.tv_shows[20]['id']

        if tv_show_id!='':
            cast=self.getControl(32109)
            plot=self.getControl(32108)
            name=self.getControl(3022)
            tv_show=tmdb.get_tv_show (tv_show_id)
            actors = tv_show['credits']['cast']
            actors=sorted(actors, key=lambda k: k['order'])
            a = ''
            i=0
            for actor in actors:
                i=i+1
                a=a + actor['name'] +", "
                if i==3:break
            cast.setLabel(a[:-2])
            if tv_show['first_air_date']!=None:
                name.setLabel(tv_show['name'] + ' ('+ tv_show['first_air_date'][:4] +')')
            else:
                name.setLabel(tv_show['name'])
            plot.setText(tv_show['overview'])
            backdrop.setImage('')
            if tv_show['backdrop_path']!=None:
                self.getControl(32121).setLabel('Loading')
                backdrop.setImage('http://image.tmdb.org/t/p/w300' +tv_show['backdrop_path'])
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
        upcoming = 32103
        now_playing = 32104
        query_btn = 32110
        previous = 32116
        next =32117
        movies_btn = 32113

        if control == popular:
            source='popular'
            page=1
            do_tv_shows=True
        if control == top_rated:
            source='top_rated'
            do_tv_shows=True
            page=1
        if control == upcoming:
            source='upcoming'
            do_tv_shows=True
            page=1
        if control == now_playing:
            source='now_playing'
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
                if source=='upcoming' or source=='now_playing':maxpage=tv_shows['total_pages']
                total_pages=tv_shows['total_pages']
                tv_shows=tv_shows['results']
                if total_pages > page:
                    tv_shows.append(tmdb.get_tv_shows(source,page+1)['results'][0])
                self.close()
                show_tv(tv_shows,source,page)
        elif do_movies:
           from resources.lib import movies
           self.close()
           movies.startup()

