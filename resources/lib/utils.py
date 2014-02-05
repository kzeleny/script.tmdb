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

def getTitleFont():
    title_font='font13'
    skin_dir = xbmc.translatePath("special://skin/")
    list_dir = os.listdir( skin_dir )
    fonts=[]
    fontxml_path =''
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
        if f['size'] >= 28:
            title_font=f['name']
            break
    return title_font

def getBaseFont():
    title_font='font13'
    skin_dir = xbmc.translatePath("special://skin/")
    list_dir = os.listdir( skin_dir )
    fonts=[]
    fontxml_path =''
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

def format_date(strDate):
    strDate=str(strDate)
    if strDate=='None':strDate=''
    if '-' in strDate:
        d=strDate.split('-')
        if d[1]=='01':d[1]='January'
        if d[1]=='02':d[1]='February'
        if d[1]=='03':d[1]='March'
        if d[1]=='04':d[1]='April'
        if d[1]=='05':d[1]='May'
        if d[1]=='06':d[1]='June'
        if d[1]=='07':d[1]='July'
        if d[1]=='08':d[1]='August'
        if d[1]=='09':d[1]='September'
        if d[1]=='10':d[1]='October'
        if d[1]=='11':d[1]='November'
        if d[1]=='12':d[1]='December'
        strDate=d[1] + ' ' + d[2] + ', ' + d[0]
    return strDate

def format_currency(number):
    locale.setlocale( locale.LC_ALL, '' )
    return locale.currency( number, grouping=True )[:-3]

def find_xbmc_by_title(title):
    moviestring = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": ["file","title","imdbnumber"]}, "id": 1}')
    moviestring = unicode(moviestring, 'utf-8', errors='ignore')
    moviestring = json.loads(moviestring)  
    xbmc_file=''
    if 'result' in moviestring:
        for movie in moviestring['result']['movies']:
            if movie['title']==title:
                xbmc_file=movie['file'] 
                xbmc.log(xbmc_file) 
                break
    return xbmc_file

def get_xbmc_movies():
    moviestring = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": ["title","year"]}, "id": 1}')
    moviestring = unicode(moviestring, 'utf-8', errors='ignore')
    moviestring = json.loads(moviestring)  
    movies=set()
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
