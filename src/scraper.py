import requests
from bs4 import BeautifulSoup
import datetime

class URLHandler() :
    BASE_URL = 'https://www.kleinanzeigen.de/'

    search_url = lambda search : f"https://www.kleinanzeigen.de/s-{search}/k0"
    price_search_url = lambda search, price_from='', price_to='' : f"https://www.kleinanzeigen.de/s-preis:{price_from}:{price_to}/{search}/k0"

    def __init__(self, scrape_given_url : bool = True, search : str = None, max_price : int = 0, min_price : int = 0, url_to_scrape : str = None):
        
        self.scrape_given_url : bool = scrape_given_url

        if self.scrape_given_url :
            self.url_to_scrape : str = url_to_scrape
        else :
            self.search : str = search
            self.max_price : int = max_price
            self.min_price : int = min_price
            
            if self.max_price == 0 and self.min_price == 0 :
                self.url_to_scrape : str = URLHandler.search_url(search=self.search)
            else :
                self.url_to_scrape : str = URLHandler.price_search_url(search=self.search, price_from=self.min_price, price_to=self.max_price)


    def __repr__(self):
        return f"URLHandler(url_to_scrape='{self.url_to_scrape}')"
    
    def get_content_data(self) :
        return requests.get(self.url_to_scrape).content
    



class KASraper(BeautifulSoup) : 

    def __init__(self, markup = "", features = None, builder = None, parse_only = None, from_encoding = None, exclude_encodings = None, element_classes = None, **kwargs):
        super().__init__(markup, features, builder, parse_only, from_encoding, exclude_encodings, element_classes, **kwargs)
            
    
    def set_date_published(self, date_published) :
        self.date_published : datetime = date_published
    
    def set_location_from(self, location_from) :
        self.location_from : datetime = location_from

    def set_max_distance(self, max_distance) :
        self.max_distance : datetime = max_distance



class KAManager() :
    def __init__(self, scrape_given_url : bool = True, search : str = None, max_price : int = 0, min_price : int = 0, url_to_scrape : str = None):
        self.url_handler = URLHandler(scrape_given_url, search, max_price, min_price, url_to_scrape)
        content = self.url_handler.get_content_data()

        self.ka_scraper = KASraper(content, "html.parser")
