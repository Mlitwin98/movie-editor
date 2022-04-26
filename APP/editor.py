from tkinter import DISABLED, NORMAL
from tkinter.messagebox import showinfo
from moviepy.editor import *
from logger import MyBarLogger
from uploader import upload

class Editor():
    def __init__(self, films, intro, outro, directory, progress_bar, btn1, btn2, title, description):
        self.films = films
        self.intro = intro
        self.outro = outro
        self.btn1 = btn1
        self.btn2 = btn2
        self.title = title
        self.description = description
        self.directory = directory
        self.logger = MyBarLogger(progress_bar)
        
    def edit(self):
        self.btn1['state'] = DISABLED
        self.btn2['state'] = DISABLED
        
        clips = []
        if self.intro:
            intro = VideoFileClip('static/intro.mp4', target_resolution=(1080, 1920), fps_source='fps')
            intro = intro.fadein(0.5)
            intro = intro.fadeout(0.5)
            clips.append(intro)
        
        for film in self.films:
            clip = VideoFileClip(film['film'], target_resolution=(1080, 1920), fps_source='fps').subclip(film['from'], film['to'])
            
            if film['in']:
                clip = clip.fadein(0.5)
                
            if film['out']:
                clip = clip.fadeout(0.5)
                
            clips.append(clip)
            
        if self.outro:
            outro = ImageClip('static/ending.jpg', duration=5)
            outro = outro.fadein(0.5)
            outro = outro.fadeout(0.5)
            clips.append(outro)
            
        fin = concatenate_videoclips(clips, method='compose')
        self.logger.reset_pb()
        fin.write_videofile(self.directory, preset='fast', threads=4, logger=self.logger)
        self.btn1['state'] = NORMAL
        self.btn2['state'] = NORMAL            
        
    def edit_and_upload(self):
        #self.edit()
        upload(self.directory, self.title, self.description)
        showinfo(title='Koniec autoryzacji', message='Uruchomiono upload\n1. Dodaj film do playlisty\n2. Uruchom zarabianie\n3. Ustaw film jako publiczny')