#!/usr/bin/env python3

import argparse
import requests

attrs = ["all", "mixTerm", "genreIndex", "artistTerm",
         "composerTerm", "albumTerm", "ratingIndex", "songTerm"]

parser = argparse.ArgumentParser(description="Download high resolution album art from the iTunes store",
    epilog="By default 'freetext' is search for through all music metadata and the matches are returned. " +
    "On these matches a search for album title is performed. It is done case-insensitively using " + 
    "Levenshtein distance with extra low cost given to deletions, to allow fuzzy matches. " +
    "The album that matches best is then downloaded to the present working directory, and named " +
    "following the pattern 'album artist - album title.png'.")

parser.add_argument("freetext", type=str,
    help="search term that will match on attribute(s) specified by 'attr'.")

parser.add_argument("album", type=str, 
    help="title of the album to search for. Closest approximate match among the 'freetext' candidates.")

parser.add_argument("-a", "--attr", type=str, default="all",
    help="the attribute to search for using 'freetext'. Available options are: " + 
    ", ".join(attrs) + " (default: %(default)s)",
    choices=attrs, metavar='ATTR')

parser.add_argument("-c", "--country", type=str, default="US", 
    help='the two-letter country code for the territory you want to search. (default: %(default)s)')

parser.add_argument("-q", "--quiet", action="store_true",
    help="print status messages and partial results.")

args = parser.parse_args()


def ldist(s, t, costs=(1, 1, 1)):
    """ 
        original: https://www.python-course.eu/levenshtein_distance.php
        
        ldist is the Levenshtein distance between the strings 
        s and t.
        For all i and j, dist[i,j] will contain the Levenshtein 
        distance between the first i characters of s and the 
        first j characters of t
        
        costs: a tuple or a list with three integers (d, i, s)
               where d defines the costs for a deletion
                     i defines the costs for an insertion and
                     s defines the costs for a substitution
    """
    
    rows = len(s)+1
    cols = len(t)+1
    deletes, inserts, substitutes = costs
    
    dist = [[0 for x in range(cols)] for x in range(rows)]
    
    # source prefixes can be transformed into empty strings 
    # by deletions:
    for row in range(1, rows):
        dist[row][0] = row * deletes
    
    # target prefixes can be created from an empty source string
    # by inserting the characters
    for col in range(1, cols):
        dist[0][col] = col * inserts
        
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                sub = 0
            else:
                sub = substitutes
            dist[row][col] = min(dist[row-1][col] + deletes,
                                 dist[row][col-1] + inserts,
                                 dist[row-1][col-1] + sub)
    
    # # to print the edit matrix
    # for r in range(rows):
    #     print(dist[r])
    
    return dist[row][col]



def download_albumart(freetext, albumtitle, attr="all", country="US", ext=".png", verbose=True):
    """
        iTunes API
        https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
    """
    
    terms = ["all", "", "mixTerm", "genreIndex", "artistTerm", 
        "composerTerm", "albumTerm", "ratingIndex", "songTerm"]
        
    if not attr in terms:
        terms_q = ", ".join(['"' + x + '"' for x in terms])
        raise Exception("'attr' is not one of:\n{}".format(terms_q))
    
    col = "\033[38;5;0;48;5;7m"
    reset = "\033[0m"
    
    if attr == "artistTerm":
        params_artist = dict(term=freetext, country=country, media="music", entity="musicArtist")
        res_artist = requests.get("https://itunes.apple.com/search", params=params_artist)
        
        if not res_artist:
            raise Exception("URL response failed with error: {}".format(res_artist.status_code))
        
        res_artist_j = res_artist.json()
        
        artistids = [x["artistId"] for x in res_artist_j["results"]]
        artistids = ",".join(map(str, artistids))
        
        params_lookup = dict(id=artistids, entity="album")
        res = requests.get("https://itunes.apple.com/lookup", params_lookup)
        res_j = res.json()["results"]
        res_j = [x for x in res_j if "collectionName" in x]
    
    else:
        if attr == "all":
            attr = ""
        
        params = dict(term=freetext, country=country, media="music",
            entity="album", attribute=attr, limit="200")
        
        res = requests.get("https://itunes.apple.com/search", params=params)
        
        if not res:
            raise Exception("URL response failed with error: {}".format(res.status_code))
        
        res_j = res.json()["results"]
    
    albums = [x["collectionName"] for x in res_j]
    
    if verbose:
        print("\n" + col + " Albums found " + reset)
        print("\n".join(albums))
    
    # closest album match using Levenshtein edit distance, low cost to deletions
    dists = tuple(ldist(x.lower(), albumtitle.lower(), (1, 20, 15)) for x in albums)
    index = dists.index(min(dists))
    match = albums[index]
    
    if verbose:
        print("\n" + col + " Album match " + reset)
        print(match)
    
    filename = res_j[index]["artistName"] + " - " + match + ext
    filename = filename.replace("/", ".")
    imgurl0 = res_j[index]["artworkUrl60"]
    
    # change file name so it refers to original resolution
    imgurl = imgurl0.rsplit("/", 1)[0] + "/10000x10000" + ext
    
    if verbose:
        print("\n" + col + " Downloading from image source " + reset + "\n" + imgurl, "\n")
        
    imgreq = requests.get(imgurl)
    open(filename, 'wb').write(imgreq.content)
    
    if verbose:
        print(col + " File saved " + reset + "\n" + filename)



download_albumart(freetext=args.freetext, albumtitle=args.album, attr=args.attr, 
    country=args.country, ext=".png", verbose=not args.quiet)

