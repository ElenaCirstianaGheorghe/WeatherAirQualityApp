from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import Snackbar

import requests
import json

import WeatherAirQualityApp_pollutionlevels as pollution_levels
from WeatherAirQualityApp_helper import KV

#Window.size = (300, 500)

class Container(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True

class MenuScreen(Screen):
    pass

class WeatherScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(MenuScreen(name="menu"))
sm.add_widget(WeatherScreen(name="weather"))

class AirControlApp(MDApp):

    def build(self):
        self.root = Builder.load_string(KV)
        return self.root

    def show_aqi(self):
        """It is looking through API for the air quality index coresponding to
        the user input. If the name city is found another function is called to
        show the index, else a snackbar will show a message explaining that the
        city has not been found."""

        try:
            self.city_name = self.root.get_screen(
                            "menu").ids.user_input.text
            self.source_aqi = requests.get(
                            f'https://api.waqi.info/feed/{self.city_name.lower()}\
                            /?token=f37fe96b9bf9deafacdb2edc057908fd0b0e2e71')
            self.api_aqi = json.loads(self.source_aqi.content)
            self.aqi = self.api_aqi['data']['aqi']
            self.aqi_info_button()
        except Exception:
            self.root.get_screen(
                        "menu").ids.info_button.text = ""
            self.root.get_screen(
                        "menu").ids.info_button.md_bg_color = 1, 1, 1, 1
            self.root.get_screen(
                        "menu").ids.info_button.on_release = self.no_action
            self.snackbar = Snackbar(text="There are no results for your search!")
            self.snackbar.show()

    def aqi_info_button(self):
        """It shows the index together with a small description in a button which
        is coloured depending on the air quality."""

        info = f"Air quality index: {self.aqi}\n"

        if self.aqi < 51:
            self.root.get_screen(
                        "menu").ids.info_button.text= f"{info} Good"
            self.root.get_screen(
                        "menu").ids.info_button.md_bg_color = 0, 193/255.0, 0, 1
        elif 50 < self.aqi < 101:
            self.root.get_screen(
                        "menu").ids.info_button.text = f"{info}Moderate"
            self.root.get_screen(
                        "menu").ids.info_button.md_bg_color = 244/255.0,\
                                                            238/255.0, 0, 1
        elif 100 < self.aqi < 151:
            self.root.get_screen(
                        "menu").ids.info_button.text = f"{info}Unhealthy for\
                                                        Sensitive Groups"
            self.root.get_screen(
                        "menu").ids.info_button.md_bg_color = 245/255.0,\
                                                            130/255.0, 0, 1
        elif 150 < self.aqi < 201:
            self.root.get_screen(
                        "menu").ids.info_button.text = f"{info}Unhealthy"
            self.root.get_screen(
                        "menu").ids.info_button.md_bg_color = 230/255.0,\
                                                            50/255.0, 99/255.0, 1
        elif 200 < self.aqi < 301:
            self.root.get_screen(
                        "menu").ids.info_button.text = f"{info}Very Unhealthy"
            self.root.get_screen(
                        "menu").ids.info_button.md_bg_color = 135/255/0, 0,\
                                                            170/255.0, 1
        elif self.aqi > 300 :
            self.root.get_screen(
                        "menu").ids.info_button.text = f"{info}Hazardous"
            self.root.get_screen(
                        "menu").ids.info_button.md_bg_color = 133/255.0,\
                                                            0, 29/255.0, 1
        self.root.get_screen(
                    "menu").ids.info_button.on_release = self.show_dialog

    def show_dialog(self):
        """It shows more information in a dialog box about the air quality
        considering its index."""

        self.dialog = MDDialog(text = "", type = "alert", size_hint= (0.6, 0.5),
                        buttons=[MDFlatButton(text="OK",
                                text_color=self.theme_cls.primary_color,
                                on_release = self.close_dialog)])
        if self.aqi < 51:
            self.dialog.text = pollution_levels.good
        elif 50 < self.aqi < 101:
            self.dialog.text = pollution_levels.moderate
        elif 100 < self.aqi < 151:
            self.dialog.text = pollution_levels.unhealthy_sensitive
        elif 150 < self.aqi < 201:
            self.dialog.text = pollution_levels.unhealthy
        elif 200 < self.aqi < 301:
            self.dialog.text = pollution_levels.very_unhealthy
        elif self.aqi > 300:
            self.dialog.text = pollution_levels.hazardous

        self.dialog.open()

    def close_dialog(self, instance):
        """It closes the dialog box containing further information about the air
        quality."""

        self.dialog.dismiss()

    def clear_info(self):
        """ It clears all the information found on the 'menu' screen and the
        button containing the air quality index is disabled."""

        self.root.get_screen(
                        "menu").ids.user_input.text = ""
        self.root.get_screen(
                    "menu").ids.info_button.text = ""
        self.root.get_screen(
                    "menu").ids.info_button.md_bg_color = 1, 1, 1, 1
        self.root.get_screen(
                    "menu").ids.info_button.on_release = self.no_action

    def no_action(self):
        """ The function is used to disable the air quality index button."""
        pass

    def show_weather_screen(self):
        """ It searches the weather for the user input through API.
        If the name city is found another function is called to show additional
        information and the screen is changed, else a snackbar will show a
        message explaining the city has not been found."""

        try:
            self.city_name = self.root.get_screen(
                            "menu").ids.user_input.text
            self.source_weather = requests.get(
                                f'http://api.openweathermap.org/data/2.5/weather?q={self.city_name.lower()}&appid=d55be5a2ffa2717965723f2fd1d5ca7f')
            self.api_weather = json.loads(self.source_weather.content)
            self.weather_info_button()
            self.root.current = "weather"
        except Exception:
            self.snackbar = Snackbar(text="There are no results for your search!")
            self.snackbar.show()

    def weather_info_button(self):
        """It shows the information about the weather (city name, icon, temperature,
        small description)"""

        self.root.get_screen(
                    "weather").ids.city.text = self.city_name.upper()

        self.icon_name = self.api_weather['weather'][0]['icon']
        self.root.get_screen(
                    "weather").ids.icon_label.icon = f'Icons\{self.icon_name}@2x.png'  #don't forget to write the path for the directory where the Icons file is stored 

        self.temp_kelvin = self.api_weather['main']['temp']
        self.temp_celsius = int(self.temp_kelvin - 273.15)
        self.root.get_screen(
                    "weather").ids.temp.text = f'{str(self.temp_celsius)} °C'

        self.root.get_screen(
                    "weather").ids.main_description.text =\
                                        self.api_weather['weather'][0]['main']

        self.root.get_screen(
                    "weather").ids.add_description.text =\
                                    self.api_weather['weather'][0]['description']

    def nav_drawer_info(self):
        """ When the plus button from the navigation drawer is pressed
        a dialog box contain additional information will be displayed on the
        screen."""

        info = "Data obtained from openweathermap.org and aqicn.org/api."
        self.dialog_nav_drawer = MDDialog(text= info, size_hint=(0.6, 0.5),
                                buttons=[MDFlatButton(text="OK",
                                text_color=self.theme_cls.primary_color,
                                on_release=self.close_dialog_nav_drawer)])
        self.dialog_nav_drawer.open()

    def close_dialog_nav_drawer(self, instance):
        """It closes the dialog box from the navigation drawer containing
        further information."""

        self.dialog_nav_drawer.dismiss()

AirControlApp().run()
