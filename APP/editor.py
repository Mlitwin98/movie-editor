from tkinter import DISABLED, NORMAL
from tkinter.messagebox import showinfo
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.VideoClip import ImageClip
from logger import MyBarLogger
#from uploader import upload

class Editor():
    def __init__(self, films, intro, outro, directory, progress_bar, btn1):
        self.films = films
        self.intro = intro
        self.outro = outro
        self.btn1 = btn1
        # self.title = title
        # self.description = description
        self.directory = directory
        self.logger = MyBarLogger(progress_bar)
        
    def edit(self):
        self.btn1['state'] = DISABLED
        
        clips = []
        if self.intro:
            intro = VideoFileClip('static/intro.mp4', target_resolution=(1080, 1920), fps_source='fps')
            intro = intro.fx(fadein, 0.5)
            intro = intro.fx(fadeout, 0.5)
            clips.append(intro)
        
        for film in self.films:
            try:
                clip = VideoFileClip(film['film'], target_resolution=(1080, 1920), fps_source='fps').subclip(film['from'], film['to'])
                
                if film['in']:
                    clip = clip.fx(fadein, 0.5)
                    
                if film['out']:
                    clip = clip.fx(fadeout, 0.5)
                    
                clips.append(clip)
            except:
                self.btn1['state'] = NORMAL
            
        if self.outro:
            outro = ImageClip('static/ending.jpg', duration=5)
            outro = outro.fx(fadein, 0.5)
            outro = outro.fx(fadeout, 0.5)
            clips.append(outro)
            
        fin = concatenate_videoclips(clips, method='compose')
        self.logger.reset_pb()
        fin.write_videofile(self.directory, preset='fast', threads=4, logger=self.logger)
        self.btn1['state'] = NORMAL            
        
    def edit_and_upload(self):
        #self.edit()
        #upload(self.directory, self.title, self.description)
        showinfo(title='Koniec autoryzacji', message='Uruchomiono upload\n1. Dodaj film do playlisty\n2. Uruchom zarabianie\n3. Ustaw film jako publiczny')