import xml.dom.minidom
from xml.dom.minidom import Node
import xbmc
import os
import locale
import json
import xbmcgui
import xbmcaddon
from resources.lib import tmdb
addon = xbmcaddon.Addon()

def get_fonts():
    skin_dir = xbmc.translatePath("special://skin/")
    list_dir = os.listdir( skin_dir )
    fonts=[]
    fontxml_path =''
    font_xml=''
    for item in list_dir:
        item = os.path.join( skin_dir, item )
        if os.path.isdir( item ):
            font_xml = os.path.join( item, "Font.xml" )
        if os.path.exists( font_xml ):
            fontxml_path=font_xml
            break
    dom =  xml.dom.minidom.parse(fontxml_path)
    fontlist=dom.getElementsByTagName('font')
    for font in fontlist:
        name = font.getElementsByTagName('name')[0].childNodes[0].nodeValue
        size = font.getElementsByTagName('size')[0].childNodes[0].nodeValue
        if name not in fonts:fonts.append(name)
    return fonts

def getTitleFont():
    title_font='font13'
    base_size=20
    multiplier=1
    skin_dir = xbmc.translatePath("special://skin/")
    list_dir = os.listdir( skin_dir )
    fonts=[]
    fontxml_path =''
    font_xml=''
    for item in list_dir:
        item = os.path.join( skin_dir, item )
        if os.path.isdir( item ):
            font_xml = os.path.join( item, "Font.xml" )
        if os.path.exists( font_xml ):
            fontxml_path=font_xml
            break
    dom =  xml.dom.minidom.parse(fontxml_path)
    fontlist=dom.getElementsByTagName('font')
    for font in fontlist:
        name = font.getElementsByTagName('name')[0].childNodes[0].nodeValue
        size = font.getElementsByTagName('size')[0].childNodes[0].nodeValue
        fonts.append({'name':name,'size':float(size)})
    fonts =sorted(fonts, key=lambda k: k['size'])
    for f in fonts:
        if f['name']=='font13':
            multiplier=f['size'] / 20
            break
    for f in fonts:
        if f['size'] >= 26 * multiplier:
            title_font=f['name']
            break
    return title_font

def getBaseFont():
    title_font='font13'
    skin_dir = xbmc.translatePath("special://skin/")
    list_dir = os.listdir( skin_dir )
    fonts=[]
    fontxml_path =''
    font_xml=''
    for item in list_dir:
        item = os.path.join( skin_dir, item )
        if os.path.isdir( item ):
            font_xml = os.path.join( item, "Font.xml" )
        if os.path.exists( font_xml ):
            fontxml_path=font_xml
            break
    dom =  xml.dom.minidom.parse(fontxml_path)
    fontlist=dom.getElementsByTagName('font')
    for font in fontlist:
        name = font.getElementsByTagName('name')[0].childNodes[0].nodeValue
        size = font.getElementsByTagName('size')[0].childNodes[0].nodeValue
        fonts.append({'name':name,'size':float(size)})
    fonts =sorted(fonts, key=lambda k: k['size'])
    for f in fonts:
        if f['size'] >= 13:
            base_font=f['name']
            break
    return base_font

def format_currency(number):
    try:
        n='$' + format(number, ',.2f')
    except:
        n='$' + str(number)
    return n

def find_xbmc_by_title(title,year):
    moviestring = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": ["file","title","year"]}, "id": 1}')
    moviestring = unicode(moviestring, 'utf-8', errors='ignore')
    moviestring = json.loads(moviestring)  
    xbmc_file=''
    if 'result' in moviestring:
        if moviestring['result']['limits']['total'] > 0:
            for movie in moviestring['result']['movies']:
                if movie['title']==title and movie['year']==int(year):
                    xbmc_file=movie['file'] 
                    xbmc.log(xbmc_file) 
                    break
    return xbmc_file

def get_xbmc_movies():
    moviestring = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": ["title","year"]}, "id": 1}')
    moviestring = unicode(moviestring, 'utf-8', errors='ignore')
    moviestring = json.loads(moviestring)
    movies=set()
    if 'result' in moviestring:
        if moviestring['result']['limits']['total'] > 0:
            for movie in moviestring['result']['movies']:
                movies.add(movie['title'] + ' ('+ str(movie['year'])+')')
    return movies

