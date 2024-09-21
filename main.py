import requests
from bs4 import BeautifulSoup
import datetime
import json
import gspread
import pandas
import numpy as np
import logging
import traceback


today = datetime.datetime.today()
date_save = today.strftime("%Y-%m-%d")
logging.basicConfig(filename='scraper.log',level=logging.INFO,
                    encoding='utf-8',
                    format='%(asctime)s : %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

filename = __file__.split('\\')[-1]

def clear_log_file():
    with open('scraper.log', 'w'):
        pass


class Crawl:
    
    creds = {
        "type": "service_account",
        "project_id": "crypto-messari",
        "private_key_id": "9cd2f9d784c4baaba89c4f5f8a565ac47d2b33ab",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCwQ2KpOgPnA7wv\nuBjzFYbkL8vmfuFlQ1e3j8IqG0Ikale7bWfc24E21cK4ZX1zeCbN5R4Rcb560q4L\nLTiLLvsfcZYyh+WCtdih//Jdg7LelwejNP8FemVy5eXvtaWJVLIVw7XDDLxA34dQ\nXrtTECiiT4cZ4S+m/Pt7m6h8e1f3ddrKbAjr91vq6gWlY0x5bIJwvjoc8jkcKzpj\ndQ6VBa6SHjQ2X4qUUEzxflpDh+qbgXm208VBr/sMfwtzueL+F9NmvJ3jSkF/Ahjl\nSNPuKXY6TbwqS+oaPf7mFQRsvXTJ0o7skVLqsoOEsAYd1DDV12usKZaQV35CUh/p\nmSvG9+k5AgMBAAECggEALQO4kaFIV9ojWEh6zrHDtkjimOX0aCkPoMhs/NXjSWuD\nJlGlgcjpMfjbdr4skK2xs0l9KVVUIQfm/OG6nAkOhxQ6GIOOQJhyT8UOv4UfzCrj\n/3FMY7jDadl+pH5OXUktBdPqenqpJSQw6XyX+Hma9wC6bwiMY+gdzY6OM+RILeEV\nc58YvulFxSHAwmb5voh5SEalnnC4G3dO3qOwBaMRzNmEpSs9OIDWQ4/BKCrvViyI\ntcpHgCt/d9AtiU61k1GxJzFiiJt/Pu5abmfnvQhZcLrhG9rkoO4dZ1zvbKKYUzgk\nZkw3Yt1Xk3y34S5rl42XsVOmNAeaRkIy/ZoqDTLZ9QKBgQDm5mWV3Awb5iJjj3C5\n/jigoxLWuBiHkBEQg7krjnStBaAOms1fIWBUP6mw5cBH+BM17uij8c1eqRT3HVwZ\n0j+qQKbd65erMtlmOYucUJSbWcX/kEXIfXEYP+hAmSTAuir8Eqgtu0V7jgpa5ffH\npweCn9Pf1lzckKwqhCT709IrxwKBgQDDbIdamsk85GgZcvaXuEYptg3sVTKsksuV\n7+hymV7sC2zDgegvdde3aFX1VwxlXPdvqJvdWPSWran2lI3Mz6eTPWMSlBPt+tLq\nXYNWSKzQ06WE+eVUmE61WDVw0x8+Jr5aubg8OA6DhdLI6IDqvFp7v4QNB0EvVPsu\nWCT6OgNC/wKBgAFfwZ8ArjnERtQc2Gji8GdUURpiAhNcch2NCx8NO/iDng44MZyt\nUCtwLYxV8az79vFNOKkxGS3FB9DopdGphKN4uwV7D23/YXfQQ9psSFYcVKdOrnug\n83lXeARaZPOYqATT/5g2ExXHJJyh3bWcctj+Jn6ggfD2E3A1VRsCia+lAoGACmUV\ndg5Rsfl8SA5Da6KTqNhUOUP25BMS3TDbrmzWDbw11thsH0onZUwZdmlg8WtWhgvz\n7nwy1mj6Z3FTcZeCFGTphi12Oexjl6/NsqM+/gSkA0S/nBZV6XN9tDimqsmoym6i\njCF3NCvEIIetg87tCTQQtBi0sO3WRorNvLmlPsUCgYAtSEFVqcTe6D6c6mNjyfhX\nrMJ2tR3l9q37C2k4GtXdx1LFeoNusEOyMU7GMTUL5gd7q571IW92mow5U04GmsXp\n2DfA41nVUT7sqnkVCoFt6LQDS+s/5v5KnxNZ23ZEul5Qbygfx9PQaZ/TuyaxZ6+S\nhJrcuKgiWaFyED4Lni/XsQ==\n-----END PRIVATE KEY-----\n",
        "client_email": "pythoncryptomessariaccount@crypto-messari.iam.gserviceaccount.com",
        "client_id": "112559430258363988070",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/pythoncryptomessariaccount%40crypto-messari.iam.gserviceaccount.com"
    }
    
    month_mapping = {
        "Jan": "01", "Feb": "02", "Mar": "03",
        "Apr": "04", "May": "05", "Jun": "06",
        "Jul": "07", "Aug": "08", "Sep": "09",
        "Oct": "10", "Nov": "11", "Dec": "12"
    }
    
    TODAY_MOVIES = []
    YESTERDAY_MOVIES = []
    NEW_MOVIES = []
    
    def get_yesterday_movies(self):
        
        while True:
            try:
                gc = gspread.service_account_from_dict(self.creds)
                spreed_sheet_id = '1HjsWyf8EJARJi192xB8gJIlc5aCPM3xQrPGPHOFUqv8'
                sheet = gc.open_by_key(spreed_sheet_id)
                worksheet = sheet.worksheet('Yesterday')
                self.YESTERDAY_MOVIES = worksheet.col_values(1)[1:]
                break
            except gspread.exceptions.APIError:
                continue  
    
    def compare_movies(self):
        
        for movie in self.TODAY_MOVIES:
            movie_name = movie['event_name']
            if movie_name not in self.YESTERDAY_MOVIES:
                self.NEW_MOVIES.append(movie)
    
    def update_today_movies(self):
        
        save = []
        for item in self.TODAY_MOVIES:
            dic = {}
            dic['Title'] = item['event_name']
            dic['Address'] = item['venue']
            dic['Date'] = item['event_start_date']
            dic['Organised by'] = item['org']
            dic['Description'] = item['event_description']
            dic['Banner url'] = item['banner_url']
            save.append(dic)
            
        df = pandas.DataFrame(save)
        df = df.drop_duplicates()
        df = df.replace(np.nan,'')
        
        while True:
            try:
                SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
                gc = gspread.service_account_from_dict(self.creds)
                spreed_sheet_id = '1HjsWyf8EJARJi192xB8gJIlc5aCPM3xQrPGPHOFUqv8'
                sheet = gc.open_by_key(spreed_sheet_id)
                worksheet = sheet.worksheet('Today')
                worksheet.batch_clear(["A1:EZ"])
                columns = df.columns.values.tolist()
                
                body = df.values.tolist()
                save = []
                save.append(columns)
                for item in body:
                    save.append(item)
                worksheet.update(values=save,range_name='A1',)
                print('Movies Today updated! : ',datetime.datetime.now() , ' | total: ' + str(len(save)))
                break
            except gspread.exceptions.APIError:
                continue
            
    def update_new_movies(self):
        
        df = pandas.DataFrame(self.NEW_MOVIES)
        df = df.drop_duplicates()
        df = df.replace(np.nan,'')
        
        while True:
            try:
                SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
                gc = gspread.service_account_from_dict(self.creds)
                spreed_sheet_id = '1HjsWyf8EJARJi192xB8gJIlc5aCPM3xQrPGPHOFUqv8'
                sheet = gc.open_by_key(spreed_sheet_id)
                worksheet = sheet.worksheet('New_events')
                worksheet.batch_clear(["A1:EZ"])
                columns = df.columns.values.tolist()
                
                body = df.values.tolist()
                save = []
                save.append(columns)
                for item in body:
                    save.append(item)
                worksheet.update(values=save,range_name='A1',)
                print('New moviews Updated! ',datetime.datetime.now() , ' | total: ' + str(len(self.NEW_MOVIES)))
                break
            except gspread.exceptions.APIError:
                continue
            
    def update_yesterday_movies(self):

        while True:
            try:
                gc = gspread.service_account_from_dict(self.creds)
                spreed_sheet_id = '1HjsWyf8EJARJi192xB8gJIlc5aCPM3xQrPGPHOFUqv8'
                sheet = gc.open_by_key(spreed_sheet_id)
                worksheet = sheet.worksheet('List of movies')
                movies = worksheet.col_values(1)[1:]
                self.list_movies = movies
                movie_ids = worksheet.col_values(2)[1:]
                for movie,movie_id in zip(movies,movie_ids):
                    #movie = 'Indian 2'
                    self.movie_name = movie
                    self.movie_id = movie_id
                    href = self.get_movies(movie_name=movie)
                    if href == None:continue
                    self.get_movies_location(href=href)
                
                break
            except gspread.exceptions.APIError:
                continue   
            
    def creat_session(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Cookie': '_gcl_au=1.1.1621302368.1726268309; _fbp=fb.2.1726268309939.615750848407725765; _ga=GA1.3.443276874.1726268310; PHPSESSID=i2q9792rmfqug8081agjtnd915; _gid=GA1.3.1284850931.1726754274; _ga_VY2W6FVJFF=GS1.3.1726754274.2.0.1726754274.60.0.0',
            'Referer': 'https://www.upwork.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        session = requests.Session()
        session.headers.update(headers)
        self.session = session
        
    def scrape_today_movies(self):
        
        response = self.session.get('https://drytickets.com.au/')
        print(response.status_code)
        soup = BeautifulSoup(response.text,'html.parser')
        script_tags = soup.select('[type="application/ld+json"]')
        EVENTS = []
        for script in script_tags:
            if '"Event"' in script.text or "'Event'" in script.text:
                EVENTS = json.loads(script.text.strip())
        
        for event in EVENTS:
            url = event.get('url')
            try:
                self.scrape_event_info(url=url)
            except Exception as e:
                error_message = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
                logging.info("-" * 113)
                logging.info(url)
                logging.error(f"An error occurred: (scrapers\\{filename})\n%s", error_message)
                logging.error("-" * 113)
                
    def scrape_event_info(self,url:str):
        #print('url:',url)
        
        response = self.session.get(url)
        soup = BeautifulSoup(response.text,'html.parser')
        JSON = json.loads(soup.select_one('[type="application/ld+json"]').text.strip())
        JSON = JSON[0]
        dic = {}
        dic['event_name'] = JSON['name']
        dic['event_description'] = JSON['description']
        startDate = JSON.get('startDate')
        calendar = soup.select('.fa.fa-calendar-o')
        if startDate == None and len(calendar) > 1:
            self.scrape_event_with_multiple_locations(soup=soup)
            return None
            
        dic['event_start_date'] = JSON['startDate'].split('T')[0]
        dic['event_start_time'] = JSON['startDate'].split('T')[1][:5]
        dic['venue_latlong'] = ''
        
        LOCATION = JSON['location']['address']
        address_region = LOCATION['addressRegion']
        city_name = 'N/A'
        if address_region == 'VIC':
            city_name = 'Melbourne'
        elif address_region == 'NSW':
            city_name = 'Sydney'
        elif address_region == 'QLD':
            city_name = 'Brisbane'
        elif address_region == 'SA':
            city_name = 'Adelaide'
        elif address_region == 'WA':
            city_name = 'Perth'
        else:
            city_name = LOCATION.get('addressLocality', 'N/A')
        if city_name == None or city_name == '':
            city_name = 'N/A'
        dic['city'] = city_name
        dic['weblink'] = url
        organized = soup.h1.parent.p.get_text(' ',strip=True)
        dic['org'] = ''
        if 'Organised by' in organized:
            dic['org'] = organized.replace('Organised by ','').strip()
        dic['language'] = ''
        dic['venue'] = LOCATION.get('streetAddress','') + ' ' + LOCATION.get('addressLocality','')
        dic['banner_url'] = JSON['image']
        
        print('Name: {}'.format(dic['event_name']))
        self.TODAY_MOVIES.append(dic)
        title = ' completed - ' + dic['event_name']
        logging.info(title)
    
    def scrape_event_with_multiple_locations(self,soup):
        calendar = soup.select('.fa.fa-calendar-o')
        
    
if __name__ == '__main__':
    clear_log_file()
    crawl_obj = Crawl()
    crawl_obj.creat_session()
    crawl_obj.scrape_today_movies()
    crawl_obj.get_yesterday_movies()
    crawl_obj.compare_movies()
    crawl_obj.update_today_movies()
    crawl_obj.update_new_movies()
