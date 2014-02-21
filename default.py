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

addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path')
do_home=False


if addon.getSetting('session_id')=='' and addon.getSetting('username')!='' and addon.getSetting('password')!='':
    addon.setSetting('session_id',tmdb.validate_new_user(addon.getSetting('username'),addon.getSetting('password')))

if addon.getSetting('startup')=='true':
    from resources.lib import opening
    opening.startup()
else:
    from resources.lib import movie
    from resources.lib import movies
    movies.source='popular'
    movies.page=1
    movies.startup()
