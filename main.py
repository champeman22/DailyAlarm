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

    def pause(self):
        mixer.music.pause()

    def resume(self):
        mixer.music.unpause()
        
    def stop(self):
        mixer.music.stop()

    def snooze(self):
        mixer.music.pause()
        print('You\'ve hit snooze', self.snoozeCounter, 'times.')
        time.sleep((60*(self.snoozeCounter))-(time.time()-self.start))
        self.snoozeCounter += 1
        self.play()
    
    def dismiss(self):
        mixer.music.stop()

    def set_time(self,dt):
        self.current_time = time.strftime("%m/%d/%Y %H:%M")
        
class sample_kvfileApp(App):
    def build(self):
        self.title = 'Champeman22 App'
        cm = Alarm()
        cm.load('RememberMe.mp3')
        Clock.schedule_interval(cm.set_time, 0.1)
        return cm

sample_kvfileApp().run()
