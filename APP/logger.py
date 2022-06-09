from proglog import ProgressBarLogger
from tkinter.messagebox import showinfo

class MyBarLogger(ProgressBarLogger):
    def __init__(self, progress_bar):
        super().__init__(init_state=None, bars=None, ignored_bars=None, logged_bars='all', min_time_interval=0, ignore_bars_under=0)        
        self.progress_bar = progress_bar
        self.one_timer = True
        
    def callback(self, **changes):
        try:
            index = self.state['bars']['t']['index']
            total = self.state['bars']['t']['total']
            percent_complete = index / total * 100
            if percent_complete < 0:
                percent_complete = 0
            if percent_complete >= 100:
                percent_complete = 0
                if self.one_timer:
                    showinfo(title='Koniec renderowania', message='Renderowanie zakończone')
                    self.one_timer = False
                
            self.progress_bar['value'] = percent_complete
        except KeyError as e:
            pass
        
    def reset_pb(self):
        self.one_timer = True