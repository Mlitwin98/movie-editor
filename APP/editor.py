from tkinter import DISABLED, NORMAL
from tkinter.messagebox import showinfo, showerror
from moviepy.video.compositing.concatenate import concatenate_videoclips, CompositeAudioClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_fadeout import audio_fadeout
from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.audio.fx.volumex import volumex
from moviepy.video.VideoClip import ImageClip, TextClip
from logger import MyBarLogger
#from uploader import upload

## Dumb imports for the sake of working after pyinstaller
from moviepy.video.fx.invert_colors import invert_colors
from moviepy.video.fx.crop import crop
from moviepy.audio.fx.audio_normalize import audio_normalize
from moviepy.video.fx.accel_decel import accel_decel
from moviepy.video.fx.blackwhite import blackwhite
from moviepy.video.fx.blink import blink
from moviepy.video.fx.colorx import colorx
from moviepy.video.fx.crop import crop
from moviepy.video.fx.even_size import even_size
from moviepy.video.fx.freeze import freeze
from moviepy.video.fx.freeze_region import freeze_region
from moviepy.video.fx.gamma_corr import gamma_corr
from moviepy.video.fx.headblur import headblur
from moviepy.video.fx.invert_colors import invert_colors
from moviepy.video.fx.loop import loop
from moviepy.video.fx.lum_contrast import lum_contrast
from moviepy.video.fx.make_loopable import make_loopable
from moviepy.video.fx.margin import margin
from moviepy.video.fx.mask_and import mask_and
from moviepy.video.fx.mask_color import mask_color
from moviepy.video.fx.mask_or import mask_or
from moviepy.video.fx.mirror_x import mirror_x
from moviepy.video.fx.mirror_y import mirror_y
from moviepy.video.fx.painting import painting
from moviepy.video.fx.resize import resize
from moviepy.video.fx.rotate import rotate
from moviepy.video.fx.scroll import scroll
from moviepy.video.fx.speedx import speedx
from moviepy.video.fx.supersample import supersample
from moviepy.video.fx.time_mirror import time_mirror
from moviepy.video.fx.time_symmetrize import time_symmetrize

from moviepy.audio.fx.audio_left_right import audio_left_right
from moviepy.audio.fx.audio_normalize import audio_normalize

class Editor():
    def __init__(self, films, intro, outro, directory:str, progress_bar, btn1, music=None):
        """
            Editor for concatenating video file clips into single movie

        Args:
            films (list): List of dictionaries containing films parameters
            intro (int): If intro should be added
            outro (int): If outro should be added
            directory (str): Directory to save final file to
            progress_bar (Progressbar): Progress bar to update
            btn1 (Button): Render button to turn on and off while editing
            music (str): File path to music file
        """
        self.films = films
        self.intro = intro
        self.outro = outro
        self.btn1 = btn1
        # self.title = title
        # self.description = description
        self.directory = directory
        self.logger = MyBarLogger(progress_bar)
        self.music = music
        
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
    
    def handle_music(self, final_movie):
        if self.music is not None:
            music = AudioFileClip(self.music)
            music = audio_loop(music, duration=final_movie.duration)
            if self.outro:
                music = music.set_end(final_movie.duration-5)
            if self.intro:
                music = music.set_start(6, change_end=False)
            music = music.fx(volumex, 0.15)
            music = music.fx(audio_fadein, 2)
            music = music.fx(audio_fadeout, 2)
            
            
            new_audio = CompositeAudioClip([final_movie.audio, music])
            final_movie.audio = new_audio
        return final_movie
        
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
                    #bg = ImageClip('static/blackscreen.jpg', duration=film['to'])
                    #text = TextClip(film['film'], fontsize=55, color='white', align='center', stroke_color='black', method='caption', size=(1920,1080))
                    
                    clip = TextClip(film['film'], fontsize=55, color='white', align='center', stroke_color='black', method='caption', size=(1920,1080))
                    clip = clip.subclip(0, film['to'])
                    #clip = CompositeVideoClip([bg, text]).subclip(0, film['to'])
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
        
        fin = self.handle_music(fin)
        
        self.logger.reset_pb()
        fin.write_videofile(self.directory, preset='fast', threads=4, logger=self.logger)
        self.btn1['state'] = NORMAL            
        
    def edit_and_upload(self):
        #self.edit()
        #upload(self.directory, self.title, self.description)
        showinfo(title='Koniec autoryzacji', message='Uruchomiono upload\n1. Dodaj film do playlisty\n2. Uruchom zarabianie\n3. Ustaw film jako publiczny')