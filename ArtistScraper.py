import spotipy
import spotipy.util as util
import pickle
import sys
import requests
from tqdm import tqdm
import os
import webbrowser
import warnings
import prince
import pandas as pd
import numpy as np
from multiprocessing import Pool
from functools import partial
from fuzzywuzzy import fuzz
import string
import json
import unidecode

warnings.simplefilter(action='ignore', category=FutureWarning)

# LASTFM infos
key_lastfm = '
secret_key_lastfm = ''

# Spotify Infos
scope = 'user-library-read'
username = ""

token = util.prompt_for_user_token(username, scope, client_id='', client_secret='', redirect_uri='http://localhost/')
if token:
    spotify = spotipy.Spotify(auth=token)
else:
    print("Connexion to spotify API failed.")
    sys.exit()


def authentificate_lastfm():
    t = requests.get('http://ws.audioscrobbler.com/2.0/?method=auth.gettoken&api_key={}&format=json'.format(key_lastfm))
    token = t.json()
    webbrowser.open('http://www.last.fm/api/auth/?api_key={}&token={}'.format(key_lastfm, token["token"]))


def get_details_tracks(tracks, pop):
    list_of_details = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'tempo']
    res = {}
    for i in list_of_details:
        det = [track[i] for track in tracks if track is not None]
        if len(det) == 0:
            return None
        mean = np.mean(det)
        std = np.std(det)
        res[i+"_top_tracks"] = {'mean': mean, 'std': std}
    res["popularity_top_tracks"] = {'mean': np.mean(pop), 'std': np.std(pop)}
    return res


def simplify_string(s):
    return unidecode.unidecode(s.lower()).replace('the', ' ').replace(' ', '').translate(str.maketrans('', '', string.punctuation))


def similar(a, b, threshold=80):
    return fuzz.ratio(simplify_string(a), simplify_string(b)) >= threshold


def get_artist_info(artist, website='spotify', nb_tracks_to_consider=5):
    if website == 'spotify':
        results = spotify.search(q='artist:' + artist, type='artist')
        if results['artists']['total'] > 0:
            maxi = None
            for i in results['artists']['items']:
                if similar(artist, i['name'], 80):
                    maxi = i
                    break
            if maxi is None:
                return None
            results = spotify.artist_top_tracks(maxi['uri'])['tracks'][:nb_tracks_to_consider]
            if results is None or len(results) == 0:
                return None
            pop = []
            ids = []
            for r in results:
                pop += [r['popularity']]
                ids += [r['id']]
            results = spotify.audio_features(ids)
            if results is None or len(results) == 0:
                return None
            det = get_details_tracks(results, pop)
            if det is None:
                return None
            return {**maxi, **det}
        else:
            return None
    else:
        r = requests.get('http://ws.audioscrobbler.com/2.0/?method=artist.search&artist={}&api_key={}&format=json'.format(artist, key_lastfm))
        try:
            data = r.json()
            if 'error' not in data.keys():
                maxi = None
                for i in data['results']['artistmatches']['artist']:
                    if similar(artist, i['name'], 80):
                        maxi = i
                if maxi is None:
                    return None
                r = requests.get('http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={}&api_key={}&format=json'.format(maxi['name'], key_lastfm))
                data = r.json()
                if 'error' not in data.keys():
                    maxi = data['artist']
                    maxi.pop("image", None)
                    maxi.pop("bio", None)
                    maxi['similar'] = [i['name'] for i in maxi['similar']['artist']]
                    maxi.pop("name", None)
                    maxi['tags'] = [i['name'] for i in maxi['tags']['tag']]
                    return maxi
                else:
                    if data['error'] == 29:
                        print('PB')
                    return None
            else:
                if data['error'] == 29:
                    print('PB')
                return None
        except json.decoder.JSONDecodeError:
            return None


def scrap_artists(year, month, day, website='spotify', nb_comp_mca=3):
    print("Scraping data of artists on %s starting..." % website)
    concerts = load_concerts(year, month, day)
    artists_list = []
    count = 0
    if 'artists_%s_data.pkl' % website in os.listdir('Data'):
        data_artists = load_artists(website)
        data_artists = list(data_artists.keys())
        for i in concerts['events']:
            if len(i['performance']) > 0:
                if i['performance'][0]['artist']['displayName'] not in data_artists and i['performance'][0]['artist']['displayName'] not in artists_list:
                    artists_list += [i['performance'][0]['artist']['displayName']]
            else:
                count += 1
        print("%d events over %d with no performance specified this day." % (count, len(concerts['events'])))
        if len(artists_list) == 0:
            print("No artist found this day, no update done.")
            return
        else:
            print("%d new artists found this day." % len(artists_list))
    else:
        for i in concerts['events']:
            if len(i['performance']) > 0:
                if i['performance'][0]['artist']['displayName'] not in artists_list:
                    artists_list += [i['performance'][0]['artist']['displayName']]
            else:
                count += 1
        print("%d events over %d with no performance specified." % (count, len(concerts['events'])))
    print("Scraping done.")


    def get_data():
        carac = []
        carac_per_artist = {}
        for key, val in artists_data.items():
            if val is not None:
                carac_per_artist[key] = val[carac_key]
                for j in val[carac_key]:
                    if j not in carac:
                        carac += [j]
        print("%d different %s have been found." % (len(carac), carac_key))
        df_artists = pd.DataFrame(carac_per_artist.keys(), columns=['artist'])
        df_caracs = pd.DataFrame(np.zeros((len(df_artists), len(carac))).astype(np.int32), columns=carac)
        df = pd.concat([df_artists, df_caracs], axis=1)
        for i, j in df.iterrows():
            for k in carac_per_artist[j['artist']]:
                df.at[i, k] = 1
        return df

    process_mca(get_data())
    save_artists(artists_data, website)


def process_scraped_data(artists_list, website):
    artists = {}
    count = 0
    nb_pool = 1 if website == "spotify" else 2
    with Pool(nb_pool) as p:
        artists_processed = list(tqdm(p.imap(partial(get_artist_info, website=website), artists_list), total=len(artists_list)))
    if website == "spotify":
        for i, j in zip(artists_list, artists_processed):
            artists[i] = j
            if artists[i] is not None:
                artists[i]['followers'] = artists[i]['followers']['total']
                artists[i].pop("images", None)
                artists[i].pop("external_urls", None)
                artists[i].pop("uri", None)
                artists[i].pop("href", None)
                artists[i].pop("type", None)
            else:
                count += 1
    else:
        for i, j in zip(artists_list, artists_processed):
            artists[i] = j
            if j is None:
                count += 1
    print("%d artists over %d not found on %s." % (count, len(artists_list), website))
    return artists
