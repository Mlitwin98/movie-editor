from fileinput import filename
from tkinter import DISABLED, GROOVE, RIDGE, SUNKEN, Tk, font, ttk, Frame, StringVar, Spinbox, NORMAL, Text
from tkinter.constants import TOP, BOTH
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno

from datetime import date, timedelta
from os.path import basename

class App(Tk):
    def __init__(self):
        super().__init__()
        self.config_root()
        self.config_style()
        self.start_widgets()

    # ROOT   
    def config_root(self):
        self.resizable(width=False, height=False)
        self.geometry('1080x800')
        self.title("Movie Edit")
        self.main_color = '#eaeaf2'
        self.configure(background = self.main_color)
    
    # STYLE  
    def config_style(self):
        self.s = ttk.Style()
        self.s.configure('My.Label', background=self.main_color, font=('TkDefaultFont', 18))
        self.s.configure('TEntry', background='#ffffff', padding='10 10 10 10')        
        
    def start_widgets(self):        
        #Labels
        ttk.Label(self, text='Tytuł:', style='My.Label').place(x=700, y=10)
        ttk.Label(self, text='Opis:', style='My.Label').place(x=700, y=100)
        ttk.Label(self, text='Miniaturka:', style='My.Label').place(x=700, y=300)
        
        #Entries
        self.titleEntry = ttk.Entry(self, style='TEntry', font=('TkDefaultFont', 14, 'bold'), width=30)
        self.descriptionEntry = Text(self, background='#ffffff', font=('TkDefaultFont', 14), width=30, height=6, padx=10, pady=10)
        
        #Button
        self.thBtn = ttk.Button(self, width=15, text='Wybierz...', command=self.button_min_click)
        
        self.place_widgets()
        
    def place_widgets(self):
        self.titleEntry.insert(0, ' - Dzika Gostomia cz. ***')
        self.titleEntry.place(x=700, y=45)
        
        self.descriptionEntry.place(x=700, y=135)
        
        self.thBtn.place(x=900, y=300)
        
    def button_min_click(self):
        self.thumbnailFileName = askopenfilename(filetypes=[("Images", "*.jpg")])
        if self.thumbnailFileName:
            self.thBtn.config(text=basename(self.thumbnailFileName))
        
if __name__ == '__main__':
    App().mainloop()