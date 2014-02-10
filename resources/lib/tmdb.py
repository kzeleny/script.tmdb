from urllib import quote_plus, unquote_plus
import json
import urllib
import urllib2
import xbmc

image_base_url=''
you_tube_base_url='plugin://plugin.video.youtube/?action=play_video&videoid='
api_key='99e8b7beac187a857152f57d67495cf4'

def get_genres():
    data = {}
    data['api_key'] = api_key
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/genre/list'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    return infostring['genres']

def get_movies(source,page):
    data = {}
    data['api_key'] = api_key
    data['page'] = str(page)
    data['language']='en'
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/movie/' + source
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    return infostring

def get_movie(movieId):
    data={}
    data['append_to_response']='credits,trailers,releases,images,keywords'
    data['api_key'] = api_key
    url_values = urllib.urlencode(data)
    url = 'http://api.themoviedb.org/3/movie/' + str(movieId)
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    movieString = urllib2.urlopen(req).read()
    movieString = unicode(movieString, 'utf-8', errors='ignore')
    movieString = json.loads(movieString)
    return movieString

def search_movies(query,page):
    global maxpage
    movieIds=[]
    data = {}
    data['api_key'] = api_key
    data['page']=str(page)
    data['query']=query
    data['language']='en'
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/search/movie'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    return infostring

def get_favorite_movies(session_id,page):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    data = {}
    data['api_key'] = api_key
    data['page']=str(page)
    data['session_id'] = session_id
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/account/' + str(session_id) + '/favorite_movies'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url,headers=headers)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    return infostring

def get_watchlist_movies(session_id,page):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    data = {}
    data['api_key'] = api_key
    data['page']=str(page)
    data['session_id'] = session_id
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/account/' + str(session_id) + '/movie_watchlist'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url,headers=headers)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    return infostring

def get_rated_movies(session_id,page):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    data = {}
    data['api_key'] = api_key
    data['page']=str(page)
    data['session_id'] = session_id
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/account/' + str(session_id) + '/rated_movies'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url,headers=headers)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    return infostring

def rate_movie(movie_id,value,session_id):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    values = json.dumps({"value": value})
    data = {}
    data['api_key'] = api_key
    data['session_id'] = session_id
    url_values = urllib.urlencode(data)
    url = 'http://api.themoviedb.org/3/movie/'+str(movie_id) +'/rating'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url,values,headers)
    infostring = urllib2.urlopen(req).read()
    xbmc.log(infostring)
    infostring = json.loads(infostring)
    if infostring['status_code']in (1,12):
        return True
    else:
        return False



def get_image_base_url():
    data = {}
    data['api_key'] = api_key
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/configuration'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    return infostring['images']['base_url']

def get_movies_by_genre(genre,page):
    sort_by='popularity.desc'
    data = {}
    data['api_key'] = api_key
    data['page'] = str(page)
    data['language']='en'
    data['with_genres']=genre
    data['sort_by']=sort_by
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/discover/movie'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    return infostring

def get_movies_by_year(year,page):
    sort_by='popularity.desc'
    data = {}
    data['api_key'] = api_key
    data['page'] = str(page)
    data['language']='en'
    data['year']=year
    data['sort_by']=sort_by
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/discover/movie'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    return infostring

def getMoviesByActor(actor,page):
    data = {}
    data['api_key'] = api_key
    data['page'] = str(page)
    data['language']='en'
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/person/' + str(actor) + '/movie_credits'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    xbmc.log(infostring)
    infostring = json.loads(infostring)
    return infostring['cast']

def getMoviesByKeyword(keyword,page):
    data = {}
    data['api_key'] = api_key
    data['page'] = str(page)
    data['language']='en'
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/keyword/' + str(keyword) + '/movies'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    xbmc.log(infostring)
    infostring = json.loads(infostring)
    return infostring['results']

def get_similar_movies(movie_id,page):
    data = {}
    data['api_key'] = api_key
    data['page']=str(page)
    data['language']='en'
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/movie/' + str(movie_id) + '/similar_movies'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    return infostring

def get_cast_by_movie_id(movie_id):
    data = {}
    data['append_to_response']='credits'
    data['api_key'] = '99e8b7beac187a857152f57d67495cf4'
    url_values = urllib.urlencode(data)
    url = 'http://api.themoviedb.org/3/movie/' + str(movie_id)
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    credits = urllib2.urlopen(req).read()
    credits = unicode(credits, 'utf-8', errors='ignore')
    credits = json.loads(credits)
    cast=credits['credits']['cast']
    return cast

def get_crew_by_movie_id(movie_id):
    data = {}
    data['append_to_response']='credits'
    data['api_key'] = api_key
    url_values = urllib.urlencode(data)
    url = 'http://api.themoviedb.org/3/movie/' + str(movie_id)
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    credits = urllib2.urlopen(req).read()
    credits = unicode(credits, 'utf-8', errors='ignore')
    credits = json.loads(credits)
    crew=credits['credits']['crew']
    return crew

def search_people(name,page):
    data = {}
    data['api_key'] = api_key
    data['page'] = str(page)
    data['query'] = name
    url_values = urllib.urlencode(data)
    url = 'http://api.themoviedb.org/3/search/person'
    full_url = url + '?' + url_values
    xbmc.log(full_url)
    req = urllib2.Request(full_url)
    people = urllib2.urlopen(req).read()
    people = json.loads(people)
    return people

def get_people(source,page):
    data = {}
    data['api_key'] = api_key
    data['page'] = str(page)
    url_values = urllib.urlencode(data)
    url = 'http://api.themoviedb.org/3/person/' + source 
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    people = urllib2.urlopen(req).read()
    people = json.loads(people)
    return people

