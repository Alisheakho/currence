from kivy.config import Config
Config.set('graphics','position','custom')
Config.set('graphics','left',0)
Config.set('graphics','top',30)

from kivy.core.window import Window
Window.size= (1000,600)

#=======================================

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager , Screen 
import sqlite3
from kivymd.uix.segmentedcontrol.segmentedcontrol  import MDSegmentedControl , MDSegmentedControlItem
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivymd.uix.dialog import MDDialog
import matplotlib.pyplot as plt
import json
import requests


class Login_screen(Screen):
    dialog = None
    def login(self,app):
        conn = sqlite3.connect('D:/projectpython/first_db.db')

        #create a cursor
        c = conn.cursor()
        
        user = f"'{self.ids.user.text}'"
        pas = f"'{self.ids.pswrd.text}'"
        query = f"SELECT * FROM users WHERE username={user} AND password={pas}"
        # print(query)
        c.execute(query)
    
        records = c.fetchall()
        # print(records)
        
        conn.commit()
        conn.close()


        if len(records) == 0 :
            self.show_alert_dialog()
        else:  app.root.current = "coine_sceen"
    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Erorr",
                text="tha email or passoword is not currect",
                radius=[20, 7, 20, 7],
            )
        self.dialog.open()
    
class Figure(FigureCanvasKivyAgg):
    def __init__(self, **kwargs):
        url = f"https://open-api.coinglass.com/public/v2/open_interest_history?symbol=BTC&time_type=m1&currency=USD"
        headers = {
            "accept": "application/json",   
            "coinglassSecret": "9815af10898b4f00be76d2f9cb104cbe"
        } 
        response = requests.request("GET", url, headers=headers)
        print(response)
        jsn = json.loads(response.text.encode('utf8'))
        # print(jsn)
        dataprice = jsn['data']['priceList']
        datelist = jsn['data']['dateList']
        plt.clf()
        plt.style.use("ggplot")
        plt.plot(datelist,dataprice)
        plt.plot(datelist,dataprice,'.')
        plt.title("BTC")
        plt.ylabel("Price")
        plt.xlabel("Time")
        plt.legend(["line time","exchange"])
        super().__init__(plt.gcf(), **kwargs)

class Coine_screen(Screen):
    name_coin = "BTC"
    time = "m1"
    def on_active(self, segmented_control: MDSegmentedControl,segmented_item: MDSegmentedControlItem,) -> None:
        print(segmented_item.text)
        print(self.name_coin)
        self.time = segmented_item.text
        self.add_chart(self.name_coin)

    def add_chart(self,symb):
        self.name_coin = symb
        # coins = ['ETH','BTC','XRP','LTC']
        #m1 m5 m15 h1 h4 h12 all
        url = f"https://open-api.coinglass.com/public/v2/open_interest_history?symbol={symb}&time_type={self.time}&currency=USD"
        headers = {
            "accept": "application/json",   
            "coinglassSecret": "9815af10898b4f00be76d2f9cb104cbe"
        } 
        response = requests.request("GET", url, headers=headers)
        jsn = json.loads(response.text.encode('utf8'))
        print(jsn)
        dataprice = jsn['data']['priceList']
        datelist = jsn['data']['dateList']
        plt.clf()
        plt.style.use("ggplot")
        plt.plot(datelist,dataprice)
        plt.plot(datelist,dataprice,'.')
        plt.title(symb)
        plt.ylabel("Price")
        plt.xlabel("Time")
        plt.legend(["line time","exchange"])
        self.ids.chart.clear_widgets()
        self.ids.chart.add_widget(FigureCanvasKivyAgg(figure=plt.gcf()))

class Screen_manager(ScreenManager):
    pass


class Main_app(MDApp):
          
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        return Builder.load_file("style.kv")  

    def on_start(self):
       pass

Main_app().run()