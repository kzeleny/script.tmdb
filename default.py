# Random trailer player
#
# Author - kzeleny
# Version - 1.1.8
# Compatibility - Frodo/Gothum
#
import xbmc
import xbmcgui
import xbmcaddon
from resources.lib import tmdb
from resources.lib import movies
from resources.lib import people
from resources.lib import tvshows
from resources.lib import opening

addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path')
start_mode=addon.getSetting('start_mode')

if addon.getSetting('session_id')=='' and addon.getSetting('username')!='' and addon.getSetting('password')!='':
    addon.setSetting('session_id',tmdb.validate_new_user(addon.getSetting('username'),addon.getSetting('password')))

if start_mode=='0':
    opening.startup()
elif start_mode=='1':
    people.startup()
elif start_mode=='2':
    tvshows.startup()
else:
    movies.startup()