def get_people_movie_credits(person_id,page):
    data = {}
    data['api_key'] = api_key
    data['page'] = str(page)
    url_values = urllib.urlencode(data)
    url = 'http://api.themoviedb.org/3/person/' + person_id + '/movie_credits' 
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    people = urllib2.urlopen(req).read()
    people = json.loads(person)
    return people

def get_people_tv_credits(person_id,page):
    data = {}
    data['api_key'] = api_key
    data['page'] = str(page)
    url_values = urllib.urlencode(data)
    url = 'http://api.themoviedb.org/3/person/' + person_id + '/tv_credits' 
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    people = urllib2.urlopen(req).read()
    people = json.loads(person)
    return people

def get_people_combined_credits(person_id,page):
    data = {}
    data['api_key'] = api_key
    data['page'] = str(page)
    url_values = urllib.urlencode(data)
    url = 'http://api.themoviedb.org/3/person/' + person_id + '/combined_credits' 
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    people = urllib2.urlopen(req).read()
    people = json.loads(person)
    return people

def get_person(person_id):
    data = {}
    data['api_key'] = api_key
    data['append_to_response'] ='combined_credits'
    url_values = urllib.urlencode(data)
    url = 'http://api.themoviedb.org/3/person/' + str(person_id)
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    person = urllib2.urlopen(req).read()
    person = json.loads(person)
    return person

def get_tv_shows(source,page):
    data = {}
    data['api_key'] = api_key
    data['page'] = str(page)
    data['language']='en'
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/tv/' + source
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    return infostring

def get_tv_show(tv_show_id):
    data={}
    data['append_to_response']='credits,images'
    data['api_key'] = api_key
    url_values = urllib.urlencode(data)
    url = 'http://api.themoviedb.org/3/tv/' + str(tv_show_id)
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    tvString = urllib2.urlopen(req).read()
    tvString = unicode(tvString, 'utf-8', errors='ignore')
    tvString = json.loads(tvString)
    return tvString

def search_tv_shows(query,page):
    global maxpage
    movieIds=[]
    data = {}
    data['api_key'] = api_key
    data['page']=str(page)
    data['query']=query
    data['language']='en'
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/search/tv'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    return infostring

def get_movie_account_states(movie_id,session_id):
    data = {}
    data['api_key'] = api_key
    data['session_id'] = session_id
    url_values = urllib.urlencode(data)
    url = 'http://api.themoviedb.org/3/movie/'+str(movie_id) +'/account_states'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    xbmc.log(str(infostring))
    return infostring

def update_favorite_movie(movie_id,session_id):
    account_state = get_movie_account_states(movie_id,session_id)
    favorite=True
    if account_state['favorite']:favorite=False
    values = {"movie_id": movie_id,'favorite':favorite}
    values = json.dumps(values)
    xbmc.log(values)
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    data = {}
    data['api_key'] = api_key
    data['session_id'] = session_id
    url_values = urllib.urlencode(data)
    url = 'http://api.themoviedb.org/3/account/'+str(movie_id) +'/favorite'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url,values,headers)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    xbmc.log(str(infostring))
    if infostring['status_code'] in (13,12,1):
        return {'update':favorite,'success':True}
    else:
        return  {'update':favorite,'success':False}
  
def update_watchlist_movie(movie_id,session_id):
    account_state = get_movie_account_states(movie_id,session_id)
    watchlist=True
    if account_state['watchlist']:watchlist=False
    values = {"movie_id": movie_id,'movie_watchlist':watchlist}
    values = json.dumps(values)
    xbmc.log(values)
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    data = {}
    data['api_key'] = api_key
    data['session_id'] = session_id
    url_values = urllib.urlencode(data)
    url = 'http://api.themoviedb.org/3/account/'+str(movie_id) +'/movie_watchlist'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url,values,headers)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    xbmc.log(str(infostring))
    if infostring['status_code'] in (13,12,1):
        return {'update':watchlist,'success':True}
    else:
        return  {'update':watchlist,'success':False}

def get_guest_session_id():
    data = {}
    data['api_key'] = api_key
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/authentication/guest_session/new'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    return infostring['guest_session_id']

def validate_new_user(username,password):
    token=request_token()
    authorize_token(username,password,token)
    session_id=get_new_session(token)
    return session_id
   
def request_token():
    data = {}
    data['api_key'] = api_key
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/authentication/token/new'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    return infostring['request_token']

def authorize_token(username,password,request_token):
    data = {}
    data['username'] =  username
    data['password'] = password
    url_values = urllib.urlencode(data)
    url = 'https://www.themoviedb.org/authenticate/'+request_token + '/validate_with_login'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    
def get_new_session(request_token):
    data = {}
    data['api_key'] = api_key
    data['request_token'] = request_token
    url_values = urllib.urlencode(data)
    url = 'https://api.themoviedb.org/3/authentication/session/new'
    full_url = url + '?' + url_values
    xbmc.log(full_url)
    req = urllib2.Request(full_url)
    try:
        infostring = urllib2.urlopen(req).read()
        infostring = json.loads(infostring)
        if infostring['success']:
            return infostring['session_id']
        else:
         return ''
    except:
        return ''

def get_account(session_id):
    data = {}
    data['api_key'] = api_key
    data['session_id'] = session_id
    url_values = urllib.urlencode(data)
    url = 'http://api.themoviedb.org/3/account'
    full_url = url + '?' + url_values
    req = urllib2.Request(full_url)
    infostring = urllib2.urlopen(req).read()
    infostring = json.loads(infostring)
    xbmc.log(str(infostring))
    return infostring