def get_login():
    session_id=''
    d = xbmcgui.Dialog()
    ans=d.yesno('tmdb Browser','You Need to Login to Perform this Funciton','','Would you Like to Set your tmdb Credentials?')
    if ans:
        addon.openSettings()
        if addon.getSetting('username')!='' and addon.getSetting('password')!='':
            session_id=tmdb.validate_new_user(addon.getSetting('username'),addon.getSetting('password'))
            if session_id!='':
                addon.setSetting('session_id',session_id)
                dialog =xbmcgui.Dialog()
                dialog.notification('themoviedb.org Browser', 'themoviedb.org Login Success', xbmcgui.NOTIFICATION_INFO, 5000)
                return session_id
            else:
                dialog =xbmcgui.Dialog()
                dialog.notification('themoviedb.org Browser', 'themoviedb.org Login Failed', xbmcgui.NOTIFICATION_ERROR, 5000)
                return ''
    else:
        return ''

def add_favorite(movie_id,session_id):
    res=tmdb.update_favorite_movie(movie_id,session_id)
    movie=tmdb.get_movie(movie_id)
    if res['success']:
        dg=xbmcgui.Dialog()
        dg.notification('themoviedb.org Browser','Successfully Added '+ movie['title'] + ' to Favorites',xbmcgui.NOTIFICATION_INFO,5000)
    else:
        dg=xbmcgui.Dialog()
        dg.notification('themoviedb.org Browser','Error Adding '+ movie['title'] + ' to Favorites',xbmcgui.NOTIFICATION_ERROR,5000)
 
def remove_favorite(movie_id,session_id):
    movie=tmdb.get_movie(movie_id)
    res=tmdb.update_favorite_movie(movie_id,session_id)
    if res['success']:
        dg=xbmcgui.Dialog()
        dg.notification('themoviedb.org Browser','Successfully Removed '+ movie['title'] + ' from Favorites',xbmcgui.NOTIFICATION_INFO,5000)
    else:
        dg=xbmcgui.Dialog()
        dg.notification('themoviedb.org Browser','Error Removing '+ movie['title'] + ' from Favorites',xbmcgui.NOTIFICATION_ERROR,5000)

def add_watchlist(movie_id,session_id):
    movie=tmdb.get_movie(movie_id,session_id)
    res=tmdb.update_watchlist_movie(movie_id,session_id)
    if res['success']:
        dg=xbmcgui.Dialog()
        dg.notification('themoviedb.org Browser','Successfully Added '+ movie['title'] + ' to Watchlist',xbmcgui.NOTIFICATION_INFO,5000)
    else:
        dg=xbmcgui.Dialog()
        dg.notification('themoviedb.org Browser','Error Adding '+ movie['title'] + ' to Watchlist',xbmcgui.NOTIFICATION_ERROR,5000)

def remove_watchlist(movie_id,session_id):
    movie=tmdb.get_movie(movie_id)
    res=tmdb.update_watchlist_movie(movie_id,session_id)
    if res['success']:
        dg=xbmcgui.Dialog()
        dg.notification('themoviedb.org Browser','Successfully Removed '+ movie['title'] + ' from Watchlist',xbmcgui.NOTIFICATION_INFO,5000)
    else:
        dg=xbmcgui.Dialog()
        dg.notification('themoviedb.org Browser','Error Removing '+ movie['title'] + ' from Watchlist',xbmcgui.NOTIFICATION_ERROR,5000)

def movie_on_list(movie_id,session_id):
    lists=tmdb.get_users_lists(addon.getSetting('session_id'),1)
    lists_results=lists['results']
    in_list=''
    for list in lists_results:
        if tmdb.is_in_list(list['id'],movie_id)['item_present']:
            in_list=True
            break
    if lists['total_pages']> 1 and not in_list:
        for i in range(2,lists['total_pages']):
            l=tmdb.get_users_lists(addon.getSetting('session_id'),i)
            for list in l['results']:
                if tmdb.is_in_list(list['id'],movie_id)['item_present']:
                    in_list=True
                    break
    return in_list
