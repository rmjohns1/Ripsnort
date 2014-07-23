#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import re


from MediaContent import MediaContent


class MediaScraper:

    def __init__(self,params):
        dirname = os.path.dirname(os.path.realpath( __file__ ))
        
        scraperType = params['type']

        if scraperType.lower() == 'imdb':
            sys.path.append(dirname + "/imdb")
            import imdb
            self.api = imdb.IMDb()

    def findMovie(self,movie,year=None):
        movie = movie.strip()
        
        if year is None:
            year = MediaScraper._extractYearFromName(movie)
            movie = MediaScraper._removeYearFromName(movie)

        return self.api.findMovie(movie,year)

    def findTVShow(self,tvshow,year=None):
        tvshow = tvshow.strip()
        return self.api.findTVShow(tvshow,year)
        
    def findContent(self,contentType,searchword):
        if contentType.lower().strip() == 'movie':
            return self.findMovie(searchword)
        elif contentType.lower().strip() == 'tvshow':
            return self.findTVShow(searchword)
        else:
            return None
    

    @staticmethod
    def _extractYearFromName(name):
        yearReturn = None

        matchGroups = re.findall(r'(\b\d{4}\b)',name)
        
        import datetime
        currentYear = datetime.date.today().year
        
        for yearFound in matchGroups:
            if int(yearFound) > 1900 and int(yearFound) < (currentYear+1):
                if yearReturn is not None:
                    #we already have a candidate. Can't be sure about either so back out
                    yearReturn = None
                    break
                else:
                    yearReturn = int(yearFound)
                    
        return yearReturn

    @staticmethod
    def _removeYearFromName(name):
        nameReturn = name
        
        year = MediaScraper._extractYearFromName(name)
        
        if year is not None:
            nameReturn = nameReturn.replace(str(year),'')
            nameReturn = nameReturn.replace('()','')
            nameReturn = nameReturn.replace('[]','')
            nameReturn = nameReturn.strip()
        
        return nameReturn

if __name__ == "__main__":
    m = MediaScraper('imdb',{})
    assert m.findMovie('The Ant Bully')[0].productionYear == 2006
    assert MediaScraper._extractYearFromName('Toy Story 3 2017') == None
    assert MediaScraper._extractYearFromName('Toy Story 3') == None
    assert MediaScraper._extractYearFromName('Toy Story 3 1899') == None
    assert MediaScraper._extractYearFromName('Toy Story 3 2010') == 2010
    assert MediaScraper._extractYearFromName('Toy Story 3 2010 2013') == None
    assert MediaScraper._extractYearFromName('Toy Story 3 2010 12') == 2010
    assert MediaScraper._extractYearFromName('Toy Story 3 2010 123') == 2010
    assert MediaScraper._extractYearFromName('Toy Story 3 (2010) 123') == 2010
    assert MediaScraper._removeYearFromName('Toy Story 3') == 'Toy Story 3'
    assert MediaScraper._removeYearFromName('Toy Story 3 (2010)') == 'Toy Story 3'
    assert MediaScraper._removeYearFromName('Toy Story 3 [2010]') == 'Toy Story 3'