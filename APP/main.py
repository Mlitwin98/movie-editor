from email.policy import default
from fileinput import filename
from tkinter import BOTTOM, DISABLED, HORIZONTAL, LEFT, NW, RIGHT, VERTICAL, X, Y, Checkbutton, Label, Tk, font, ttk, Frame, NORMAL, Text, Canvas
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
        self.set_scrollbar()
        self.start_widgets()

    # ROOT   
    def config_root(self):
        self.resizable(width=False, height=False)
        self.geometry('1080x800')
        self.title("Movie Edit")
        self.main_color = '#eaeaf2'
        self.configure(background = self.main_color)
        
        self.left_side_widgets = {
            'buttons':[],
            'in':[],
            'out':[],
            'from':[],
            'to':[],
            'films':[]
        }
    
    # STYLE  
    def config_style(self):
        self.s = ttk.Style()
        self.s.configure('My.Label', background=self.main_color, font=('TkDefaultFont', 18))
        self.s.configure('TEntry', background='#ffffff', padding='10 10 10 10')        
        
    def set_scrollbar(self):
        def onCanvasConfigure(e):
            lutCanvas.itemconfig('frame', width=lutCanvas.winfo_width())
        
        lutCanvas = Canvas(self, background='#eaeaf2')
        scroll = ttk.Scrollbar(lutCanvas, orient=VERTICAL, command=lutCanvas.yview)
        self.write_frame = Frame(lutCanvas)
        
        lutCanvas.configure(yscrollcommand=scroll.set)
        lutCanvas.bind('<Configure>', lambda e: lutCanvas.configure(scrollregion=lutCanvas.bbox('all')))

        def _on_mouse_wheel(event):
            lutCanvas.yview_scroll(-1 * int((event.delta / 120)), "units")
            
        lutCanvas.bind_all("<MouseWheel>", _on_mouse_wheel)

        scroll.pack(side=RIGHT, fill=Y)
        lutCanvas.place(relheight=1, relwidth=0.4, relx=0)
        lutCanvas.create_window((0, 0), window=self.write_frame, anchor=NW, tags='frame')
        lutCanvas.bind("<Configure>", onCanvasConfigure)
        
        
        
        self.write_frame.columnconfigure(0, weight=2)
        self.write_frame.columnconfigure(1, weight=3)
        self.write_frame.columnconfigure(2, weight=3)
        self.write_frame.columnconfigure(3, weight=1)
        self.write_frame.columnconfigure(4, weight=1)
        
        
        
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
        
        #LEFT SIDE WIDGETS
        #LABELS TOP
        Label(self.write_frame, text="Film", height=3, font=('TkDefaultFont', 14, 'bold')).grid(row = 0, column=0)
        Label(self.write_frame, text="Od", height=3, font=('TkDefaultFont', 14, 'bold')).grid(row = 0, column=1)
        Label(self.write_frame, text="Do", height=3, font=('TkDefaultFont', 14, 'bold')).grid(row = 0, column=2)
        Label(self.write_frame, text="IN", height=3, font=('TkDefaultFont', 14, 'bold')).grid(row = 0, column=3)
        Label(self.write_frame, text="OUT", height=3, font=('TkDefaultFont', 14, 'bold')).grid(row = 0, column=4)
        
        
        #START BTN
        self.left_side_widgets['buttons'].append(ttk.Button(self.write_frame, text='Wybierz film', command=self.button_film_click))
        self.left_side_widgets['in'].append(Checkbutton(self.write_frame, padx=10))
        self.left_side_widgets['out'].append(Checkbutton(self.write_frame, padx=10))
        
        self.place_widgets()
        
    def place_widgets(self):
        self.titleEntry.insert(0, ' - Dzika Gostomia cz. ***')
        self.titleEntry.place(x=700, y=45)
        
        self.descriptionEntry.place(x=700, y=135)
        
        self.thBtn.place(x=900, y=300)
        
        # LEFT
        self.left_side_widgets['buttons'][0].grid(row = 1, column = 0)
        self.left_side_widgets['in'][0].grid(row = 1, column = 3)
        self.left_side_widgets['out'][0].grid(row = 1, column = 4)
        self.left_side_widgets['in'][0].select()
        self.left_side_widgets['out'][0].select()
        
    def button_min_click(self):
        self.thumbnailFileName = askopenfilename(filetypes=[("Images", "*.jpg")])
        if self.thumbnailFileName:
            self.thBtn.config(text=basename(self.thumbnailFileName))
        
    def button_film_click(self):
        pass    
        
if __name__ == '__main__':
    App().mainloop()