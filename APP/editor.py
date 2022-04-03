from asyncio.log import logger
from moviepy.editor import *

class Editor():
    def __init__(self, films, intro, outro, directory):
        self.films = films
        self.intro = intro
        self.outro = outro
        self.directory = directory
        
    def edit(self):
        clips = []
        if self.intro:
            intro = ImageClip('static/intro.jpg', duration=5)
            intro = intro.fadeout(0.5)
            clips.append(intro)
        
        for film in self.films:
            clip = VideoFileClip(film['film'], target_resolution=(1080, 1920)).subclip(film['from'], film['to'])
            
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
        fin.write_videofile(self.directory, preset='fast', threads=4)