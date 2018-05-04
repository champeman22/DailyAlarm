import kivy
kivy.require("1.8.0")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import NumericProperty, StringProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.clock import Clock
import time
import os
import random
try:
    import pygame.mixer as mixer
except ImportError:
    import android.mixer as mixer

class Alarm(BoxLayout):
    start=0
    snoozeCounter=NumericProperty(1)
    current_time=StringProperty()
    
    def load(self,song):
        mixer.init()
        mixer.music.load(song)
        
    def play(self):
        if self.snoozeCounter==1:
            self.start=time.time()
        mixer.music.play()
        #need to add code to account for no user action

    def snooze(self):
        mixer.music.pause()
        #print('You\'ve hit snooze', self.snoozeCounter, 'times.')
        time.sleep((60*(self.snoozeCounter))-(time.time()-self.start))
        self.snoozeCounter += 1
        self.play()
    
    def dismiss(self):
        mixer.music.stop()
        #add code to exit  

    def set_time(self,dt):
        self.current_time = time.strftime("%m/%d/%Y %H:%M")

    def get_song(self):
        DOTW=str(time.strftime('%A'))
        songpath=os.getcwd()+'\\'+DOTW
        choices=os.listdir(songpath)
        #add default song if len(choices)=0
        if len(choices)!=0:
            song=choices[random.randint(0,len(choices)-1)]
            #cycle through rather than pick random?
            self.load(songpath+'\\'+song)
        else:
            song='RememberMe.mp3'
            self.load(song)        
        
class MainScreenKVApp(App):
    def build(self):
        self.title = 'Champeman22 App'
        home = Alarm()
        Popup=TimePickerKVApp()
        alarm_time=Popup.set_alarm_time()
        #add one day of seconds if time already passed today
        if alarm_time-time.time()<0:
            alarm_time+=86400
        #sleep until the right time
        time.sleep(alarm_time-time.time())
        #Figure out threading here for the sleep piece
        
        #get song to play for the day
        home.get_song()
        home.play()
        Clock.schedule_interval(home.set_time, 0.1)
        return home

class TimePickerKVApp(App):
    def set_alarm_time(self):
        #incorporate time picker
        #time_input = str(raw_input("Please enter the time in HH:MM:SS format: "))
        #use below for testing purposes
        time_input='10:23:10'
        current_date=time.strftime('%Y/%m/%d')
        selected_time = time.mktime(time.strptime('%s %s'%(current_date, time_input),"%Y/%m/%d  %H:%M:%S"))
        return selected_time

MainScreenKVApp().run()
