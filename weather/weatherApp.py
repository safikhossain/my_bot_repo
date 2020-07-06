import string
import pandas as pd
from pandasql import sqldf
import xlrd
#from tabulate import tabulate

import pyowm
from config.config_reader import ConfigReader

pysqldf = lambda q: sqldf(q, globals())
#w_data = pd.read_excel("C:\\Users\\shossain\\Documents\\Projects\\Chatbot Sourav\\Azure\\weatherbot\\my_bot_repo_1\\Data\\weather_data.xlsx")
w_data = pd.read_excel("./Data/weather_data.xlsx",sheet_name='Sheet1')

class WeatherInformation():
    def __init__(self):
        self.config_reader = ConfigReader()
        self.configuration = self.config_reader.read_config()
        self.owmapikey = self.configuration['WEATHER_API_KEY']
        self.owm = pyowm.OWM(self.owmapikey)

    def get_weather_info(self,city):
        self.city=city

        mgr = self.owm.weather_manager()
        observation = mgr.weather_at_place(city)
        #get weather for the passed city
        weather = observation.weather
        #min max temperatures
        temp_dict_celsius = (weather.temperature('celsius'))
        min_temp = str(temp_dict_celsius['temp_min'])
        max_temp = str(temp_dict_celsius['temp_min'])
        #wind = str(weather.wind)
        humid = str(weather.humidity)
        
        self.bot_replies = "Today the weather in "+city+".\n Maximum Temperature :"+max_temp+" degree celsius"+".\n Minimum Temperature :"+min_temp+" degree celsius. "+". \n Humidity: "+humid
        return self.bot_replies

    def get_weather_data(self,city):
        self.city=city
        

        MainQuery="select  Date, City,Temp, max_temp,min_temp,Humid, Wind from w_data where "+"City="+"'"+string.capwords(city)+"'"
        res=pysqldf(MainQuery)
        #res = tabulate(res)
        res=res.to_html(index=False,border=0)   
        
        self.bot_replies = res
        return self.bot_replies