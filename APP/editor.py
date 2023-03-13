from tkinter import DISABLED, NORMAL
from tkinter.messagebox import showinfo, showerror
from moviepy.video.compositing.concatenate import concatenate_videoclips, CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.VideoClip import ImageClip, TextClip
from logger import MyBarLogger
#from uploader import upload

class Editor():
    def __init__(self, films, intro, outro, directory:str, progress_bar, btn1):
        """
            Editor for concatenating video file clips into single movie

        Args:
            films (list): List of dictionaries containing films parameters
            intro (int): If intro should be added
            outro (int): If outro should be added
            directory (str): Directory to save final file to
            progress_bar (Progressbar): Progress bar to update
            btn1 (Button): Render button to turn on and off while editing
        """
        self.films = films
        self.intro = intro
        self.outro = outro
        self.btn1 = btn1
        # self.title = title
        # self.description = description
        self.directory = directory
        self.logger = MyBarLogger(progress_bar)
        
    def handle_intro(self, clips):
        """
            Add intro to existing list of clips

        Args:
            clips (list): List of clips to append outro to
        """
        if self.intro:
            intro = VideoFileClip('static/intro.mp4', target_resolution=(1080, 1920), fps_source='fps')
            intro = self.handle_fades(intro, True, True)
            clips.append(intro)
            
    def handle_outro(self, clips):
        """
            Add outro to existing list of clips

        Args:
            clips (list): List of clips to append outro to
        """
        if self.outro:
            outro = ImageClip('static/ending.jpg', duration=5)
            outro = self.handle_fades(outro, True, True)
            clips.append(outro)

    def handle_fades(self, clip, to_fadein:bool, to_fadeout:bool):
        """
            Add fadein, fadeout effect to clip

        Args:
            clip (VideoFileClip): Clip to edit
            to_fadein (bool): If fade in should be added
            to_fadeout (bool): If fade out should be added

        Returns:
            clip: Clip after optional fadein, fadeout
        """
        if to_fadein:
            clip = clip.fx(fadein, 0.5)     
        if to_fadeout:
            clip = clip.fx(fadeout, 0.5)
            
        return clip
        
    def edit(self):
        """
            Concatenate video file clips and save edited movie to chosen directory
        """
        self.btn1['state'] = DISABLED
        
        clips = []
        
        self.handle_intro(clips)
        
        for film in self.films:
            try:
                if film['is_text']:
                    bg = ImageClip('static/blackscreen.jpg', duration=6)
                    text = TextClip(film['film'], fontsize=55, color='white', align='center', stroke_color='black', method='caption', size=(1920,1080))
                    clip = CompositeVideoClip([bg, text]).subclip(0, 6)
                else:
                    clip = VideoFileClip(film['film'], target_resolution=(1080, 1920), fps_source='fps')
                    
                    duration = int(clip.duration)
                
                    if film['to'] > duration:
                        showerror('BŁĄD', f"Błąd długości... \nSprawdź czy film\n{film['film']}\ntrwa do {film['to']//60}:{film['to'] - film['to']//60*60}")
                        self.logger.reset_pb()
                        self.btn1['state'] = NORMAL 
                        return None
                        
                    clip = clip.subclip(film['from'], film['to'])
                
                clip = self.handle_fades(clip, film['in'], film['out'])

                clips.append(clip)
            except:
                self.btn1['state'] = NORMAL
            
        self.handle_outro(clips)
            
        fin = concatenate_videoclips(clips, method='compose')
        self.logger.reset_pb()
        fin.write_videofile(self.directory, preset='fast', threads=4, logger=self.logger)
        self.btn1['state'] = NORMAL            
        
    def edit_and_upload(self):
        #self.edit()
        #upload(self.directory, self.title, self.description)
        showinfo(title='Koniec autoryzacji', message='Uruchomiono upload\n1. Dodaj film do playlisty\n2. Uruchom zarabianie\n3. Ustaw film jako publiczny')